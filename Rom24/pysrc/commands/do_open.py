from act_move import find_door
from interp import cmd_table, cmd_type
from merc import read_word, ITEM_PORTAL, IS_SET, EX_ISDOOR, EX_CLOSED, EX_LOCKED, REMOVE_BIT, act, TO_CHAR, TO_ROOM, \
    ITEM_CONTAINER, CONT_CLOSED, CONT_CLOSEABLE, CONT_LOCKED, rev_dir, POS_RESTING, LOG_NORMAL


def do_open(ch, argument):
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Open what?\n")
        return

    obj = ch.get_obj_here(arg)
    if obj:
        # open portal */
        if obj.item_type == ITEM_PORTAL:
            if not IS_SET(obj.value[1], EX_ISDOOR):
                ch.send("You can't do that.\n")
                return
            if not IS_SET(obj.value[1], EX_CLOSED):
                ch.send("It's already open.\n")
                return
            if IS_SET(obj.value[1], EX_LOCKED):
                ch.send("It's locked.\n")
                return
            REMOVE_BIT(obj.value[1], EX_CLOSED)
            act("You open $p.", ch, obj, None, TO_CHAR)
            act("$n opens $p.", ch, obj, None, TO_ROOM)
            return
            # 'open object' */
        if obj.item_type != ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not IS_SET(obj.value[1], CONT_CLOSED):
            ch.send("It's already open.\n")
            return
        if not IS_SET(obj.value[1], CONT_CLOSEABLE):
            ch.send("You can't do that.\n")
            return
        if IS_SET(obj.value[1], CONT_LOCKED):
            ch.send("It's locked.\n")
            return
        REMOVE_BIT(obj.value[1], CONT_CLOSED)
        act("You open $p.", ch, obj, None, TO_CHAR)
        act("$n opens $p.", ch, obj, None, TO_ROOM)
        return

    door = find_door(ch, arg)
    if door >= 0:
        # 'open door' */
        pexit = ch.in_room.exit[door]
        if not IS_SET(pexit.exit_info, EX_CLOSED):
            ch.send("It's already open.\n")
            return
        if IS_SET(pexit.exit_info, EX_LOCKED):
            ch.send("It's locked.\n")
            return
        REMOVE_BIT(pexit.exit_info, EX_CLOSED)
        act("$n opens the $d.", ch, None, pexit.keyword, TO_ROOM)
        ch.send("Ok.\n")

        # open the other side */
        to_room = pexit.to_room
        if to_room and to_room.exit[rev_dir[door]] and to_room.exit[rev_dir[door]].to_room == ch.in_room:
            pexit_rev = to_room.exit[rev_dir[door]]
            REMOVE_BIT(pexit_rev.exit_info, EX_CLOSED)
            for rch in to_room.people:
                act("The $d opens.", rch, None, pexit_rev.keyword, TO_CHAR)


cmd_table['open'] = cmd_type('open', do_open, POS_RESTING, 0, LOG_NORMAL, 1)
