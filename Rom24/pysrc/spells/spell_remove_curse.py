from const import SLOT, skill_type, skill_table
from merc import TARGET_OBJ, IS_OBJ_STAT, ITEM_NODROP, ITEM_NOREMOVE, ITEM_NOUNCURSE, saves_dispel, REMOVE_BIT, act, \
    TO_ALL, TO_CHAR, check_dispel, TO_ROOM, POS_STANDING, TAR_OBJ_CHAR_DEF


def spell_remove_curse(sn, level, ch, victim, target):
    found = False
    # do object cases first */
    if target == TARGET_OBJ:
        obj = victim

        if IS_OBJ_STAT(obj, ITEM_NODROP) or IS_OBJ_STAT(obj, ITEM_NOREMOVE):
            if not IS_OBJ_STAT(obj, ITEM_NOUNCURSE) and not saves_dispel(level + 2, obj.level, 0):
                REMOVE_BIT(obj.extra_flags, ITEM_NODROP)
                REMOVE_BIT(obj.extra_flags, ITEM_NOREMOVE)
                act("$p glows blue.", ch, obj, None, TO_ALL)
                return
            act("The curse on $p is beyond your power.", ch, obj, None, TO_CHAR)
            return

        act("There doesn't seem to be a curse on $p.", ch, obj, None, TO_CHAR)
        return

    # characters */
    if check_dispel(level, victim, skill_table['curse']):
        victim.send("You feel better.\n")
        act("$n looks more relaxed.", victim, None, None, TO_ROOM)

    for obj in victim.carrying:
        if (IS_OBJ_STAT(obj, ITEM_NODROP) or IS_OBJ_STAT(obj, ITEM_NOREMOVE)) and not IS_OBJ_STAT(obj, ITEM_NOUNCURSE):
            # attempt to remove curse */
            if not saves_dispel(level, obj.level, 0):
                REMOVE_BIT(obj.extra_flags, ITEM_NODROP)
                REMOVE_BIT(obj.extra_flags, ITEM_NOREMOVE)
                act("Your $p glows blue.", victim, obj, None, TO_CHAR)
                act("$n's $p glows blue.", victim, obj, None, TO_ROOM)
                break

skill_type("remove curse",
           { 'mage':53, 'cleric':18, 'thief':53, 'warrior':22 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_remove_curse, TAR_OBJ_CHAR_DEF, POS_STANDING,
           None, SLOT(35), 5, 12, "", "!Remove Curse!", "")