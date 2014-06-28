from const import SLOT, skill_type, register_spell
from merc import ITEM_DRINK_CON, ITEM_FOOD, TAR_OBJ_INV, POS_STANDING


def spell_detect_poison(sn, level, ch, victim, target):
    if victim.item_type == ITEM_DRINK_CON or obj.item_type == ITEM_FOOD:
        if obj.value[3] != 0:
            ch.send("You smell poisonous fumes.\n")
        else:
            ch.send("It looks delicious.\n")
    else:
        ch.send("It doesn't look poisoned.\n")
    return


register_spell(skill_type("detect poison",
                          {'mage': 15, 'cleric': 7, 'thief': 9, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_poison, TAR_OBJ_INV, POS_STANDING, None,
                          SLOT(21), 5, 12, "", "!Detect Poison!", ""))