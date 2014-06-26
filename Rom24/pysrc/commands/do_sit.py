from interp import cmd_type
from merc import POS_FIGHTING, ITEM_FURNITURE, IS_SET, SIT_ON, SIT_IN, SIT_AT, act, TO_CHAR, POS_DEAD, POS_SLEEPING, \
    IS_AFFECTED, AFF_SLEEP, TO_ROOM, POS_SITTING, POS_RESTING, POS_STANDING, LOG_NORMAL


def do_sit(ch, argument):
    obj = None
    if ch.position == POS_FIGHTING:
        ch.send("Maybe you should finish this fight first?\n")
        return
    # okay, now that we know we can sit, find an object to sit on */
    if argument:
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if obj == None:
            ch.send("You don't see that here.\n")
            return
        else:
            obj = ch.on

        if obj:
            if obj.item_type != ITEM_FURNITURE or (
                    not IS_SET(obj.value[2], SIT_ON)
                    and not IS_SET(obj.value[2], SIT_IN)
                    and not IS_SET(obj.value[2], SIT_AT)):
                ch.send("You can't sit on that.\n")
                return
            if ch.on != obj and obj.count_users() >= obj.value[0]:
                act("There's no more room on $p.", ch, obj, None, TO_CHAR, POS_DEAD)
                return
            ch.on = obj

    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch, AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return

        if obj is None:
            ch.send("You wake and sit up.\n")
            act("$n wakes and sits up.", ch, None, None, TO_ROOM)
        elif IS_SET(obj.value[2], SIT_AT):
            act("You wake and sit at $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and sits at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act("You wake and sit on $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and sits at $p.", ch, obj, None, TO_ROOM)
        else:
            act("You wake and sit in $p.", ch, obj, None, TO_CHAR, POS_DEAD)
            act("$n wakes and sits in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_SITTING
        return
    elif ch.position == POS_RESTING:
        if obj is None:
            ch.send("You stop resting.\n")
        elif IS_SET(obj.value[2], SIT_AT):
            act("You sit at $p.", ch, obj, None, TO_CHAR)
            act("$n sits at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act("You sit on $p.", ch, obj, None, TO_CHAR)
            act("$n sits on $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_SITTING
        return
    elif ch.position == POS_SITTING:
        ch.send("You are already sitting down.\n")
        return
    elif ch.position == POS_STANDING:
        if obj is None:
            ch.send("You sit down.\n")
            act("$n sits down on the ground.", ch, None, None, TO_ROOM)
        elif IS_SET(obj.value[2], SIT_AT):
            act("You sit down at $p.", ch, obj, None, TO_CHAR)
            act("$n sits down at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], SIT_ON):
            act("You sit on $p.", ch, obj, None, TO_CHAR)
            act("$n sits on $p.", ch, obj, None, TO_ROOM)
        else:
            act("You sit down in $p.", ch, obj, None, TO_CHAR)
            act("$n sits down in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_SITTING


cmd_type('sit', do_sit, POS_SLEEPING, 0, LOG_NORMAL, 1)
