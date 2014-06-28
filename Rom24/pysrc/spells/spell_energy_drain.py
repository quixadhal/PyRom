import random

from const import SLOT, skill_type, register_spell
from fight import damage
from merc import saves_spell, DAM_NEGATIVE, dice, POS_FIGHTING, TAR_CHAR_OFFENSIVE
from update import gain_exp


def spell_energy_drain(sn, level, ch, victim, target):
    # Drain XP, MANA, HP.
    # Caster gains HP.
    if victim != ch:
        ch.alignment = max(-1000, ch.alignment - 50)

    if saves_spell(level, victim, DAM_NEGATIVE):
        victim.send("You feel a momentary chill.\n")
        return
    if victim.level <= 2:
        dam = ch.hit + 1
    else:
        gain_exp(victim, 0 - random.randint(level // 2, 3 * level // 2))
        victim.mana //= 2
        victim.move //= 2
        dam = dice(1, level)
        ch.hit += dam

    victim.send("You feel your life slipping away! \n")
    ch.send("Wow....what a rush! \n")
    damage(ch, victim, dam, sn, DAM_NEGATIVE, True)


register_spell(skill_type("energy drain",
                          {'mage': 19, 'cleric': 22, 'thief': 26, 'warrior': 23},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_energy_drain, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(25), 35, 12, "energy drain", "!Energy Drain!", ""))