import logging

logger = logging.getLogger()

import handler_game
import interp
import merc
import state_checks


def do_rest(self, argument):
    ch = self
    obj = None
    if ch.position == merc.POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return
        # okay, now that we know we can rest, find an object to rest on
    if argument:
        obj = ch.get_item_list(argument, ch.in_room.items)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        else:
            obj = ch.on

        if obj:
            if obj.item_type != merc.ITEM_FURNITURE \
                    or (not state_checks.IS_SET(obj.value[2], merc.REST_ON)
                        and not state_checks.IS_SET(obj.value[2], merc.REST_IN)
                        and not state_checks.IS_SET(obj.value[2], merc.REST_AT)):
                ch.send("You can't rest on that.\n")
                return
            if obj and ch.on != obj and obj.count_users() >= obj.value[0]:
                handler_game.act("There's no more room on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
                return
            ch.on = obj

    if ch.position == merc.POS_SLEEPING:
        if ch.is_affected(merc.AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake up and start resting.\n")
            handler_game.act("$n wakes up and starts resting.", ch, None, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_AT):
            handler_game.act("You wake up and rest at $p.", ch, obj, None, merc.TO_CHAR, merc.POS_SLEEPING)
            handler_game.act("$n wakes up and rests at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_ON):
            handler_game.act("You wake up and rest on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_SLEEPING)
            handler_game.act("$n wakes up and rests on $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You wake up and rest in $p.", ch, obj, None, merc.TO_CHAR, merc.POS_SLEEPING)
            handler_game.act("$n wakes up and rests in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_RESTING
        return
    elif ch.position == merc.POS_RESTING:
        ch.send("You are already resting.\n")
        return
    elif ch.position == merc.POS_STANDING:
        if obj is None:
            ch.send("You rest.\n")
            handler_game.act("$n sits down and rests.", ch, None, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_AT):
            handler_game.act("You sit down at $p and rest.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits down at $p and rests.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_ON):
            handler_game.act("You sit on $p and rest.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n sits on $p and rests.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You rest in $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n rests in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_RESTING
        return
    elif ch.position == merc.POS_SITTING:
        if not obj:
            ch.send("You rest.\n")
            handler_game.act("$n rests.", ch, None, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_AT):
            handler_game.act("You rest at $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n rests at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.REST_ON):
            handler_game.act("You rest on $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n rests on $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You rest in $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n rests in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_RESTING
        return


interp.register_command(interp.cmd_type('rest', do_rest, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
