from merc import is_affected, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, APPLY_AC, TAR_CHAR_DEFENSIVE, POS_STANDING
from const import skill_type, SLOT


def spell_armor(sn, level, ch, victim, target):
    if is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already armored.\n")
        else:
            act("$N is already armored.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 24
    af.modifier = -20
    af.location = APPLY_AC
    af.bitvector = 0
    victim.affect_add(af)
    victim.send("You feel someone protecting you.\n")
    if ch is not victim:
        act("$N is protected by your magic.", ch, None, victim, TO_CHAR)


skill_type("armor",
           {'mage': 7, 'cleric': 2, 'thief': 10, 'warrior': 5},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_armor, TAR_CHAR_DEFENSIVE, POS_STANDING,
           None, SLOT(1), 5, 12, "", "You feel less armored.", "")