import logging

logger = logging.getLogger(__name__)

from rom24 import interp
from rom24 import merc
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_room
from rom24 import state_checks
from rom24 import instance


def do_open(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Open what?\n")
        return

    item = ch.get_item_here(arg)
    if item:
        # open portal
        if item.item_type == merc.ITEM_PORTAL:
            if not state_checks.IS_SET(item.value[1], merc.EX_ISDOOR):
                ch.send("You can't do that.\n")
                return
            if not state_checks.IS_SET(item.value[1], merc.EX_CLOSED):
                ch.send("It's already open.\n")
                return
            if state_checks.IS_SET(item.value[1], merc.EX_LOCKED):
                ch.send("It's locked.\n")
                return
            item.value[1] = state_checks.REMOVE_BIT(item.value[1], merc.EX_CLOSED)
            handler_game.act("You open $p.", ch, item, None, merc.TO_CHAR)
            handler_game.act("$n opens $p.", ch, item, None, merc.TO_ROOM)
            return
            # 'open object'
        if item.item_type != merc.ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not state_checks.IS_SET(item.value[1], merc.CONT_CLOSED):
            ch.send("It's already open.\n")
            return
        if not state_checks.IS_SET(item.value[1], merc.CONT_CLOSEABLE):
            ch.send("You can't do that.\n")
            return
        if state_checks.IS_SET(item.value[1], merc.CONT_LOCKED):
            ch.send("It's locked.\n")
            return
        item.value[1] = state_checks.REMOVE_BIT(item.value[1], merc.CONT_CLOSED)
        handler_game.act("You open $p.", ch, item, None, merc.TO_CHAR)
        handler_game.act("$n opens $p.", ch, item, None, merc.TO_ROOM)
        return

    door = handler_room.find_door(ch, arg)
    if door >= 0:
        # 'open door'
        pexit = ch.in_room.exit[door]
        if not pexit.exit_info.is_set(merc.EX_CLOSED):
            ch.send("It's already open.\n")
            return
        if pexit.exit_info.is_set(merc.EX_LOCKED):
            ch.send("It's locked.\n")
            return
        pexit.exit_info.rem_bit(merc.EX_CLOSED)
        handler_game.act("$n opens the $d.", ch, None, pexit.keyword, merc.TO_ROOM)
        ch.send("Ok.\n")

        # open the other side
        to_room = instance.rooms[pexit.to_room]
        pexit_rev = to_room.exit[merc.rev_dir[door]] if pexit.to_room else None
        if to_room and pexit_rev and pexit_rev.to_room == ch.in_room.instance_id:
            pexit_rev.exit_info.rem_bit(merc.EX_CLOSED)
            for rch_id in to_room.people[:]:
                rch = instance.characters[rch_id]
                handler_game.act(
                    "The $d opens.", rch, None, pexit_rev.keyword, merc.TO_CHAR
                )


interp.register_command(
    interp.cmd_type("open", do_open, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
