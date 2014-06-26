from interp import cmd_type
from merc import POS_FIGHTING, ITEM_FURNITURE, IS_SET, REST_ON, REST_IN, REST_AT, act, TO_CHAR, POS_DEAD, POS_SLEEPING, \
    IS_AFFECTED, AFF_SLEEP, TO_ROOM, POS_RESTING, POS_STANDING, POS_SITTING, LOG_NORMAL


def do_rest(self, argument):
    ch = self
    obj = None
    if ch.position == POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return
        # okay, now that we know we can rest, find an object to rest on */
    if argument:
        obj = ch.get_obj_list(argument, ch.in_room.contents)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        else:
            obj = ch.on

        if obj:
            if obj.item_type != ITEM_FURNITURE or (
                    not IS_SET(obj.value[2], REST_ON) and not IS_SET(obj.value[2], REST_IN)
                    and not IS_SET(obj.value[2], REST_AT)):
                ch.send("You can't rest on that.\n")
                return
            if obj and ch.on != obj and obj.count_users() >= obj.value[0]:
                act("There's no more room on $p.", ch, obj, None, TO_CHAR, POS_DEAD)
                return
            ch.on = obj

    if ch.position == POS_SLEEPING:
        if IS_AFFECTED(ch, AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake up and start resting.\n")
            act("$n wakes up and starts resting.", ch, None, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_AT):
            act("You wake up and rest at $p.", ch, obj, None, TO_CHAR, POS_SLEEPING)
            act("$n wakes up and rests at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_ON):
            act("You wake up and rest on $p.", ch, obj, None, TO_CHAR, POS_SLEEPING)
            act("$n wakes up and rests on $p.", ch, obj, None, TO_ROOM)
        else:
            act("You wake up and rest in $p.", ch, obj, None, TO_CHAR, POS_SLEEPING)
            act("$n wakes up and rests in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_RESTING
        return
    elif ch.position == POS_RESTING:
        ch.send("You are already resting.\n")
        return
    elif ch.position == POS_STANDING:
        if obj == None:
            ch.send("You rest.\n")
            act("$n sits down and rests.", ch, None, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_AT):
            act("You sit down at $p and rest.", ch, obj, None, TO_CHAR)
            act("$n sits down at $p and rests.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_ON):
            act("You sit on $p and rest.", ch, obj, None, TO_CHAR)
            act("$n sits on $p and rests.", ch, obj, None, TO_ROOM)
        else:
            act("You rest in $p.", ch, obj, None, TO_CHAR)
            act("$n rests in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_RESTING
        return
    elif ch.position == POS_SITTING:
        if not obj:
            ch.send("You rest.\n")
            act("$n rests.", ch, None, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_AT):
            act("You rest at $p.", ch, obj, None, TO_CHAR)
            act("$n rests at $p.", ch, obj, None, TO_ROOM)
        elif IS_SET(obj.value[2], REST_ON):
            act("You rest on $p.", ch, obj, None, TO_CHAR)
            act("$n rests on $p.", ch, obj, None, TO_ROOM)
        else:
            act("You rest in $p.", ch, obj, None, TO_CHAR)
            act("$n rests in $p.", ch, obj, None, TO_ROOM)
        ch.position = POS_RESTING
        return


cmd_type('rest', do_rest, POS_SLEEPING, 0, LOG_NORMAL, 1)
