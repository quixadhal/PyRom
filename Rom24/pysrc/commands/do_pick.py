import random
import const
from handler_room import find_door
from interp import cmd_table, cmd_type
from merc import read_word, WAIT_STATE, IS_NPC, IS_AWAKE, act, TO_CHAR, ITEM_PORTAL, IS_SET, EX_ISDOOR, EX_CLOSED, \
    EX_PICKPROOF, REMOVE_BIT, EX_LOCKED, TO_ROOM, ITEM_CONTAINER, CONT_CLOSED, CONT_LOCKED, CONT_PICKPROOF, IS_IMMORTAL, \
    rev_dir, POS_RESTING, LOG_NORMAL
from skills import check_improve


def do_pick(self, argument):
    ch = self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Pick what?\n")
        return

    WAIT_STATE(ch, const.skill_table["pick lock"].beats)

    # look for guards */
    for gch in ch.in_room.people:
        if IS_NPC(gch) and IS_AWAKE(gch) and ch.level + 5 < gch.level:
            act("$N is standing too close to the lock.", ch, None, gch, TO_CHAR)
            return
        if not IS_NPC(ch) and random.randint(1, 99) > ch.get_skill("pick lock"):
            ch.send("You failed.\n")
            check_improve(ch, "pick lock", False, 2)
            return
        obj = ch.get_obj_here(arg)
        if obj:
            # portal stuff */
            if obj.item_type == ITEM_PORTAL:
                if not IS_SET(obj.value[1], EX_ISDOOR):
                    ch.send("You can't do that.\n")
                    return
                if not IS_SET(obj.value[1], EX_CLOSED):
                    ch.send("It's not closed.\n")
                    return
                if obj.value[4] < 0:
                    ch.send("It can't be unlocked.\n")
                    return
                if IS_SET(obj.value[1], EX_PICKPROOF):
                    ch.send("You failed.\n")
                    return
                REMOVE_BIT(obj.value[1], EX_LOCKED)
                act("You pick the lock on $p.", ch, obj, None, TO_CHAR)
                act("$n picks the lock on $p.", ch, obj, None, TO_ROOM)
                check_improve(ch, "pick lock", True, 2)
                return


                # 'pick object' */
            if obj.item_type != ITEM_CONTAINER:
                ch.send("That's not a container.\n")
                return
            if not IS_SET(obj.value[1], CONT_CLOSED):
                ch.send("It's not closed.\n")
                return
            if obj.value[2] < 0:
                ch.send("It can't be unlocked.\n")
                return
            if not IS_SET(obj.value[1], CONT_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if IS_SET(obj.value[1], CONT_PICKPROOF):
                ch.send("You failed.\n")
                return

            REMOVE_BIT(obj.value[1], CONT_LOCKED)
            act("You pick the lock on $p.", ch, obj, None, TO_CHAR)
            act("$n picks the lock on $p.", ch, obj, None, TO_ROOM)
            check_improve(ch, "pick lock", True, 2)
            return
        door = find_door(ch, arg)
        if door >= 0:
            # 'pick door' */
            pexit = ch.in_room.exit[door]
            if not IS_SET(pexit.exit_info, EX_CLOSED) and not IS_IMMORTAL(ch):
                ch.send("It's not closed.\n")
                return
            if pexit.key < 0 and not IS_IMMORTAL(ch):
                ch.send("It can't be picked.\n")
                return
            if not IS_SET(pexit.exit_info, EX_LOCKED):
                ch.send("It's already unlocked.\n")
                return
            if IS_SET(pexit.exit_info, EX_PICKPROOF) and not IS_IMMORTAL(ch):
                ch.send("You failed.\n")
                return
            REMOVE_BIT(pexit.exit_info, EX_LOCKED)
            ch.send("*Click*\n")
            act("$n picks the $d.", ch, None, pexit.keyword, TO_ROOM)
            check_improve(ch, "pick_lock", True, 2)

            # unlock the other side */
            to_room = pexit.to_room
            if to_room and to_room.exit[rev_dir[door]] != 0 \
                    and to_room.exit[rev_dir[door]].to_room == ch.in_room:
                REMOVE_BIT(to_room.exit[rev_dir[door]].exit_info, EX_LOCKED)


cmd_table['pick'] = cmd_type('pick', do_pick, POS_RESTING, 0, LOG_NORMAL, 1)
