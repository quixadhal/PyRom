from const import SLOT, skill_type
import const
from merc import is_affected, act, TO_CHAR, check_dispel, TO_ROOM, POS_FIGHTING, TAR_CHAR_DEFENSIVE


def spell_cure_blindness(sn, level, ch, victim, target):
    if not is_affected(victim, const.skill_table['blindness']):
        if victim == ch:
            ch.send("You aren't blind.\n")
        else:
            act("$N doesn't appear to be blinded.", ch, None, victim, TO_CHAR)
        return

    if check_dispel(level, victim, const.skill_table['blindness']):
        victim.send("Your vision returns!\n")
        act("$n is no longer blinded.", victim, None, None, TO_ROOM)
    else:
        ch.send("Spell failed.\n")


skill_type("cure blindness",
           {'mage': 53, 'cleric': 6, 'thief': 53, 'warrior': 8},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cure_blindness, TAR_CHAR_DEFENSIVE, POS_FIGHTING,
           None, SLOT(14), 5, 12, "", "!Cure Blindness!", "")