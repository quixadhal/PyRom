import random

from rom24 import const
from rom24 import effects
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc


def spell_frost_breath(sn, level, ch, victim, target):
    handler_game.act(
        "$n breathes out a freezing cone of frost! ", ch, None, victim, merc.TO_NOTVICT
    )
    handler_game.act(
        "$n breathes a freezing cone of frost over you! ",
        ch,
        None,
        victim,
        merc.TO_VICT,
    )
    handler_game.act("You breath out a cone of frost.", ch, None, None, merc.TO_CHAR)

    hpch = max(12, ch.hit)
    hp_dam = random.randint(hpch // 11 + 1, hpch // 6)
    dice_dam = game_utils.dice(level, 16)

    dam = max(hp_dam + dice_dam // 10, dice_dam + hp_dam // 10)
    effects.cold_effect(victim.in_room, level, dam // 2, merc.TARGET_ROOM)

    for vch in victim.in_room.people[:]:
        if fight.is_safe_spell(ch, vch, True) or (
            vch.is_npc() and ch.is_npc() and (ch.fighting != vch or vch.fighting != ch)
        ):
            continue

        if vch == victim:  # full damage */
            if handler_magic.saves_spell(level, vch, merc.DAM_COLD):
                effects.cold_effect(vch, level // 2, dam // 4, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 2, sn, merc.DAM_COLD, True)
            else:
                effects.cold_effect(vch, level, dam, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam, sn, merc.DAM_COLD, True)
        else:
            if handler_magic.saves_spell(level - 2, vch, merc.DAM_COLD):
                effects.cold_effect(vch, level // 4, dam // 8, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 4, sn, merc.DAM_COLD, True)
            else:
                effects.cold_effect(vch, level // 2, dam // 4, merc.TARGET_CHAR)
                fight.damage(ch, vch, dam // 2, sn, merc.DAM_COLD, True)


const.register_spell(
    const.skill_type(
        "frost breath",
        {"mage": 34, "cleric": 36, "thief": 38, "warrior": 40},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_frost_breath,
        merc.TAR_CHAR_OFFENSIVE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(202),
        125,
        24,
        "blast of frost",
        "!Frost Breath!",
        "",
    )
)
