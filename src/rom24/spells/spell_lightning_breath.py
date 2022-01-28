import random

from rom24 import const
from rom24 import effects
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc


def spell_lightning_breath(sn, level, ch, victim, target):
    handler_game.act(
        "$n breathes a bolt of lightning at $N.", ch, None, victim, merc.TO_NOTVICT
    )
    handler_game.act(
        "$n breathes a bolt of lightning at you! ", ch, None, victim, merc.TO_VICT
    )
    handler_game.act(
        "You breathe a bolt of lightning at $N.", ch, None, victim, merc.TO_CHAR
    )

    hpch = max(10, ch.hit)
    hp_dam = random.randint(hpch // 9 + 1, hpch // 5)
    dice_dam = game_utils.dice(level, 20)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)

    if handler_magic.saves_spell(level, victim, merc.DAM_LIGHTNING):
        effects.shock_effect(victim, level // 2, dam // 4, merc.TARGET_CHAR)
        fight.damage(ch, victim, dam // 2, sn, merc.DAM_LIGHTNING, True)
    else:
        effects.shock_effect(victim, level, dam, merc.TARGET_CHAR)
        fight.damage(ch, victim, dam, sn, merc.DAM_LIGHTNING, True)

        #
        # * Spells for mega1.are from Glop//Erkenbrand.


const.register_spell(
    const.skill_type(
        "lightning breath",
        {"mage": 37, "cleric": 40, "thief": 43, "warrior": 46},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_lightning_breath,
        merc.TAR_CHAR_OFFENSIVE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(204),
        150,
        24,
        "blast of lightning",
        "!Lightning Breath!",
        "",
    )
)
# * Spells for mega1.are from Glop/Erkenbrand. */)
