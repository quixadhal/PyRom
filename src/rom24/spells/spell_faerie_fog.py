from rom24 import const
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_faerie_fog(sn, level, ch, victim, target):
    handler_game.act(
        "$n conjures a cloud of purple smoke.", ch, None, None, merc.TO_ROOM
    )
    ch.send("You conjure a cloud of purple smoke.\n")

    for ich_id in ch.in_room.people:

        ich = instance.characters[ich_id]
        if ich.invis_level > 0:
            continue

        if ich == ch or handler_magic.saves_spell(level, ich, merc.DAM_OTHER):
            continue

        ich.affect_strip("invis")
        ich.affect_strip("mass_invis")
        ich.affect_strip("sneak")
        ich.affected_by.rem_bit(merc.AFF_HIDE)
        ich.affected_by.rem_bit(merc.AFF_INVISIBLE)
        ich.affected_by.rem_bit(merc.AFF_SNEAK)
        handler_game.act("$n is revealed! ", ich, None, None, merc.TO_ROOM)
        ich.send("You are revealed! \n")


const.register_spell(
    const.skill_type(
        "faerie fog",
        {"mage": 14, "cleric": 21, "thief": 16, "warrior": 24},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_faerie_fog,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(73),
        12,
        12,
        "faerie fog",
        "!Faerie Fog!",
        "",
    )
)
