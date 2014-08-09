import logging


logger = logging.getLogger()

import random

import interp
import merc
import const
import game_utils
import handler_game
import handler_room
import state_checks


def do_pick(self, argument):
    ch = self
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Pick what?\n")
        return

    state_checks.WAIT_STATE(ch, const.skill_table["pick lock"].beats)

    # look for guards
    for gch in ch.in_room.people:
        if state_checks.IS_NPC(gch) and state_checks.IS_AWAKE(gch) and ch.level + 5 < gch.level:
            handler_game.act("$N is standing too close to the lock.", ch, None, gch, merc.TO_CHAR)
            return
        if not ch.is_npc() and random.randint(1, 99) > ch.get_skill("pick lock"):
            ch.send("You failed.\n")
            if ch.is_pc():
                ch.check_improve( "pick lock", False, 2)
            return
        obj = ch.get_item_here(arg)
        if obj:
            # portal stuff
            if obj.item_type == merc.ITEM_PORTAL:
                if not state_checks.IS_SET(obj.value[1], merc.EX_ISDOOR):
                    ch.send("You can't do that.\n")
                    return
                if not state_checks.IS_SET(obj.value[1], merc.EX_CLOSED):
                    ch.send("It's not closed.\n")
                    return
                if obj.value[4] < 0:
                    ch.send("It can't be unlocked.\n")
                    return
                if state_checks.IS_SET(obj.value[1], merc.EX_PICKPROOF):
                    ch.send("You failed.\n")
                    return
                state_checks.REMOVE_BIT(obj.value[1], merc.EX_LOCKED)
                handler_game.act("You pick the lock on $p.", ch, obj, None, merc.TO_CHAR)
                handler_game.act("$n picks the lock on $p.", ch, obj, None, merc.TO_ROOM)
                if ch.is_pc():
                    ch.check_improve( "pick lock", True, 2)
                return


                # 'pick object'
            if obj.item_type != merc.ITEM_CONTAINER:
                ch.send("That's not a container.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[2] < 0:
                ch.send("It can't be unlocked.\n")
                return
            if not state_checks.IS_SET(obj.value[1], merc.CONT_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if state_checks.IS_SET(obj.value[1], merc.CONT_PICKPROOF):
                ch.send("You failed.\n")
                return

            state_checks.REMOVE_BIT(obj.value[1], merc.CONT_LOCKED)
            handler_game.act("You pick the lock on $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n picks the lock on $p.", ch, obj, None, merc.TO_ROOM)
            if ch.is_pc():
                ch.check_improve( "pick lock", True, 2)
            return
        door = handler_room.find_door(ch, arg)
        if door >= 0:
            # 'pick door'
            pexit = ch.in_room.exit[door]
            if not state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED) and not ch.is_immortal():
                ch.send("It's not closed.\n")
                return
            if pexit.key < 0 and not ch.is_immortal():
                ch.send("It can't be picked.\n")
                return
            if not state_checks.IS_SET(pexit.exit_info, merc.EX_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if state_checks.IS_SET(pexit.exit_info, merc.EX_PICKPROOF) and not ch.is_immortal():
                ch.send("You failed.\n")
                return
            state_checks.REMOVE_BIT(pexit.exit_info, merc.EX_LOCKED)
            ch.send("*Click*\n")
            handler_game.act("$n picks the $d.", ch, None, pexit.keyword, merc.TO_ROOM)
            if ch.is_pc():
                ch.check_improve( "pick_lock", True, 2)

            # unlock the other side
            to_room = pexit.to_room
            if to_room and to_room.exit[merc.rev_dir[door]] != 0 \
                    and to_room.exit[merc.rev_dir[door]].to_room == ch.in_room:
                state_checks.REMOVE_BIT(to_room.exit[merc.rev_dir[door]].exit_info, merc.EX_LOCKED)


interp.register_command(interp.cmd_type('pick', do_pick, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
