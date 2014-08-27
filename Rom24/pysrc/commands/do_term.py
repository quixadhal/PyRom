import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import miniboa


def usage(ch):
    ch.send('Usage: term [[ttype]] [[cols N]] [[rows N]]\n')
    ch.send('       valid ttypes are %s.\n\n' % ', '.join(miniboa.TERMINAL_TYPES))


def do_term(ch, argument):
    if not argument:
        ch.send('Terminal Type is %s (%d columns, %d rows)\n' % (ch.desc.terminal_type, ch.desc.columns, ch.desc.rows))
        return
    else:
        args = argument.split()
        expect_rows = False
        expect_cols = False
        got_type = False
        changed = False
        for a in args:
            if a.lower() == 'help':
                usage(ch)
                return
            if a.lower() == 'rows':
                expect_rows = True
                continue
            elif a.lower() == 'columns' or a.lower() == 'cols':
                expect_cols = True
                continue
            elif a.isnumeric():
                if expect_rows:
                    ch.desc.rows = game_utils.to_integer(a)
                    expect_rows = False
                    changed = True
                elif expect_cols:
                    ch.desc.columns = game_utils.to_integer(a)
                    expect_cols = False
                    changed = True
                else:
                    ch.send('Invalid argument: %s\n\n' % a)
                    usage(ch)
                    return
            elif not got_type and a.lower() in miniboa.TERMINAL_TYPES:
                ch.desc.terminal_type = a.lower()
                got_type = True
                changed = True
            else:
                ch.send('Invalid argument: %s\n\n' % a)
                usage(ch)
                return
        if changed:
            ch.send('Terminal Type set to %s (%d columns, %d rows)\n' % (ch.desc.terminal_type, ch.desc.columns, ch.desc.rows))


interp.register_command(interp.cmd_type('term', do_term, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
