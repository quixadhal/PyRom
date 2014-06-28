from const import SLOT, register_spell, skill_type, liq_table
from handler import extra_bit_name, cont_bit_name, weapon_bit_name, affect_loc_name, affect_bit_name, imm_bit_name
from merc import ITEM_SCROLL, ITEM_POTION, ITEM_PILL, MAX_SKILL, ITEM_WAND, ITEM_STAFF, ITEM_DRINK_CON, ITEM_CONTAINER, \
    ITEM_WEAPON, WEAPON_EXOTIC, WEAPON_SWORD, WEAPON_DAGGER, WEAPON_SPEAR, WEAPON_MACE, WEAPON_AXE, WEAPON_FLAIL, \
    WEAPON_WHIP, WEAPON_POLEARM, ITEM_ARMOR, APPLY_NONE, TO_AFFECTS, TO_OBJECT, TO_IMMUNE, TO_RESIST, TO_VULN, \
    POS_STANDING, TAR_OBJ_INV


def spell_identify(sn, level, ch, victim, target):
    obj = victim
    ch.send("Object '%s' is type %s, extra flags %s.\nWeight is %d, value is %d, level is %d.\n" % ( obj.name,
                                                                                                     obj.item_type,
                                                                                                     extra_bit_name(
                                                                                                         obj.extra_flags),
                                                                                                     obj.weight // 10,
                                                                                                     obj.cost,
                                                                                                     obj.level ))

    if obj.item_type == ITEM_SCROLL or obj.item_type == ITEM_POTION or obj.item_type == ITEM_PILL:
        ch.send("Level %d spells of:" % obj.value[0])
        for i in obj.value:
            if i >= 0 and i < MAX_SKILL:
                ch.send(" '%s'" % skill_table[i].name)
        ch.send(".\n")
    elif obj.item_type == ITEM_WAND or obj.item_type == ITEM_STAFF:
        ch.send("Has %d charges of level %d" % ( obj.value[2], obj.value[0] ))
        if obj.value[3] >= 0 and obj.value[3] < MAX_SKILL:
            ch.send("' %s'" % const.skill_table[obj.value[3]].name)
        ch.send(".\n")
    elif obj.item_type == ITEM_DRINK_CON:
        ch.send("It holds %s-colored %s.\n" % ( liq_table[obj.value[2]].liq_color, liq_table[obj.value[2]].liq_name))
        send_to_char(buf, ch)
    elif obj.item_type == ITEM_CONTAINER:
        ch.send("Capacity: %d#  Maximum weight: %d#  flags: %s\n" % (
            obj.value[0], obj.value[3], cont_bit_name(obj.value[1])))
        if obj.value[4] != 100:
            ch.send("Weight multiplier: %d%%\n" % obj.value[4])
    elif obj.item_type == ITEM_WEAPON:
        ch.send("Weapon type is ")

        weapons = {WEAPON_EXOTIC: "exotic",
                   WEAPON_SWORD: "sword",
                   WEAPON_DAGGER: "dagger",
                   WEAPON_SPEAR: "spear//staff",
                   WEAPON_MACE: "mace//club",
                   WEAPON_AXE: "axe",
                   WEAPON_FLAIL: "flail",
                   WEAPON_WHIP: "whip",
                   WEAPON_POLEARM: "polearm"}

        if obj.value[0] not in weapons:
            ch.send("unknown")
        else:
            ch.send(weapons[obj.value[0]])

        if obj.pIndexData.new_format:
            ch.send("Damage is %dd%d (average %d).\n" % (
                obj.value[1], obj.value[2], (1 + obj.value[2]) * obj.value[1] // 2))
        else:
            ch.send("Damage is %d to %d (average %d).\n" % (
                obj.value[1], obj.value[2], ( obj.value[1] + obj.value[2] ) // 2 ))

        if obj.value[4]:  # weapon flags */
            ch.send("Weapons flags: %s\n" % weapon_bit_name(obj.value[4]))
    elif obj.item_type == ITEM_ARMOR:
        ch.send("Armor class is %d pierce, %d bash, %d slash, and %d vs. magic.\n" % ( obj.value[0],
                                                                                       obj.value[1], obj.value[2],
                                                                                       obj.value[3] ))

    affected = obj.affected
    if not obj.enchanted:
        affected.extend(obj.pIndexData.affected)

    for paf in affected:
        if paf.location != APPLY_NONE and paf.modifier != 0:
            ch.send("Affects %s by %d.\n" % ( affect_loc_name(paf.location), paf.modifier ))
            if paf.bitvector:
                if paf.where == TO_AFFECTS:
                    ch.send("Adds %s affect.\n" % affect_bit_name(paf.bitvector))
                elif paf.where == TO_OBJECT:
                    ch.send("Adds %s object flag.\n" % extra_bit_name(paf.bitvector))
                elif paf.where == TO_IMMUNE:
                    ch.send("Adds immunity to %s.\n" % imm_bit_name(paf.bitvector))
                elif paf.where == TO_RESIST:
                    ch.send("Adds resistance to %s.\n" % imm_bit_name(paf.bitvector))
                elif paf.where == TO_VULN:
                    ch.send("Adds vulnerability to %s.\n" % imm_bit_name(paf.bitvector))
                else:
                    ch.send("Unknown bit %d: %d\n" % (paf.where, paf.bitvector))


register_spell(skill_type("identify",
                          {'mage': 15, 'cleric': 16, 'thief': 18, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_identify, TAR_OBJ_INV, POS_STANDING, None,
                          SLOT(53), 12, 24, "", "!Identify!", ""))