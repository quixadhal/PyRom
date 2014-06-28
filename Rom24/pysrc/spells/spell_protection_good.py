from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_PROTECT_GOOD, AFF_PROTECT_EVIL, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, \
    APPLY_SAVING_SPELL, POS_STANDING, TAR_CHAR_SELF


def spell_protection_good(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_PROTECT_GOOD) or IS_AFFECTED(victim, AFF_PROTECT_EVIL):
        if victim == ch:
            ch.send("You are already protected.\n")
        else:
            act("$N is already protected.", ch, None, victim, TO_CHAR)
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 24
    af.location = APPLY_SAVING_SPELL
    af.modifier = -1
    af.bitvector = AFF_PROTECT_GOOD
    victim.affect_add(af)
    victim.send("You feel aligned with darkness.\n")
    if ch != victim:
        act("$N is protected from good.", ch, None, victim, TO_CHAR)


register_spell(skill_type("protection good",
                          {'mage': 12, 'cleric': 9, 'thief': 17, 'warrior': 11},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_protection_good, TAR_CHAR_SELF, POS_STANDING,
                          None, SLOT(514), 5, 12, "", "You feel less protected.", ""))