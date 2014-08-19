import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_curse(sn, level, ch, victim, target):
    # deal with the object case first */
    if target == merc.TARGET_ITEM:
        obj = victim
        if obj.flags.evil:
            handler_game.act("$p is already filled with evil.", ch, obj, None, merc.TO_CHAR)
            return

        if obj.flags.bless:
            paf = state_checks.affect_find(obj.affected, const.skill_table["bless"])
            if not handler_magic.saves_dispel(level, paf.level if paf is not None else obj.level, 0):
                if paf:
                    obj.affect_remove(paf)
                handler_game.act("$p glows with a red aura.", ch, obj, None, merc.TO_ALL)
                state_checks.REMOVE_BIT(obj.extra_flags, merc.ITEM_BLESS)
                return
            else:
                handler_game.act("The holy aura of $p is too powerful for you to overcome.", ch, obj, None,
                                 merc.TO_CHAR)
                return
        af = handler_game.AFFECT_DATA()
        af.where = merc.TO_OBJECT
        af.type = sn
        af.level = level
        af.duration = 2 * level
        af.location = merc.APPLY_SAVES
        af.modifier = +1
        af.bitvector = merc.ITEM_EVIL
        obj.affect_add(af)

        handler_game.act("$p glows with a malevolent aura.", ch, obj, None, merc.TO_ALL)

        if obj.wear_loc != merc.WEAR_NONE:
            ch.saving_throw += 1
        return

    # character curses */
    if victim.is_affected( merc.AFF_CURSE) or handler_magic.saves_spell(level, victim, merc.DAM_NEGATIVE):
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = merc.APPLY_HITROLL
    af.modifier = -1 * (level // 8)
    af.bitvector = merc.AFF_CURSE
    victim.affect_add(af)

    af.location = merc.APPLY_SAVING_SPELL
    af.modifier = level // 8
    victim.affect_add(af)

    victim.send("You feel unclean.\n")
    if ch != victim:
        handler_game.act("$N looks very uncomfortable.", ch, None, victim, merc.TO_CHAR)


const.register_spell(const.skill_type("curse",
                          {'mage': 18, 'cleric': 18, 'thief': 26, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_curse, merc.TAR_OBJ_CHAR_OFF, merc.POS_FIGHTING, None,
                          const.SLOT(17), 20, 12, "curse", "The curse wears off.", "$p is no longer impure."))
