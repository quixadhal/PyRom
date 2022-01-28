from rom24 import const
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import merc
from rom24 import state_checks


def spell_holy_word(sn, level, ch, victim, target):
    # RT really nasty high-level attack spell */
    handler_game.act("$n utters a word of divine power! ", ch, None, None, merc.TO_ROOM)
    ch.send("You utter a word of divine power.\n")

    for vch_id in ch.in_room.people:

        vch = instance.characters[vch_id]
        if (
            (ch.is_good() and vch.is_good())
            or (ch.is_evil() and vch.is_evil())
            or (ch.is_neutral() and vch.is_neutral())
        ):
            vch.send("You feel full more powerful.\n")
            const.skill_table["frenzy"].spell_fun(
                "frenzy", level, ch, vch, merc.TARGET_CHAR
            )
            const.skill_table["bless"].spell_fun(
                "bless", level, ch, vch, merc.TARGET_CHAR
            )
        elif (ch.is_good() and state_checks.IS_EVIL(vch)) or (
            ch.is_evil() and state_checks.IS_GOOD(vch)
        ):
            if not fight.is_safe_spell(ch, vch, True):
                const.skill_table["curse"].spell_fun(
                    "curse", level, ch, vch, merc.TARGET_CHAR
                )
                vch.send("You are struck down! \n")
                dam = game_utils.dice(level, 6)
                fight.damage(ch, vch, dam, sn, merc.DAM_ENERGY, True)
        elif state_checks.IS_NEUTRAL(ch):
            if not fight.is_safe_spell(ch, vch, True):
                const.skill_table["curse"].spell_fun(
                    "curse", level // 2, ch, vch, merc.TARGET_CHAR
                )
                vch.send("You are struck down! \n")
                dam = game_utils.dice(level, 4)
                fight.damage(ch, vch, dam, sn, merc.DAM_ENERGY, True)
    ch.send("You feel drained.\n")
    ch.move = 0
    ch.hit = ch.hit // 2


const.register_spell(
    const.skill_type(
        "holy word",
        {"mage": 53, "cleric": 36, "thief": 53, "warrior": 42},
        {"mage": 2, "cleric": 2, "thief": 4, "warrior": 4},
        spell_holy_word,
        merc.TAR_IGNORE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(506),
        200,
        24,
        "divine wrath",
        "!Holy Word!",
        "",
    )
)
