import const
import merc
import state_checks


def spell_mass_healing(sn, level, ch, victim, target):
    for gch in merc.rooms[ch.in_room].people:
        if (
            ch.is_npc() and state_checks.IS_NPC(gch) ) or ( not ch.is_npc() and not state_checks.IS_NPC(gch)):
            const.skill_table['heal'].spell_fun('heal', level, ch, gch, merc.TARGET_CHAR)
            const.skill_table['refresh'].spell_fun('refresh', level, ch, gch, merc.TARGET_CHAR)


const.register_spell(const.skill_type("mass healing",
                          {'mage': 53, 'cleric': 38, 'thief': 53, 'warrior': 46},
                          {'mage': 2, 'cleric': 2, 'thief': 4, 'warrior': 4},
                          spell_mass_healing, merc.TAR_IGNORE, merc.POS_STANDING, None,
                          const.SLOT(508), 100, 36, "", "!Mass Healing!", ""))
