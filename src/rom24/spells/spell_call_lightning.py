from rom24 import const
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_call_lightning(sn, level, ch, victim, target):
    if not state_checks.IS_OUTSIDE(ch):
        ch.send("You must be out of doors.\n")
        return

    if handler_game.weather_info.sky < merc.SKY_RAINING:
        ch.send("You need bad weather.\n")
        return

    dam = game_utils.dice(level // 2, 8)

    ch.send("Mota's lightning strikes your foes! \n")
    handler_game.act(
        "$n calls Mota's lightning to strike $s foes! ", ch, None, None, merc.TO_ROOM
    )

    for vch in instance.characters.values():
        if vch.in_room == None:
            continue
        if vch.in_room == ch.in_room:
            if vch is not ch and (not vch.is_npc() if ch.is_npc() else vch.is_npc()):
                fight.damage(
                    ch,
                    vch,
                    dam // 2
                    if handler_magic.saves_spell(level, vch, merc.DAM_LIGHTNING)
                    else dam,
                    sn,
                    merc.DAM_LIGHTNING,
                    True,
                )
            continue

        if (
            vch.in_room.area == ch.in_room.area
            and state_checks.IS_OUTSIDE(vch)
            and vch.is_awake()
        ):
            vch.send("Lightning flashes in the sky.\n")


const.register_spell(
    const.skill_type(
        "call lightning",
        {"mage": 26, "cleric": 18, "thief": 31, "warrior": 22},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_call_lightning,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(6),
        15,
        12,
        "lightning bolt",
        "!Call Lightning!",
        "",
    )
)
