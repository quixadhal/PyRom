from rom24 import const
from rom24 import handler_game
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_dispel_magic(sn, level, ch, victim, target):
    # modified for enhanced use */
    if handler_magic.saves_spell(level, victim, merc.DAM_OTHER):
        victim.send("You feel a brief tingling sensation.\n")
        ch.send("You failed.\n")
        return

    spells = {
        "armor": None,
        "bless": None,
        "blindness": "$n is no longer blinded",
        "calm": "$n no longer looks so peaceful...",
        "change sex": "$n looks more like $mself again.",
        "charm person": "$n regains $s free will.",
        "chill touch": "$n looks warmer",
        "curse": None,
        "detect evil": None,
        "detect good": None,
        "detect hidden": None,
        "detect invis": None,
        "detect magic": None,
        "faerie fire": "$n's outline fades",
        "fly": "$n falls to the ground! ",
        "frenzy": "$n no longer looks so wild.",
        "giant strength": "$n no longer looks so mighty.",
        "haste": "$n is no longer moving so quickly",
        "infravision": None,
        "invis": "$n fades into existence.",
        "mass invis": "$n fades into existence",
        "pass door": None,
        "protection evil": None,
        "protection good": None,
        "sanctuary": "The white aura around $n's body vanishes.",
        "shield": "The shield protecting $n vanishes",
        "sleep": None,
        "slow": "$n is no longer moving so slowly.",
        "stone skin": "$n's skin regains its normal texture.",
        "weaken": "$n looks stronger.",
    }

    for k, v in spells.items():
        if handler_magic.check_dispel(level, victim, const.skill_table[k]):
            if v:
                handler_game.act(v, victim, None, None, merc.TO_ROOM)
            found = True

    if (
        victim.is_affected(merc.AFF_SANCTUARY)
        and not handler_magic.saves_dispel(level, victim.level, -1)
        and not state_checks.is_affected(victim, const.skill_table["sanctuary"])
    ):
        state_checks.REMOVE_BIT(victim.affected_by, merc.AFF_SANCTUARY)
        handler_game.act(
            "The white aura around $n's body vanishes.",
            victim,
            None,
            None,
            merc.TO_ROOM,
        )
        found = True

    if found:
        ch.send("Ok.\n")
    else:
        ch.send("Spell failed.\n")


const.register_spell(
    const.skill_type(
        "dispel magic",
        {"mage": 16, "cleric": 24, "thief": 30, "warrior": 30},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_dispel_magic,
        merc.TAR_CHAR_OFFENSIVE,
        merc.POS_FIGHTING,
        None,
        const.SLOT(59),
        15,
        12,
        "",
        "!Dispel Magic!",
        "",
    )
)
