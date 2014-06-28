import random

from const import SLOT, skill_type, register_spell
from effects import shock_effect
from fight import damage
from merc import act, TO_NOTVICT, TO_VICT, TO_CHAR, dice, saves_spell, DAM_LIGHTNING, TARGET_CHAR, POS_FIGHTING, \
    TAR_CHAR_OFFENSIVE


def spell_lightning_breath(sn, level, ch, victim, target):
    act("$n breathes a bolt of lightning at $N.", ch, None, victim, TO_NOTVICT)
    act("$n breathes a bolt of lightning at you! ", ch, None, victim, TO_VICT)
    act("You breathe a bolt of lightning at $N.", ch, None, victim, TO_CHAR)

    hpch = max(10, ch.hit)
    hp_dam = random.randint(hpch // 9 + 1, hpch // 5)
    dice_dam = dice(level, 20)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)

    if saves_spell(level, victim, DAM_LIGHTNING):
        shock_effect(victim, level // 2, dam // 4, TARGET_CHAR)
        damage(ch, victim, dam // 2, sn, DAM_LIGHTNING, True)
    else:
        shock_effect(victim, level, dam, TARGET_CHAR)
        damage(ch, victim, dam, sn, DAM_LIGHTNING, True)

        #
        # * Spells for mega1.are from Glop//Erkenbrand.


register_spell(skill_type("lightning breath",
                          {'mage': 37, 'cleric': 40, 'thief': 43, 'warrior': 46},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_lightning_breath, TAR_CHAR_OFFENSIVE, POS_FIGHTING, None,
                          SLOT(204), 150, 24, "blast of lightning", "!Lightning Breath!", ""))
# * Spells for mega1.are from Glop/Erkenbrand. */)