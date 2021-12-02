import random

from rom24 import const
from rom24 import effects
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc


def spell_gas_breath(sn, level, ch, victim, target):
    handler_game.act(
        "$n breathes out a cloud of poisonous gas! ", ch, None, None, merc.TO_ROOM
    )
    handler_game.act(
        "You breath out a cloud of poisonous gas.", ch, None, None, merc.TO_CHAR
    )

    hpch = max(16, ch.hit)
    hp_dam = random.randint(hpch // 15 + 1, 8)
    dice_dam = game_utils.dice(level, 12)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    effects.poison_effect(ch.in_room, level, dam, merc.TARGET_ROOM)

    for vch_id in ch.in_room.people:

        vch = instance.characters[vch_id]
        if fight.is_safe_spell(ch, vch, True) or (
            ch.is_npc() and vch.is_npc() and (ch.fighting == vch or vch.fighting == ch)
        ):
            continue

        if handler_magic.saves_spell(level, vch, merc.DAM_POISON):
            effects.poison_effect(vch, level // 2, dam // 4, merc.TARGET_CHAR)
            fight.damage(ch, vch, dam // 2, sn, merc.DAM_POISON, True)
        else:
            effects.poison_effect(vch, level, dam, merc.TARGET_CHAR)
            fight.damage(ch, vch, dam, sn, merc.DAM_POISON, True)


const.register_spell(
    const.skill_type(
        "gas breath",
        {"mage": 39, "cleric": 43, "thief": 47, "warrior": 50},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_gas_breath,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(203),
        175,
        24,
        "blast of gas",
        "!Gas Breath!",
        "",
    )
)
