from const import skill_table, SLOT, skill_type, register_spell
from merc import IS_NPC, TARGET_CHAR, POS_STANDING, TAR_IGNORE


def spell_mass_healing(sn, level, ch, victim, target):
    for gch in ch.in_room.people:
        if (IS_NPC(ch) and IS_NPC(gch) ) or ( not IS_NPC(ch) and not IS_NPC(gch)):
            skill_table['heal'].spell_fun('heal', level, ch, gch, TARGET_CHAR)
            skill_table['refresh'].spell_fun('refresh', level, ch, gch, TARGET_CHAR)


register_spell(skill_type("mass healing",
                          {'mage': 53, 'cleric': 38, 'thief': 53, 'warrior': 46},
                          {'mage': 2, 'cleric': 2, 'thief': 4, 'warrior': 4},
                          spell_mass_healing, TAR_IGNORE, POS_STANDING, None,
                          SLOT(508), 100, 36, "", "!Mass Healing!", ""))