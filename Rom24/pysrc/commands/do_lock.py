import logging

logger = logging.getLogger()

from handler_room import find_door, has_key
from interp import cmd_type, register_command
from merc import read_word, ITEM_PORTAL, IS_SET, EX_ISDOOR, EX_NOCLOSE, EX_CLOSED, EX_NOLOCK, EX_LOCKED, SET_BIT, act, \
    TO_CHAR, TO_ROOM, ITEM_CONTAINER, CONT_CLOSED, CONT_LOCKED, rev_dir, POS_RESTING, LOG_NORMAL


def do_lock(ch, argument):
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Lock what?\n")
        return
    obj = ch.get_obj_here(arg)
    if obj:
        # portal stuff
        if obj.item_type == ITEM_PORTAL:
            if not IS_SET(obj.value[1], EX_ISDOOR) or IS_SET(obj.value[1], EX_NOCLOSE):
                ch.send("You can't do that.\n")
                return
            if not IS_SET(obj.value[1], EX_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[4] < 0 or IS_SET(obj.value[1], EX_NOLOCK):
                ch.send("It can't be locked.\n")
                return
            if not has_key(ch, obj.value[4]):
                ch.send("You lack the key.\n")
                return
            if IS_SET(obj.value[1], EX_LOCKED):
                ch.send("It's already locked.\n")
                return
            SET_BIT(obj.value[1], EX_LOCKED)
            act("You lock $p.", ch, obj, None, TO_CHAR)
            act("$n locks $p.", ch, obj, None, TO_ROOM)
            return
        # 'lock object'
        if obj.item_type != ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not IS_SET(obj.value[1], CONT_CLOSED):
            ch.send("It's not closed.\n")
            return
        if obj.value[2] < 0:
            ch.send("It can't be locked.\n")
            return
        if not has_key(ch, obj.value[2]):
            ch.send("You lack the key.\n")
            return
        if IS_SET(obj.value[1], CONT_LOCKED):
            ch.send("It's already locked.\n")
            return

        SET_BIT(obj.value[1], CONT_LOCKED)
        act("You lock $p.", ch, obj, None, TO_CHAR)
        act("$n locks $p.", ch, obj, None, TO_ROOM)
        return
    door = find_door(ch, arg)
    if door >= 0:
        # 'lock door'
        pexit = ch.in_room.exit[door]
        if not IS_SET(pexit.exit_info, EX_CLOSED):
            ch.send("It's not closed.\n")
            return
        if pexit.key < 0:
            ch.send("It can't be locked.\n")
            return
        if not has_key(ch, pexit.key):
            ch.send("You lack the key.\n")
            return
        if IS_SET(pexit.exit_info, EX_LOCKED):
            ch.send("It's already locked.\n")
            return

        SET_BIT(pexit.exit_info, EX_LOCKED)
        ch.send("*Click*\n")
        act("$n locks the $d.", ch, None, pexit.keyword, TO_ROOM)
        # lock the other side
        to_room = pexit.to_room
        if to_room and to_room.exit[rev_dir[door]] != 0 \
                and to_room.exit[rev_dir[door]].to_room == ch.in_room:
            SET_BIT(to_room.exit[rev_dir[door]].exit_info, EX_LOCKED)


register_command(cmd_type('lock', do_lock, POS_RESTING, 0, LOG_NORMAL, 1))
