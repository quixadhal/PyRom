from rom24 import const
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_mass_invis(sn, level, ch, victim, target):
    for gch_id in ch.in_room.people:
        gch = instance.characters[gch_id]
        if not gch.is_same_group(ch) or gch.is_affected(merc.AFF_INVISIBLE):
            continue
        handler_game.act(
            "$n slowly fades out of existence.", gch, None, None, merc.TO_ROOM
        )
        gch.send("You slowly fade out of existence.\n")
        af = handler_game.AFFECT_DATA()
        af.where = merc.TO_AFFECTS
        af.type = sn
        af.level = level // 2
        af.duration = 24
        af.location = merc.APPLY_NONE
        af.modifier = 0
        af.bitvector = merc.AFF_INVISIBLE
        gch.affect_add(af)
    ch.send("Ok.\n")


const.register_spell(
    const.skill_type(
        "mass invis",
        {"mage": 22, "cleric": 25, "thief": 31, "warrior": 53},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_mass_invis,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(69),
        20,
        24,
        "",
        "You are no longer invisible.",
        "",
    )
)
