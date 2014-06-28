from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_INFRARED, act, TO_CHAR, TO_ROOM, AFFECT_DATA, TO_AFFECTS, APPLY_NONE, POS_STANDING, \
    TAR_CHAR_DEFENSIVE


def spell_infravision(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_INFRARED):
        if victim == ch:
            ch.send("You can already see in the dark.\n")
        else:
            act("$N already has infravision.\n", ch, None, victim, TO_CHAR)
        return

    act("$n's eyes glow red.\n", ch, None, None, TO_ROOM)
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_INFRARED
    victim.affect_add(af)
    victim.send("Your eyes glow red.\n")
    return


register_spell(skill_type("infravision",
                          {'mage': 9, 'cleric': 13, 'thief': 10, 'warrior': 16},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_infravision, TAR_CHAR_DEFENSIVE, POS_STANDING,
                          None, SLOT(77), 5, 18, "", "You no longer see in the dark.", ""))