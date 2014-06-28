from const import SLOT, skill_type
from merc import saves_spell, DAM_DISEASE, IS_NPC, IS_SET, ACT_UNDEAD, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_STR, \
    AFF_PLAGUE, TO_ROOM, POS_FIGHTING, TAR_CHAR_OFFENSIVE


def spell_plague(sn, level, ch, victim, target):
    # RT plague spell, very nasty */
    if saves_spell(level, victim, DAM_DISEASE) or (IS_NPC(victim) and IS_SET(victim.act, ACT_UNDEAD)):
        if ch == victim:
            ch.send("You feel momentarily ill, but it passes.\n")
        else:
            act("$N seems to be unaffected.", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level * 3 // 4
    af.duration = level
    af.location = APPLY_STR
    af.modifier = -5
    af.bitvector = AFF_PLAGUE
    victim.affect_join(af)

    victim.send("You scream in agony as plague sores erupt from your skin.\n")
    act("$n screams in agony as plague sores erupt from $s skin.", victim, None, None, TO_ROOM)

skill_type("plague",
           { 'mage':23, 'cleric':17, 'thief':36, 'warrior':26 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_plague, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
           SLOT(503), 20, 12, "sickness", "Your sores vanish.", "")