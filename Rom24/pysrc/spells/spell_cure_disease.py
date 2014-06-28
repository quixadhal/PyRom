from const import SLOT, skill_type, skill_table
from merc import is_affected, act, TO_CHAR, check_dispel, TO_ROOM, POS_STANDING, TAR_CHAR_DEFENSIVE


def spell_cure_disease(sn, level, ch, victim, target):
    if not is_affected(victim, skill_table['plague']):
        if victim == ch:
            ch.send("You aren't ill.\n")
        else:
            act("$N doesn't appear to be diseased.", ch, None, victim, TO_CHAR)
        return

    if check_dispel(level, victim, skill_table['plague']):
        victim.send("Your sores vanish.\n")
        act("$n looks relieved as $s sores vanish.", victim, None, None, TO_ROOM)
        return

    ch.send("Spell failed.\n")


skill_type("cure disease",
           {'mage': 53, 'cleric': 13, 'thief': 53, 'warrior': 14},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cure_disease, TAR_CHAR_DEFENSIVE, POS_STANDING,
           None, SLOT(501), 20, 12, "", "!Cure Disease!", "")