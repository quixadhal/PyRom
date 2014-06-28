from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_DETECT_INVIS, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, POS_STANDING, \
    TAR_CHAR_SELF


def spell_detect_invis(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_DETECT_INVIS):
        if victim == ch:
            ch.send("You can already see invisible.\n")
        else:
            act("$N can already see invisible things.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = APPLY_NONE
    af.bitvector = AFF_DETECT_INVIS
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


register_spell(skill_type("detect invis",
                          {'mage': 3, 'cleric': 8, 'thief': 6, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_invis, TAR_CHAR_SELF, POS_STANDING,
                          None, SLOT(19), 5, 12, "", "You no longer see invisible objects.", ""))