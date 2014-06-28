from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_DETECT_EVIL, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, TAR_CHAR_SELF, \
    POS_STANDING


def spell_detect_evil(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_DETECT_EVIL):
        if victim == ch:
            ch.send("You can already sense evil.\n")
        else:
            act("$N can already detect evil.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = APPLY_NONE
    af.bitvector = AFF_DETECT_EVIL
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


register_spell(skill_type("detect evil",
                          {'mage': 11, 'cleric': 4, 'thief': 12, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_evil, TAR_CHAR_SELF, POS_STANDING, None,
                          SLOT(18), 5, 12, "", "The red in your vision disappears.", ""))