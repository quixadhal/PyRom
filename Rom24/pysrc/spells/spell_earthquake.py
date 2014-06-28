from const import SLOT, skill_type, register_spell
from fight import damage, is_safe_spell
from merc import act, TO_ROOM, char_list, IS_AFFECTED, AFF_FLYING, DAM_BASH, dice, POS_FIGHTING, TAR_IGNORE


def spell_earthquake(sn, level, ch, victim, target):
    ch.send("The earth trembles beneath your feet! \n")
    act("$n makes the earth tremble and shiver.", ch, None, None, TO_ROOM)

    for vch in char_list[:]:
        if not vch.in_room:
            continue
        if vch.in_room == ch.in_room:
            if vch != ch and not is_safe_spell(ch, vch, True):
                if IS_AFFECTED(vch, AFF_FLYING):
                    damage(ch, vch, 0, sn, DAM_BASH, True)
                else:
                    damage(ch, vch, level + dice(2, 8), sn, DAM_BASH, True)
            continue

        if vch.in_room.area == ch.in_room.area:
            vch.send("The earth trembles and shivers.\n")


register_spell(skill_type("earthquake",
                          {'mage': 53, 'cleric': 10, 'thief': 53, 'warrior': 14},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_earthquake, TAR_IGNORE, POS_FIGHTING,
                          None, SLOT(23), 15, 12, "earthquake", "!Earthquake!", ""))