from rom24 import const
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_earthquake(sn, level, ch, victim, target):
    ch.send("The earth trembles beneath your feet! \n")
    handler_game.act(
        "$n makes the earth tremble and shiver.", ch, None, None, merc.TO_ROOM
    )

    for vch in instance.characters.values():
        if not vch.in_room:
            continue
        if vch.in_room == ch.in_room:
            if vch != ch and not fight.is_safe_spell(ch, vch, True):
                if state_checks.IS_AFFECTED(vch, merc.AFF_FLYING):
                    fight.damage(ch, vch, 0, sn, merc.DAM_BASH, True)
                else:
                    fight.damage(
                        ch, vch, level + game_utils.dice(2, 8), sn, merc.DAM_BASH, True
                    )
            continue

        if vch.in_room.area == ch.in_room.area:
            vch.send("The earth trembles and shivers.\n")


const.register_spell(
    const.skill_type(
        "earthquake",
        {"mage": 53, "cleric": 10, "thief": 53, "warrior": 14},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_earthquake,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(23),
        15,
        12,
        "earthquake",
        "!Earthquake!",
        "",
    )
)
