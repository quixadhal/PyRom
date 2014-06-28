from const import SLOT, skill_table, skill_type
from fight import damage
from merc import IS_NPC, IS_EVIL, act, TO_ROOM, TO_VICT, dice, saves_spell, DAM_NEGATIVE, TARGET_CHAR, \
    TAR_CHAR_OFFENSIVE, POS_FIGHTING


def spell_demonfire(sn, level, ch, victim, target):
    # RT replacement demonfire spell */
    if not IS_NPC(ch) and not IS_EVIL(ch):
        victim = ch
        ch.send("The demons turn upon you! \n")

    ch.alignment = max(-1000, ch.alignment - 50)

    if victim != ch:
        act("$n calls forth the demons of Hell upon $N! ", ch, None, victim, TO_ROOM)
        act("$n has assailed you with the demons of Hell! ", ch, None, victim, TO_VICT)
        ch.send("You conjure forth the demons of hell! \n")
    dam = dice(level, 10)
    if saves_spell(level, victim, DAM_NEGATIVE):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_NEGATIVE, True)
    skill_table['curse'].spell_fun('curse', 3 * level // 4, ch, victim, TARGET_CHAR)


skill_type("demonfire",
           {'mage': 53, 'cleric': 34, 'thief': 53, 'warrior': 45},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_demonfire, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(505), 20, 12, "torments", "!Demonfire!", "")