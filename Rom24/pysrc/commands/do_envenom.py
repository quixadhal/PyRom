import merc
import interp
import const
import skills


# for poisoning weapons and food/drink */
def do_envenom(ch, argument):
    # find out what */
    if not argument:
        ch.send("Envenom what item?\n")
        return
    obj = ch.get_obj_list(argument, ch.carrying)
    if not obj:
        ch.send("You don't have that item.\n")
        return
    skill = ch.get_skill('envenom')
    if skill < 1:
        ch.send("Are you crazy? You'd poison yourself!\n")
        return
    if obj.item_type == merc.ITEM_FOOD or obj.item_type == merc.ITEM_DRINK_CON:
        if merc.IS_OBJ_STAT(obj, merc.ITEM_BLESS) or merc.IS_OBJ_STAT(obj, merc.ITEM_BURN_PROOF):
            merc.act("You fail to poison $p.", ch, obj, None, merc.TO_CHAR)
            return
        if random.randint(1,99) < skill:  # success! */
            merc.act("$n treats $p with deadly poison.", ch, obj, None, merc.TO_ROOM)
            merc.act("You treat $p with deadly poison.", ch, obj, None, merc.TO_CHAR)
            if not obj.value[3]:
                obj.value[3] = 1
                skills.check_improve(ch, "envenom", True, 4)
            merc.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
        merc.act("You fail to poison $p.", ch, obj, None, merc.TO_CHAR)
        if not obj.value[3]:
            skills.check_improve(ch, "envenom", False, 4)
            WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
    if obj.item_type == merc.ITEM_WEAPON:
        if merc.IS_WEAPON_STAT(obj, merc.WEAPON_FLAMING) \
        or merc.IS_WEAPON_STAT(obj, merc.WEAPON_FROST) \
        or merc.IS_WEAPON_STAT(obj, merc.WEAPON_VAMPIRIC) \
        or merc.IS_WEAPON_STAT(obj, merc.WEAPON_SHARP) \
        or merc.IS_WEAPON_STAT(obj, merc.WEAPON_VORPAL) \
        or merc.IS_WEAPON_STAT(obj, merc.WEAPON_SHOCKING) \
        or merc.IS_OBJ_STAT(obj, merc.ITEM_BLESS) or merc.IS_OBJ_STAT(obj, merc.ITEM_BURN_PROOF):
            merc.act("You can't seem to envenom $p.", ch, obj, None, merc.TO_CHAR)
            return
        if obj.value[3] < 0 or const.attack_table[obj.value[3]].damage == merc.DAM_BASH:
            ch.send("You can only envenom edged weapons.\n")
            return
        if merc.IS_WEAPON_STAT(obj, merc.WEAPON_POISON):
            merc.act("$p is already envenomed.", ch, obj, None, merc.TO_CHAR)
            return
        percent = random.randint(1,99)
        if percent < skill:
            af = merc.AFFECT_DATA()
            af.where = merc.TO_WEAPON
            af.type = "poison"
            af.level = ch.level * percent // 100
            af.duration = ch.level // 2 * percent // 100
            af.location = 0
            af.modifier = 0
            af.bitvector = merc.WEAPON_POISON
            obj.affect_add(af)

            merc.act("$n coats $p with deadly venom.", ch, obj, None, merc.TO_ROOM)
            merc.act("You coat $p with venom.", ch, obj, None, merc.TO_CHAR)
            skills.check_improve(ch, "envenom", True, 3)
            merc.WAIT_STATE(ch, const.skill_table["envenom"].beats)
            return
        else:
            merc.act("You fail to envenom $p.", ch, obj, None, merc.TO_CHAR)
            skills.check_improve(ch,"envenom",False,3)
            merc.WAIT_STATE(ch,const.skill_table["envenom"].beats)
            return
    merc.act("You can't poison $p.", ch, obj, None, merc.TO_CHAR)
    return

interp.cmd_table['envenom'] = interp.cmd_type('envenom', do_envenom, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)