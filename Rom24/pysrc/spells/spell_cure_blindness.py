import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_cure_blindness(sn, level, ch, victim, target):
    if not state_checks.is_affected(victim, const.skill_table['blindness']):
        if victim == ch:
            ch.send("You aren't blind.\n")
        else:
            handler_game.act("$N doesn't appear to be blinded.", ch, None, victim, merc.TO_CHAR)
        return

    if handler_magic.check_dispel(level, victim, const.skill_table['blindness']):
        victim.send("Your vision returns!\n")
        handler_game.act("$n is no longer blinded.", victim, None, None, merc.TO_ROOM)
    else:
        ch.send("Spell failed.\n")


const.register_spell(const.skill_type("cure blindness",
                          {'mage': 53, 'cleric': 6, 'thief': 53, 'warrior': 8},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_blindness, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(14), 5, 12, "", "!Cure Blindness!", ""))
