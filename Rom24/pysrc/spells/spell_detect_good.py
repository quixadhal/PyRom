from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_DETECT_GOOD, act, TO_CHAR, TO_AFFECTS, APPLY_NONE, TAR_CHAR_SELF, POS_STANDING


def spell_detect_good(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_DETECT_GOOD):
        if victim == ch:
            ch.send("You can already sense good.\n")
        else:
            act("$N can already detect good.", ch, None, victim, TO_CHAR)
        return
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = APPLY_NONE
    af.bitvector = AFF_DETECT_GOOD
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


skill_type("detect good",
           {'mage': 11, 'cleric': 4, 'thief': 12, 'warrior': 53},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_detect_good, TAR_CHAR_SELF, POS_STANDING, None,
           SLOT(513), 5, 12, "", "The gold in your vision disappears.", "")