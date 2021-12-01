import random
import const
import fight
import game_utils
import handler_magic
import merc
import update


def spell_energy_drain(sn, level, ch, victim, target):
    # Drain XP, MANA, HP.
    # Caster gains HP.
    if victim != ch:
        ch.alignment = max(-1000, ch.alignment - 50)

    if handler_magic.saves_spell(level, victim, merc.DAM_NEGATIVE):
        victim.send("You feel a momentary chill.\n")
        return
    if victim.level <= 2:
        dam = ch.hit + 1
    else:
        update.gain_exp(victim, 0 - random.randint(level // 2, 3 * level // 2))
        victim.mana //= 2
        victim.move //= 2
        dam = game_utils.dice(1, level)
        ch.hit += dam

    victim.send("You feel your life slipping away! \n")
    ch.send("Wow....what a rush! \n")
    fight.damage(ch, victim, dam, sn, merc.DAM_NEGATIVE, True)


const.register_spell(const.skill_type("energy drain",
                          {'mage': 19, 'cleric': 22, 'thief': 26, 'warrior': 23},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_energy_drain, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(25), 35, 12, "energy drain", "!Energy Drain!", ""))
