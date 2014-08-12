import logging

logger = logging.getLogger()

import game_utils
import handler_game
import handler_room
import interp
import merc
import state_checks


def do_lock(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Lock what?\n")
        return
    obj = ch.get_item_here(arg)
    if obj:
        # portal stuff
        if obj.item_type == merc.ITEM_PORTAL:
            if not state_checks.IS_SET(obj.value[1], merc.EX_ISDOOR) or state_checks.IS_SET(obj.value[1],
                                                                                            merc.EX_NOCLOSE):
                ch.send("You can't do that.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.EX_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[4] < 0 or state_checks.IS_SET(obj.value[1], merc.EX_NOLOCK):
                ch.send("It can't be locked.\n")
                return
            if not ch.has_key(obj.value[4]):
                ch.send("You lack the key.\n")
                return
            if state_checks.IS_SET(obj.value[1], merc.EX_LOCKED):
                ch.send("It's already locked.\n")
                return
            state_checks.SET_BIT(obj.value[1], merc.EX_LOCKED)
            handler_game.act("You lock $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n locks $p.", ch, obj, None, merc.TO_ROOM)
            return
        # 'lock object'
        if obj.item_type != merc.ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
            ch.send("It's not closed.\n")
            return
        if obj.value[2] < 0:
            ch.send("It can't be locked.\n")
            return
        if not ch.has_key(obj.value[2]):
            ch.send("You lack the key.\n")
            return
        if state_checks.IS_SET(obj.value[1], merc.CONT_LOCKED):
            ch.send("It's already locked.\n")
            return

        state_checks.SET_BIT(obj.value[1], merc.CONT_LOCKED)
        handler_game.act("You lock $p.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$n locks $p.", ch, obj, None, merc.TO_ROOM)
        return
    door = handler_room.find_door(ch, arg)
    if door >= 0:
        # 'lock door'
        pexit = ch.in_room.exit[door]
        if not pexit.exit_info.is_set(merc.EX_CLOSED):
            ch.send("It's not closed.\n")
            return
        if pexit.key < 0:
            ch.send("It can't be locked.\n")
            return
        if not ch.has_key(pexit.key):
            ch.send("You lack the key.\n")
            return
        if pexit.exit_info.is_set(merc.EX_LOCKED):
            ch.send("It's already locked.\n")
            return

        pexit.exit_info.set_bit(merc.EX_LOCKED)
        ch.send("*Click*\n")
        handler_game.act("$n locks the $d.", ch, None, pexit.keyword, merc.TO_ROOM)
        # lock the other side
        to_room = pexit.to_room
        if to_room and to_room.exit[merc.rev_dir[door]] != 0 \
                and to_room.exit[merc.rev_dir[door]].to_room == ch.in_room:
            to_room.exit[merc.rev_dir[door]].exit_info.set_bit(merc.EX_LOCKED)


interp.register_command(interp.cmd_type('lock', do_lock, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
