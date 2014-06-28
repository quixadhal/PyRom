import logging

logger = logging.getLogger()

from interp import cmd_type, register_command
from merc import POS_FIGHTING, ITEM_FURNITURE, IS_SET, STAND_AT, STAND_ON, STAND_IN, TO_CHAR, POS_DEAD, POS_SLEEPING, \
    IS_AFFECTED, AFF_SLEEP, act, TO_ROOM, POS_STANDING, POS_RESTING, POS_SITTING, LOG_NORMAL


def do_stand(ch, argument):
    obj = None
    if argument:
        if ch.position == POS_FIGHTING:
            ch.send("Maybe you should finish fighting first?\n")
            return
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        if obj.item_type != ITEM_FURNITURE or (
                        not IS_SET(obj.value[2], STAND_AT) and not IS_SET(obj.value[2], STAND_ON)
                and not IS_SET(obj.value[2], STAND_IN)):
            ch.send("You can't seem to find a place to stand.\n")
            return
        if ch.on != obj and obj.count_users() >= obj.value[0]:
            act("There's no room to stand on $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            return
        ch.on = obj

    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch, AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake and stand up.\n")
            act("$n wakes and stands up.", ch, None, None, TO_ROOM)
            ch.on = None
        elif IS_SET(obj.value[2], STAND_AT):
            act("You wake and stand at $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and stands at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], STAND_ON):
            act("You wake and stand on $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and stands on $p.", ch, obj, None, TO_ROOM)
        else:
            act("You wake and stand in $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and stands in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_STANDING
        ch.do_look("auto")
        return
    elif ch.position == POS_RESTING or ch.position == POS_SITTING:
        if not obj:
            ch.send("You stand up.\n")
            act("$n stands up.", ch, None, None, TO_ROOM)
            ch.on = None
        elif IS_SET(obj.value[2], STAND_AT):
            act("You stand at $p.", ch, obj, None, TO_CHAR)
            act("$n stands at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], STAND_ON):
            act("You stand on $p.", ch, obj, None, TO_CHAR)
            act("$n stands on $p.", ch, obj, None, TO_ROOM)
        else:
            act("You stand in $p.", ch, obj, None, TO_CHAR)
            act("$n stands on $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_STANDING
        return
    elif ch.position == POS_STANDING:
        ch.send("You are already standing.\n")
        return
    elif ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return


register_command(cmd_type('stand', do_stand, POS_SLEEPING, 0, LOG_NORMAL, 1))
