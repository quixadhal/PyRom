from rom24 import const
from rom24 import handler_magic
from rom24 import merc


def spell_farsight(sn, level, ch, victim, target):
    if ch.is_affected(merc.AFF_BLIND):
        ch.send("Maybe it would help if you could see?\n")
        return

    ch.do_scan(handler_magic.target_name)


const.register_spell(
    const.skill_type(
        "farsight",
        {"mage": 14, "cleric": 16, "thief": 16, "warrior": 53},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_farsight,
        merc.TAR_IGNORE,
        merc.POS_STANDING,
        None,
        const.SLOT(521),
        36,
        20,
        "farsight",
        "!Farsight!",
        "",
    )
)
