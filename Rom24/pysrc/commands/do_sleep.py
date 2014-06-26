from interp import cmd_table, cmd_type
from merc import POS_SLEEPING, POS_RESTING, POS_SITTING, POS_STANDING, act, TO_ROOM, ITEM_FURNITURE, IS_SET, SLEEP_ON, \
    SLEEP_IN, SLEEP_AT, TO_CHAR, POS_DEAD, POS_FIGHTING, LOG_NORMAL


def do_sleep(ch, argument):
    obj = None
    if ch.position == POS_SLEEPING:
        ch.send("You are already sleeping.\n")
        return
    elif ch.position == POS_RESTING \
            or ch.position == POS_SITTING \
            or ch.position == POS_STANDING:
        if not argument and not ch.on:
            ch.send("You go to sleep.\n")
            act("$n goes to sleep.", ch, None, None, TO_ROOM)
            ch.position = POS_SLEEPING
        else:  # find an object and sleep on it */
            if not argument:
                obj = ch.on
            else:
                obj = ch.get_obj_list(argument, ch.in_room.contents)

            if obj is None:
                ch.send("You don't see that here.\n")
                return
            if obj.item_type != ITEM_FURNITURE or (
                    not IS_SET(obj.value[2], SLEEP_ON)
                    and not IS_SET(obj.value[2], SLEEP_IN)
                    and not IS_SET(obj.value[2], SLEEP_AT)):
                ch.send("You can't sleep on that!\n")
                return
            if ch.on != obj and obj.count_users() >= obj.value[0]:
                act("There is no room on $p for you.", ch, obj, None, TO_CHAR, POS_DEAD)
                return
            ch.on = obj
            if IS_SET(obj.value[2], SLEEP_AT):
                act("You go to sleep at $p.", ch, obj, None, TO_CHAR)
                act("$n goes to sleep at $p.", ch, obj, None, TO_ROOM)
            elif IS_SET(obj.value[2], SLEEP_ON):
                act("You go to sleep on $p.", ch, obj, None, TO_CHAR)
                act("$n goes to sleep on $p.", ch, obj, None, TO_ROOM)
            else:
                act("You go to sleep in $p.", ch, obj, None, TO_CHAR)
                act("$n goes to sleep in $p.", ch, obj, None, TO_ROOM)
            ch.position = POS_SLEEPING
        return
    elif ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return


cmd_table['sleep'] = cmd_type('sleep', do_sleep, POS_SLEEPING, 0, LOG_NORMAL, 1)
