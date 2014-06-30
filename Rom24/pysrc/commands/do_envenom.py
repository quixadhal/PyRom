import logging

logger = logging.getLogger()

import random
import merc
import interp
import const
import skills
import handler_game
import state_checks


# for poisoning weapons and food/drink
def do_envenom(ch, argument):
    # find out what
    if not argument:
        ch.send("Envenom what item?\n")
        return
    obj = ch.get_obj_list(argument, ch.contents)
    if not obj:
        ch.send("You don't have that item.\n")
        return
    skill = ch.get_skill('envenom')
    if skill < 1:
        ch.send("Are you crazy? You'd poison yourself!\n")
        return
    if obj.item_type == merc.ITEM_FOOD or obj.item_type == merc.ITEM_DRINK_CON:
        if state_checks.IS_OBJ_STAT(obj, merc.ITEM_BLESS) or state_checks.IS_OBJ_STAT(obj, merc.ITEM_BURN_PROOF):
            handler_game.act("You fail to poison $p.", ch, obj, None, merc.TO_CHAR)
            return
        if random.randint(1, 99) < skill:  # success!
            handler_game.act("$n treats $p with deadly poison.", ch, obj, None, merc.TO_ROOM)
            handler_game.act("You treat $p with deadly poison.", ch, obj, None, merc.TO_CHAR)
            if not obj.value[3]:
                obj.value[3] = 1
                ch.check_improve( "envenom", True, 4)
            state_checks.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
        handler_game.act("You fail to poison $p.", ch, obj, None, merc.TO_CHAR)
        if not obj.value[3]:
            ch.check_improve( "envenom", False, 4)
            state_checks.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
    if obj.item_type == merc.ITEM_WEAPON:
        if state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_FLAMING) \
                or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_FROST) \
                or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_VAMPIRIC) \
                or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_SHARP) \
                or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_VORPAL) \
                or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_SHOCKING) \
                or state_checks.IS_OBJ_STAT(obj, merc.ITEM_BLESS) or state_checks.IS_OBJ_STAT(obj, merc.ITEM_BURN_PROOF):
            handler_game.act("You can't seem to envenom $p.", ch, obj, None, merc.TO_CHAR)
            return
        if obj.value[3] < 0 or const.attack_table[obj.value[3]].damage == merc.DAM_BASH:
            ch.send("You can only envenom edged weapons.\n")
            return
        if state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_POISON):
            handler_game.act("$p is already envenomed.", ch, obj, None, merc.TO_CHAR)
            return
        percent = random.randint(1, 99)
        if percent < skill:
            af = handler_game.AFFECT_DATA()
            af.where = merc.TO_WEAPON
            af.type = "poison"
            af.level = ch.level * percent // 100
            af.duration = ch.level // 2 * percent // 100
            af.location = 0
            af.modifier = 0
            af.bitvector = merc.WEAPON_POISON
            obj.affect_add(af)

            handler_game.act("$n coats $p with deadly venom.", ch, obj, None, merc.TO_ROOM)
            handler_game.act("You coat $p with venom.", ch, obj, None, merc.TO_CHAR)
            ch.check_improve( "envenom", True, 3)
            state_checks.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
        else:
            handler_game.act("You fail to envenom $p.", ch, obj, None, merc.TO_CHAR)
            ch.check_improve( "envenom", False, 3)
            state_checks.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
    handler_game.act("You can't poison $p.", ch, obj, None, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('envenom', do_envenom, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
