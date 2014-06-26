from handler_room import find_door
from interp import cmd_table, cmd_type
from merc import read_word, ITEM_PORTAL, IS_SET, EX_ISDOOR, EX_NOCLOSE, EX_CLOSED, SET_BIT, act, TO_CHAR, TO_ROOM, \
    ITEM_CONTAINER, CONT_CLOSED, CONT_CLOSEABLE, rev_dir, POS_RESTING, LOG_NORMAL


def do_close(ch, argument):
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Close what?\n")
        return

    obj = ch.get_obj_here(arg)
    if obj:
        # portal stuff */
        if obj.item_type == ITEM_PORTAL:
            if not IS_SET(obj.value[1], EX_ISDOOR) or IS_SET(obj.value[1], EX_NOCLOSE):
                ch.send("You can't do that.\n")
                return
            if IS_SET(obj.value[1], EX_CLOSED):
                ch.send("It's already closed.\n")
                return
            SET_BIT(obj.value[1], EX_CLOSED)
            act("You close $p.", ch, obj, None, TO_CHAR)
            act("$n closes $p.", ch, obj, None, TO_ROOM)
            return
        # 'close object' */
        if obj.item_type != ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if IS_SET(obj.value[1], CONT_CLOSED):
            ch.send("It's already closed.\n")
            return
        if not IS_SET(obj.value[1], CONT_CLOSEABLE):
            ch.send("You can't do that.\n")
            return
        SET_BIT(obj.value[1], CONT_CLOSED)
        act("You close $p.", ch, obj, None, TO_CHAR)
        act("$n closes $p.", ch, obj, None, TO_ROOM)
        return
    door = find_door(ch, arg)
    if find_door(ch, arg) >= 0:
        # 'close door' */
        pexit = ch.in_room.exit[door]
        if IS_SET(pexit.exit_info, EX_CLOSED):
            ch.send("It's already closed.\n")
            return
        SET_BIT(pexit.exit_info, EX_CLOSED)
        act("$n closes the $d.", ch, None, pexit.keyword, TO_ROOM)
        ch.send("Ok.\n")

        # close the other side */
        to_room = pexit.to_room
        pexit_rev = to_room.exit[rev_dir[door]] if pexit.to_room else None
        if to_room and pexit_rev and pexit_rev.to_room == ch.in_room:
            SET_BIT(pexit_rev.exit_info, EX_CLOSED)
            for rch in to_room.people:
                act("The $d closes.", rch, None, pexit_rev.keyword, TO_CHAR)


cmd_table['close'] = cmd_type('close', do_close, POS_RESTING, 0, LOG_NORMAL, 1)
