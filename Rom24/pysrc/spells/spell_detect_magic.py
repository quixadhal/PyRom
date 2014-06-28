from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_DETECT_MAGIC, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, POS_STANDING, \
    TAR_CHAR_SELF


def spell_detect_magic(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_DETECT_MAGIC):
        if victim == ch:
            ch.send("You can already sense magical auras.\n")
        else:
            act("$N can already detect magic.", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = APPLY_NONE
    af.bitvector = AFF_DETECT_MAGIC
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")

skill_type("detect magic",
           { 'mage':2, 'cleric':6, 'thief':5, 'warrior':53 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_detect_magic, TAR_CHAR_SELF, POS_STANDING, None,
           SLOT(20), 5, 12, "", "The detect magic wears off.", "")