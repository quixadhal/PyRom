import random
from fight import stop_fighting
from interp import cmd_type
from merc import IS_NPC, IS_SET, ACT_PET, act, TO_ROOM, room_index_hash, ROOM_VNUM_TEMPLE, ROOM_NO_RECALL, IS_AFFECTED, \
    AFF_CURSE, WAIT_STATE, POS_FIGHTING, LOG_NORMAL
from skills import check_improve
from update import gain_exp


def do_recall(ch, argument):
    if IS_NPC(ch) and not IS_SET(ch.act, ACT_PET):
        ch.send("Only players can recall.\n")
        return
    act("$n prays for transportation!", ch, 0, 0, TO_ROOM)
    location = room_index_hash[ROOM_VNUM_TEMPLE]
    if not location:
        ch.send("You are completely lost.\n")
        return
    if ch.in_room == location:
        return
    if IS_SET(ch.in_room.room_flags, ROOM_NO_RECALL) or IS_AFFECTED(ch, AFF_CURSE):
        ch.send("Mota has forsaken you.\n")
        return
    victim = ch.fighting
    if victim:
        skill = ch.get_skill("recall")
        if random.randint(1, 99) < 80 * skill / 100:
            check_improve(ch, "recall", False, 6)
            WAIT_STATE(ch, 4)
            ch.send("You failed!.\n")
            return
        lose = 25 if ch.desc else 50
        gain_exp(ch, 0 - lose)
        check_improve(ch, "recall", True, 4)
        ch.send("You recall from combat!  You lose %d exps.\n" % lose)
        stop_fighting(ch, True)
    ch.move /= 2
    act("$n disappears.", ch, None, None, TO_ROOM)
    ch.from_room()
    ch.to_room(location)
    act("$n appears in the room.", ch, None, None, TO_ROOM)
    ch.do_look("auto")

    if ch.pet is not None:
        ch.pet.do_recall("")
    return


cmd_type('recall', do_recall, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_type("/", do_recall, POS_FIGHTING, 0, LOG_NORMAL, 0)
