import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_cure_disease(sn, level, ch, victim, target):
    if not state_checks.is_affected(victim, const.skill_table['plague']):
        if victim == ch:
            ch.send("You aren't ill.\n")
        else:
            handler_game.act("$N doesn't appear to be diseased.", ch, None, victim, merc.TO_CHAR)
        return

    if handler_magic.check_dispel(level, victim, const.skill_table['plague']):
        victim.send("Your sores vanish.\n")
        handler_game.act("$n looks relieved as $s sores vanish.", victim, None, None, merc.TO_ROOM)
        return

    ch.send("Spell failed.\n")


const.register_spell(const.skill_type("cure disease",
                          {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 14},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_cure_disease, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(501), 20, 12, "", "!Cure Disease!", ""))
