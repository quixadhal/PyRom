import ast
import copy
import inspect
import time
import collections
import tokenize
import io
import logging

logger = logging.getLogger()

import merc
import settings
import instance

signals = {'say': []}


def emit_signal(signal, actor=None, victim=None, argument=None, audience=None):
    if actor.dampen:  # Prevent an actor from giving off signals while in scripting.
        return
    actor.dampen = True
    if actor and actor.is_npc():
        actor.absorb(signal, actor, victim, argument)

    if victim and victim.is_npc():
        victim.absorb(signal, actor, victim, argument)

    if audience:
        [instance.global_instances[a].absorb(signal, actor, victim, argument, audience) for a in audience if a != actor and a != victim]
    for prog in signals[signal]:
        prog.execute(actor, victim, argument, audience)
    actor.dampen = False

def register_prog(signal, prog):
    signals[signal].append(prog)

def register_signal(self, signal, prog):
    if signal not in self.listeners:
        self.listeners[signal] = []
    self.listeners[signal].append(prog)

def absorb(self, signal, ch, victim, argument, audience):
    progs = self.listeners.get(signal, [])
    for prog in progs:
        prog.execute(ch, victim, argument, audience)

class Progs:
    def __init__(self, code=None):
        self.code = code
        self.tokens = None
        self.current_scope = 0
        self.exec_else = {0: False}
        self.loop_scope = {0: False}
        self.actor = None
        self.victim = None
        self.argument = ""
        self.compare_ops = ['<', '<=', '>', '>=', '==']
        self.equation_ops = ['**', '+', '-', '/', '*', '(', ')']
        self.process_tokens = {'break': None,
                               'continue': None,
                               'elif': self.process_elif,
                               'else': self.process_else,
                               'for': self.process_for,
                               'if': self.process_if}

    def tokenize(self):
        self.tokens = tokenize.tokenize(io.BytesIO(self.code.encode('utf-8')).readline)

    def increase_scope(self, local_scope):
        self.current_scope += 1

    def decrease_scope(self, local_scope):
        self.current_scope -= 1

    def get_in_scope(self, string, scope, current):
        for i in range(current, -1, -1):
            if string in scope[i]:
                return scope[i][string]
        if string in merc.__dict__:
            return merc.__dict__[string]
        return None

    def jump_scope(self, scope, keep=False):
        tracking = self.current_scope
        tokens = []

        for token in self.tokens:
            if keep:
                tokens.append(copy.deepcopy(token))
            if token.type == tokenize.INDENT:
                tracking = len(token.string) // 4
            if token.type == tokenize.DEDENT:
                tracking -= 1
                if tracking == scope:
                    break
        if keep:
            return tokens


    def token_after_op(self):
        next_token = None
        try:
            next(self.tokens)  # skip the operator
            next_token = next(self.tokens)
        except StopIteration:
            logger.debug("Failed to process a variable with dot operator")
            logger.debug(next_token)
            return None
        if next_token.type == tokenize.NEWLINE:
            logger.debug("Unexpected new line after operator")
            logger.debug(next_token)
        return next_token

    def next_char(self, line, pos, impose=False):
        line_length = len(line)
        try:
            next_char = line[pos]
        except IndexError:
            return ''
        while line[pos] == ' ' and pos + 1 < line_length:
            pos += 1
            next_char = line[pos]
        if impose:
            return pos, next_char
        return next_char

    def compare_conditions(self, values, op):
        outcome = False
        if not values[1]:
            return True if values[0] else False
        if op == '<':
            outcome = values[0] < values[1]
        elif op == '<=':
            outcome = values[0] <= values[1]
        elif op == '>':
            outcome = values[0] > values[1]
        elif op == '>=':
            outcome = values[0] >= values[1]
        elif op == '==':
            outcome = values[0] == values[1]
        del values[:]
        return outcome

    def seek(self, value):
        if type(value) == str:
            for token in self.tokens:
                if token.string == value:
                    return token
        else:
            for token in self.tokens:
                if token.type == value:
                    return token
        return None
    def process_for(self, token, local_scope, scope):
        iterator_tok = copy.deepcopy(next(self.tokens))
        next(self.tokens) # The in
        iterable_tok =  copy.deepcopy(next(self.tokens))
        iterable = self.process_variable(iterable_tok, local_scope, scope)
        self.seek(tokenize.NEWLINE)
        loop = self.jump_scope(local_scope, True)
        self.increase_scope(local_scope)
        local_scope[scope+1] = {iterator_tok.string: None}
        if not iterable and not isinstance(iterable, collections.Iterable):
            logger.debug("For sent a non-iterable %s", iterable_tok.string)
            logger.debug(iterable_tok)
            logger.debug(iterator_tok)
            logger.debug(iterable)
            return
        tokens = self.tokens
        for count, value in enumerate(iterable):
            if count > settings.MAX_ITERATIONS:
                logger.debug("Exceeded max iterations.")
                logger.debug(iterable_tok)
                logger.debug(iterator_tok)
                break
            local_scope[scope+1][iterator_tok.string] = value
            self.tokens = iter(loop)
            for token in self.tokens:
                self.process_token(token, local_scope, scope + 1, [tokenize.NAME, tokenize.OP, tokenize.NEWLINE])
        self.tokens = tokens

    def process_condition(self, token, local_scope, scope, open_paren=0):
        condition = False
        set_value = 0
        values = [None, None]
        op = None
        for token in self.tokens:
            look_forward = self.next_char(token.line, token.end[1])
            if look_forward in self.equation_ops or token.string in self.equation_ops:
                value = self.process_equation(token, local_scope, scope)
                values[set_value] = ast.literal_eval(value)
            elif token.type == tokenize.NAME:
                if token.string == 'and':
                    condition = self.compare_conditions(values, op)
                    if not condition:
                        seek_char = ')' if open_paren > 0 else ':'
                        self.seek(seek_char)
                        return condition
                    values = [None, None]
                    set_value = 0
                    op = None
                elif token.string == 'or':
                    condition = self.compare_conditions(values, op)
                    if condition:
                        seek_char = ')' if open_paren > 0 else ':'
                        self.seek(seek_char)
                        return condition
                    values = [None, None]
                    set_value = 0
                    op = None
                else:
                    values[set_value] = self.process_variable(token, local_scope, scope)
            elif token.type == tokenize.NUMBER:
                values[set_value] = int(token.string)
            elif token.type == tokenize.STRING:
                values[set_value] = token.string[1: -1]
            elif token.type == tokenize.OP:
                if token.string == '(':
                    condition = self.process_condition(token, local_scope, scope, open_paren + 1)
                elif token.string in self.compare_ops:
                    op = token.string
                    set_value = 1
                elif token.string in [')', ':']:
                    return self.compare_conditions(values, op)

    def process_if(self, token, local_scope, scope):
        condition = self.process_condition(token, local_scope, scope)
        self.exec_else[scope] = False
        if not condition:
            self.exec_else[scope] = True
            self.jump_scope(scope)
        else:
            self.increase_scope(local_scope)

    def process_elif(self, token, local_scope, scope):
        if self.exec_else[scope] and self.process_condition(token, local_scope, scope):
            self.exec_else[scope] = False
            self.increase_scope(local_scope)
        else:
            self.jump_scope(scope)

    def process_else(self, token, local_scope, scope):
        self.seek(':')
        if not self.exec_else[scope]:
            self.jump_scope(scope)
        else:
            self.increase_scope(local_scope)

    def process_equation(self, token, local_scope, scope, open_paren=0, equation=''):
        expected = [tokenize.OP, tokenize.NUMBER, tokenize.NAME]
        value = ''
        if token.type in expected:
            if token.type == tokenize.NAME:
                value = self.process_variable(token, local_scope, scope)
            elif token.type == tokenize.NUMBER:
                value = int(token.string)
            elif token.type == tokenize.OP:
                value = token.string
                if value == '(':
                    open_paren += 1
                if value == ')':
                    open_paren -= 1
                next_tok = next(self.tokens)
                return self.process_equation(next_tok, local_scope, scope, open_paren, '%s%s' % (equation, value))
            equation = '%s%s' % (equation, value)
        look_forward = self.next_char(token.line, token.end[1])

        if look_forward in self.equation_ops:
            if(look_forward == ')' and open_paren-1 > 0):
                pass
            else:
                next_tok = next(self.tokens)
                equation = self.process_equation(next_tok, local_scope, scope, open_paren, equation)
        return equation

    def process_variable(self, token, local_scope, scope):
        l, pos = token.end
        next_pos, next_char = self.next_char(token.line, pos, True)

        if next_char == '.':
            # Access variable scope
            token = copy.deepcopy(token) #Copy the token because when you generate new ones it changes the ref.
            target = self.get_in_scope(token.string, local_scope, scope)
            new_token = self.token_after_op()
            local_scope[scope + 1] = {attr: value for attr, value in inspect.getmembers(target) if not attr.startswith('_')}
            var = self.get_in_scope(new_token.string, local_scope, scope + 1)

            if not var:
                logger.debug("Unset variable with dot operator, %s", new_token.string)
                logger.debug(token)
                logger.debug(new_token)
                return None
            if not local_scope[scope + 1]:
                logger.debug("dot operator on var with no members, %s", token.string)
                logger.debug(token)
                logger.debug(new_token)
                return None
            value = self.process_variable(new_token, local_scope, scope + 1)
            del local_scope[scope + 1]
            return value

        elif next_char == '(':
            # Access callable variable
            args = []
            value = None
            token = copy.deepcopy(token)
            target = self.get_in_scope(token.string, local_scope, scope)
            for itoken in self.tokens:
                if itoken.type == tokenize.NAME:
                    value = self.process_variable(itoken, local_scope, scope - 1)
                elif itoken.type == tokenize.NUMBER:
                    value = int(itoken.string)
                elif itoken.type == tokenize.STRING:
                    value = itoken.string[1:-1]
                elif itoken.type == tokenize.OP:
                    if itoken.string == ',':
                        args.append(copy.deepcopy(value))
                        value = None
                    if itoken.string == ')':
                        args.append(copy.deepcopy(value))
                        return target(*args)

        elif next_char == '=' and self.next_char(token.line, next_pos) != '=':
            # Assignment
            token = copy.deepcopy(token)
            next(self.tokens)  #skip the op
            value = None
            for itoken in self.tokens:
                look_forward = self.next_char(itoken.line, itoken.end[1])
                if look_forward in self.equation_ops or itoken.string in self.equation_ops:
                    value = self.process_equation(itoken, local_scope, scope)
                    value = ast.literal_eval(value)
                elif itoken.type == tokenize.NAME:
                    value = self.process_variable(itoken, local_scope, scope)
                elif itoken.type == tokenize.NUMBER:
                    value = int(itoken.string)
                elif itoken.type == tokenize.STRING:
                    value = itoken.string[1:-1]
                elif itoken.type == tokenize.NEWLINE:
                    break

            var = self.get_in_scope(token.string, local_scope, scope)
            if not var:
                # New assignment
                local_scope[scope].update({token.string: value})
            else:
                local_scope[scope][token.string] = value
            return value
        if token.string == "not":
            token = next(self.tokens)
            value = self.process_variable(token, local_scope, scope)
            return not value
        # not a callable
        value = self.get_in_scope(token.string, local_scope, scope)
        if not value:
            logger.debug("Error, value referenced before assignment. %s", token.string)
            logger.debug(token)
        return value

    def process_token(self, token, local_scope, scope, exec_types):
        if token.type in exec_types:
            if token.type == tokenize.NAME and token.string not in self.process_tokens:
                self.process_variable(token, local_scope, scope)
                return True
            proc = self.process_tokens.get(token.string, None)
            if proc:
                proc(token, local_scope, scope)
        elif token.type == tokenize.INDENT:
            if len(token.string) % 4:
                logger.debug("Invalid indent")
                logger.debug(token)
                return False
            set_scope = len(token.string) // 4
            if set_scope not in local_scope:
                logger.debug("Invalid indent. None existent.")
                logger.debug(token)
                return False
        elif token.type == tokenize.DEDENT:
            self.decrease_scope(local_scope)
        return True

    def execute(self, actor, victim, argument, audience):
        logger.debug("Executing script.")
        exec_start = time.time()
        self.tokenize()
        local_scope = {0: {'actor': actor, 'victim': victim, 'argument': argument}}
        self.current_scope = 0
        exec_types = [tokenize.NAME, tokenize.OP, tokenize.NEWLINE]
        try:
            for token in self.tokens:
                now = time.time()
                # logger.debug('Time difference is: %0.3fms', (now - exec_start) * 1000.0)
                if (now - exec_start) * 1000.0 > 200.0:
                    logger.error('Maximum PyProg execution time exceeded')
                    raise TimeoutError
                self.process_token(token, local_scope, 0, exec_types)
        except:
            actor.send("Something went wrong.")
        exec_stop = time.time()
        logger.debug("Script took % 0.3fms", (exec_stop-exec_start) * 1000.0)

test_prog = """if actor.perm_hit > 20:
    if actor.perm_hit > 30:
        actor.do_say("I'm pretty much god.")
    else:
        actor.do_say("I'm a beast!")
else:
    actor.do_say("I'm a wimp!")
if actor.guild.name == 'mage':
    actor.do_say("I'm a mage tho, so don't mess with me.")
elif actor.guild.name == 'thief':
    actor.do_say("I'm a thief, hold your wallet!")
else:
    actor.do_say("I'm not sure what I am.")
if not actor.act.is_set(PLR_CANLOOT):
    actor.do_say("And I can't loot!")
for vict in char_list:
    actor.do_say(vict.name)
"""
register_prog('say', Progs(test_prog))
