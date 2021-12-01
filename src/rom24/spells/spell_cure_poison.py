import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_cure_poison(sn, level, ch, victim, target):
    if not state_checks.is_affected(victim, const.skill_table['poison']):
        if victim == ch:
            ch.send("You aren't poisoned.\n")
        else:
            handler_game.act("$N doesn't appear to be poisoned.", ch, None, victim, merc.TO_CHAR)
        return

    if handler_magic.check_dispel(level, victim, const.skill_table['poison']):
        victim.send("A warm feeling runs through your body.\n")
        handler_game.act("$n looks much better.", victim, None, None, merc.TO_ROOM)
        return

    ch.send("Spell failed.\n")


const.register_spell(const.skill_type("cure poison",
                          {'mage': 53, 'cleric': 14, 'thief': 53, 'warrior': 16},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_poison, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(43), 5, 12, "", "!Cure Poison!", ""))
