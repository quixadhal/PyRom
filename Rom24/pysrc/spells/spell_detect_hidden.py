from const import SLOT, skill_type
from merc import IS_AFFECTED, AFF_DETECT_HIDDEN, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, TAR_CHAR_SELF, \
    POS_STANDING


def spell_detect_hidden(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_DETECT_HIDDEN):
        if victim == ch:
            ch.send("You are already as alert as you can be. \n")
        else:
            act("$N can already sense hidden lifeforms.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_DETECT_HIDDEN
    victim.affect_add(af)
    victim.send("Your awareness improves.\n")
    if ch != victim:
        ch.send("Ok.\n")

skill_type("detect hidden",
           { 'mage':15, 'cleric':11, 'thief':12, 'warrior':53 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_detect_hidden, TAR_CHAR_SELF, POS_STANDING, None,
           SLOT(44), 5, 12, "", "You feel less aware of your surroundings.", "")