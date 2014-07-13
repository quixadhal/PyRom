import logging

logger = logging.getLogger()

import interp
import merc
import state_checks


def do_sleep(ch, argument):
    obj = None
    if ch.position == merc.POS_SLEEPING:
        ch.send("You are already sleeping.\n")
        return
    elif ch.position == merc.POS_RESTING \
            or ch.position == merc.POS_SITTING \
            or ch.position == merc.POS_STANDING:
        if not argument and not ch.on:
            ch.send("You go to sleep.\n")
            act("$n goes to sleep.", ch, None, None, merc.TO_ROOM)
            ch.position = merc.POS_SLEEPING
        else:  # find an object and sleep on it
            if not argument:
                obj = ch.on
            else:
                obj = ch.get_item_list(argument, merc.rooms[ch.in_room].contents)

            if obj is None:
                ch.send("You don't see that here.\n")
                return
            if obj.item_type != merc.ITEM_FURNITURE or (
                            not state_checks.IS_SET(obj.value[2], merc.SLEEP_ON)
                        and not state_checks.IS_SET(obj.value[2], merc.SLEEP_IN)
                    and not state_checks.IS_SET(obj.value[2], merc.SLEEP_AT)):
                ch.send("You can't sleep on that!\n")
                return
            if ch.on != obj and obj.count_users() >= obj.value[0]:
                act("There is no room on $p for you.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
                return
            ch.on = obj
            if state_checks.IS_SET(obj.value[2], merc.SLEEP_AT):
                act("You go to sleep at $p.", ch, obj, None, merc.TO_CHAR)
                act("$n goes to sleep at $p.", ch, obj, None, merc.TO_ROOM)
            elif state_checks.IS_SET(obj.value[2], merc.SLEEP_ON):
                act("You go to sleep on $p.", ch, obj, None, merc.TO_CHAR)
                act("$n goes to sleep on $p.", ch, obj, None, merc.TO_ROOM)
            else:
                act("You go to sleep in $p.", ch, obj, None, merc.TO_CHAR)
                act("$n goes to sleep in $p.", ch, obj, None, merc.TO_ROOM)
            ch.position = merc.POS_SLEEPING
        return
    elif ch.position == merc.POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return


interp.register_command(interp.cmd_type('sleep', do_sleep, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
