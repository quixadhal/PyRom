import random

from rom24 import const
from rom24 import effects
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc


def spell_fire_breath(sn, level, ch, victim, target):
    handler_game.act(
        "$n breathes forth a cone of fire.", ch, None, victim, merc.TO_NOTVICT
    )
    handler_game.act(
        "$n breathes a cone of hot fire over you! ", ch, None, victim, merc.TO_VICT
    )
    handler_game.act("You breath forth a cone of fire.", ch, None, None, merc.TO_CHAR)

    hpch = max(10, ch.hit)
    hp_dam = random.randint(hpch // 9 + 1, hpch // 5)
    dice_dam = game_utils.dice(level, 20)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    effects.fire_effect(victim.in_room, level, dam // 2, merc.TARGET_ROOM)

    for vch in victim.in_room.people[:]:
        if fight.is_safe_spell(ch, vch, True) or (
            vch.is_npc() and ch.is_npc() and (ch.fighting != vch or vch.fighting != ch)
        ):
            continue

        if vch == victim:  # full damage */
            if handler_magic.saves_spell(level, vch, merc.DAM_FIRE):
                effects.fire_effect(vch, level // 2, dam // 4, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 2, sn, merc.DAM_FIRE, True)
            else:
                effects.fire_effect(vch, level, dam, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam, sn, merc.DAM_FIRE, True)
        else:  # partial damage */
            if handler_magic.saves_spell(level - 2, vch, merc.DAM_FIRE):
                effects.fire_effect(vch, level // 4, dam // 8, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 4, sn, merc.DAM_FIRE, True)
            else:
                effects.fire_effect(vch, level // 2, dam // 4, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 2, sn, merc.DAM_FIRE, True)


const.register_spell(
    const.skill_type(
        "fire breath",
        {"mage": 40, "cleric": 45, "thief": 50, "warrior": 51},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_fire_breath,
        merc.TAR_CHAR_OFFENSIVE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(201),
        200,
        24,
        "blast of flame",
        "The smoke leaves your eyes.",
        "",
    )
)
