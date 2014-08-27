import logging

logger = logging.getLogger()

import handler_game
import interp
import merc
import state_checks

def do_sit(ch, argument):
    obj = None
    if ch.position == merc.POS_FIGHTING:
        ch.send("Maybe you should finish this fight first?\n")
        return
    # okay, now that we know we can sit, find an object to sit on
    if argument:
        obj = ch.get_item_list(argument, ch.in_room.items)
        if obj is None:
            ch.send("You don't see that here.\n")
            return
        else:
            obj = ch.on

        if obj:
            if obj.item_type != merc.ITEM_FURNITURE or (
                    not state_checks.IS_SET(obj.value[2], merc.SIT_ON)
                    and not state_checks.IS_SET(obj.value[2], merc.SIT_IN)
                    and not state_checks.IS_SET(obj.value[2], merc.SIT_AT)):
                ch.send("You can't sit on that.\n")
                return
            if ch.on != obj and obj.count_users() >= obj.value[0]:
                handler_game.act("There's no more room on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
                return
            ch.on = obj

    if ch.position == merc.POS_SLEEPING:
        if ch.is_affected(merc.AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return

        if obj is None:
            ch.send("You wake and sit up.\n")
            handler_game.act("$n wakes and sits up.", ch, None, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.SIT_AT):
            handler_game.act("You wake and sit at $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and sits at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.SIT_ON):
            handler_game.act("You wake and sit on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and sits at $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You wake and sit in $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and sits in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_SITTING
        return
    elif ch.position == merc.POS_RESTING:
        if obj is None:
            ch.send("You stop resting.\n")
        elif state_checks.IS_SET(obj.value[2], merc.SIT_AT):
            handler_game.act("You sit at $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.SIT_ON):
            handler_game.act("You sit on $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits on $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_SITTING
        return
    elif ch.position == merc.POS_SITTING:
        ch.send("You are already sitting down.\n")
        return
    elif ch.position == merc.POS_STANDING:
        if obj is None:
            ch.send("You sit down.\n")
            handler_game.act("$n sits down on the ground.", ch, None, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.SIT_AT):
            handler_game.act("You sit down at $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits down at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.SIT_ON):
            handler_game.act("You sit on $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits on $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You sit down in $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits down in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_SITTING


interp.register_command(interp.cmd_type('sit', do_sit, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
