import logging

logger = logging.getLogger()

import interp
import merc
import game_utils
import handler_game
import handler_room
import state_checks


def do_open(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Open what?\n")
        return

    obj = ch.get_item_here(arg)
    if obj:
        # open portal
        if obj.item_type == merc.ITEM_PORTAL:
            if not state_checks.IS_SET(obj.value[1], merc.EX_ISDOOR):
                ch.send("You can't do that.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.EX_CLOSED):
                ch.send("It's already open.\n")
                return
            if state_checks.IS_SET(obj.value[1], merc.EX_LOCKED):
                ch.send("It's locked.\n")
                return
            state_checks.REMOVE_BIT(obj.value[1], merc.EX_CLOSED)
            handler_game.act("You open $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n opens $p.", ch, obj, None, merc.TO_ROOM)
            return
            # 'open object'
        if obj.item_type != merc.ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
            ch.send("It's already open.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSEABLE):
            ch.send("You can't do that.\n")
            return
        if state_checks.IS_SET(obj.value[1], merc.CONT_LOCKED):
            ch.send("It's locked.\n")
            return
        state_checks.REMOVE_BIT(obj.value[1], merc.CONT_CLOSED)
        handler_game.act("You open $p.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$n opens $p.", ch, obj, None, merc.TO_ROOM)
        return

    door = handler_room.find_door(ch, arg)
    if door >= 0:
        # 'open door'
        pexit = ch.in_room.exit[door]
        if not state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED):
            ch.send("It's already open.\n")
            return
        if state_checks.IS_SET(pexit.exit_info, merc.EX_LOCKED):
            ch.send("It's locked.\n")
            return
        state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_CLOSED)
        handler_game.act("$n opens the $d.", ch, None, pexit.keyword, merc.TO_ROOM)
        ch.send("Ok.\n")

        # open the other side
        to_room = pexit.to_room
        if to_room and to_room.exit[merc.rev_dir[door]] and to_room.exit[merc.rev_dir[door]].to_room == ch.in_room:
            pexit_rev = to_room.exit[merc.rev_dir[door]]
            state_checks.REMOVE_BIT(pexit_rev.exit_info, merc.EX_CLOSED)
            for rch in to_room.people:
                handler_game.act("The $d opens.", rch, None, pexit_rev.keyword, merc.TO_CHAR)


interp.register_command(interp.cmd_type('open', do_open, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
