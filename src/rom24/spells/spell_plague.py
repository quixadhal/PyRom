import const
import handler_game
import handler_magic
import merc


def spell_plague(sn, level, ch, victim, target):
    # RT plague spell, very nasty */
    if handler_magic.saves_spell(level, victim, merc.DAM_DISEASE) or (
        victim.is_npc() and victim.act.is_set(merc.ACT_UNDEAD)):
        if ch == victim:
            ch.send("You feel momentarily ill, but it passes.\n")
        else:
            handler_game.act("$N seems to be unaffected.", ch, None, victim, merc.TO_CHAR)
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level * 3 // 4
    af.duration = level
    af.location = merc.APPLY_STR
    af.modifier = -5
    af.bitvector = merc.AFF_PLAGUE
    victim.affect_join(af)

    victim.send("You scream in agony as plague sores erupt from your skin.\n")
    handler_game.act("$n screams in agony as plague sores erupt from $s skin.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("plague",
                          {'mage': 23, 'cleric': 17, 'thief': 36, 'warrior': 26},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_plague, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(503), 20, 12, "sickness", "Your sores vanish.", ""))
