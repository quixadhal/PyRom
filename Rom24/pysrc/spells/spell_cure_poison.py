from const import skill_type, SLOT, skill_table
from merc import is_affected, act, TO_CHAR, check_dispel, TO_ROOM, TAR_CHAR_DEFENSIVE, POS_STANDING


def spell_cure_poison(sn, level, ch, victim, target):
    if not is_affected(victim, skill_table['poison']):
        if victim == ch:
            ch.send("You aren't poisoned.\n")
        else:
            act("$N doesn't appear to be poisoned.", ch, None, victim, TO_CHAR)
        return

    if check_dispel(level, victim, skill_table['poison']):
        victim.send("A warm feeling runs through your body.\n")
        act("$n looks much better.", victim, None, None, TO_ROOM)
        return

    ch.send("Spell failed.\n")


skill_type("cure poison",
           {'mage': 53, 'cleric': 14, 'thief': 53, 'warrior': 16},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_cure_poison, TAR_CHAR_DEFENSIVE, POS_STANDING,
           None, SLOT(43), 5, 12, "", "!Cure Poison!", "")