from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_PROTECT_EVIL, AFF_PROTECT_GOOD, act, TO_CHAR, AFFECT_DATA, TO_AFFECTS, \
    APPLY_SAVING_SPELL, TAR_CHAR_SELF, POS_STANDING


def spell_protection_evil(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_PROTECT_EVIL) or IS_AFFECTED(victim, AFF_PROTECT_GOOD):
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
    af.bitvector = AFF_PROTECT_EVIL
    victim.affect_add(af)
    victim.send("You feel holy and pure.\n")
    if ch != victim:
        act("$N is protected from evil.", ch, None, victim, TO_CHAR)


register_spell(skill_type("protection evil",
                          {'mage': 12, 'cleric': 9, 'thief': 17, 'warrior': 11},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_protection_evil, TAR_CHAR_SELF, POS_STANDING,
                          None, SLOT(34), 5, 12, "", "You feel less protected.", ""))