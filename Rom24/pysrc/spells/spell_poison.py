import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_poison(sn, level, ch, victim, target):
    if target == merc.TARGET_ITEM:
        obj = victim

        if obj.item_type == merc.ITEM_FOOD or obj.item_type == merc.ITEM_DRINK_CON:
            if obj.flags.bless or obj.flags.burn_proof:
                handler_game.act("Your spell fails to corrupt $p.", ch, obj, None, merc.TO_CHAR)
                return
            obj.value[3] = 1
            handler_game.act("$p is infused with poisonous vapors.", ch, obj, None, merc.TO_ALL)
            return
        if obj.item_type == merc.ITEM_WEAPON:
            if state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_FLAMING) \
                    or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_FROST) \
                    or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_VAMPIRIC) \
                    or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_SHARP) \
                    or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_VORPAL) \
                    or state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_SHOCKING) \
                    or obj.flags.bless \
                    or obj.flags.burn_proof:
                handler_game.act("You can't seem to envenom $p.", ch, obj, None, merc.TO_CHAR)
                return
            if state_checks.IS_WEAPON_STAT(obj, merc.WEAPON_POISON):
                handler_game.act("$p is already envenomed.", ch, obj, None, merc.TO_CHAR)
                return
            af = handler_game.AFFECT_DATA()
            af.where = merc.TO_WEAPON
            af.type = sn
            af.level = level // 2
            af.duration = level // 8
            af.location = 0
            af.modifier = 0
            af.bitvector = merc.WEAPON_POISON
            obj.affect_add(af)
            handler_game.act("$p is coated with deadly venom.", ch, obj, None, merc.TO_ALL)
            return
        handler_game.act("You can't poison $p.", ch, obj, None, merc.TO_CHAR)
        return

    if handler_magic.saves_spell(level, victim, merc.DAM_POISON):
        handler_game.act("$n turns slightly green, but it passes.", victim, None, None, merc.TO_ROOM)
        victim.send("You feel momentarily ill, but it passes.\n")
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = merc.APPLY_STR
    af.modifier = -2
    af.bitvector = merc.AFF_POISON
    victim.affect_join(af)
    victim.send("You feel very sick.\n")
    handler_game.act("$n looks very ill.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("poison",
                          {'mage': 17, 'cleric': 12, 'thief': 15, 'warrior': 21},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_poison, merc.TAR_OBJ_CHAR_OFF, merc.POS_FIGHTING, None,
                          const.SLOT(33), 10, 12, "poison", "You feel less sick.",
                          "The poison on $p dries up."))
