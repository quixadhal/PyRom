import const
import fight
import game_utils
import handler_game
import handler_magic
import merc


def spell_demonfire(sn, level, ch, victim, target):
    # RT replacement demonfire spell */
    if not ch.is_npc() and not ch.is_evil():
        victim = ch
        ch.send("The demons turn upon you! \n")

    ch.alignment = max(-1000, ch.alignment - 50)

    if victim != ch:
        handler_game.act("$n calls forth the demons of Hell upon $N! ", ch, None, victim, merc.TO_ROOM)
        handler_game.act("$n has assailed you with the demons of Hell! ", ch, None, victim, merc.TO_VICT)
        ch.send("You conjure forth the demons of hell! \n")
    dam = game_utils.dice(level, 10)
    if handler_magic.saves_spell(level, victim, merc.DAM_NEGATIVE):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_NEGATIVE, True)
    const.skill_table['curse'].spell_fun('curse', 3 * level // 4, ch, victim, merc.TARGET_CHAR)


const.register_spell(const.skill_type("demonfire",
                          {'mage': 53, 'cleric': 34, 'thief': 53, 'warrior': 45},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_demonfire, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(505), 20, 12, "torments", "!Demonfire!", ""))
