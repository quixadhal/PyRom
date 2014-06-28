import const
import handler
import merc


def spell_identify(sn, level, ch, victim, target):
    obj = victim
    ch.send("Object '%s' is type %s, extra flags %s.\nWeight is %d, value is %d, level is %d.\n" % ( obj.name,
                                                                                                     obj.item_type,
                                                                                                     handler.extra_bit_name(
                                                                                                         obj.extra_flags),
                                                                                                     obj.weight // 10,
                                                                                                     obj.cost,
                                                                                                     obj.level ))

    if obj.item_type == merc.ITEM_SCROLL or obj.item_type == merc.ITEM_POTION or obj.item_type == merc.ITEM_PILL:
        ch.send("Level %d spells of:" % obj.value[0])
        for i in obj.value:
            if i >= 0 and i < merc.MAX_SKILL:
                ch.send(" '%s'" % const.skill_table[i].name)
        ch.send(".\n")
    elif obj.item_type == merc.ITEM_WAND or obj.item_type == merc.ITEM_STAFF:
        ch.send("Has %d charges of level %d" % ( obj.value[2], obj.value[0] ))
        if obj.value[3] >= 0 and obj.value[3] < merc.MAX_SKILL:
            ch.send("' %s'" % const.skill_table[obj.value[3]].name)
        ch.send(".\n")
    elif obj.item_type == merc.ITEM_DRINK_CON:
        ch.send("It holds %s-colored %s.\n" % ( const.liq_table[obj.value[2]].liq_color, const.liq_table[obj.value[2]].liq_name))
    elif obj.item_type == merc.ITEM_CONTAINER:
        ch.send("Capacity: %d#  Maximum weight: %d#  flags: %s\n" % (
            obj.value[0], obj.value[3], handler.cont_bit_name(obj.value[1])))
        if obj.value[4] != 100:
            ch.send("Weight multiplier: %d%%\n" % obj.value[4])
    elif obj.item_type == merc.ITEM_WEAPON:
        ch.send("Weapon type is ")

        weapons = {merc.WEAPON_EXOTIC: "exotic",
                   merc.WEAPON_SWORD: "sword",
                   merc.WEAPON_DAGGER: "dagger",
                   merc.WEAPON_SPEAR: "spear//staff",
                   merc.WEAPON_MACE: "mace//club",
                   merc.WEAPON_AXE: "axe",
                   merc.WEAPON_FLAIL: "flail",
                   merc.WEAPON_WHIP: "whip",
                   merc.WEAPON_POLEARM: "polearm"}

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
            ch.send("Weapons flags: %s\n" % handler.weapon_bit_name(obj.value[4]))
    elif obj.item_type == merc.ITEM_ARMOR:
        ch.send("Armor class is %d pierce, %d bash, %d slash, and %d vs. magic.\n" % ( obj.value[0],
                                                                                       obj.value[1], obj.value[2],
                                                                                       obj.value[3] ))

    affected = obj.affected
    if not obj.enchanted:
        affected.extend(obj.pIndexData.affected)

    for paf in affected:
        if paf.location != merc.APPLY_NONE and paf.modifier != 0:
            ch.send("Affects %s by %d.\n" % ( handler.affect_loc_name(paf.location), paf.modifier ))
            if paf.bitvector:
                if paf.where == merc.TO_AFFECTS:
                    ch.send("Adds %s affect.\n" % handler.affect_bit_name(paf.bitvector))
                elif paf.where == merc.TO_OBJECT:
                    ch.send("Adds %s object flag.\n" % handler.extra_bit_name(paf.bitvector))
                elif paf.where == merc.TO_IMMUNE:
                    ch.send("Adds immunity to %s.\n" % handler.imm_bit_name(paf.bitvector))
                elif paf.where == merc.TO_RESIST:
                    ch.send("Adds resistance to %s.\n" % handler.imm_bit_name(paf.bitvector))
                elif paf.where == merc.TO_VULN:
                    ch.send("Adds vulnerability to %s.\n" % handler.imm_bit_name(paf.bitvector))
                else:
                    ch.send("Unknown bit %d: %d\n" % (paf.where, paf.bitvector))


const.register_spell(const.skill_type("identify",
                          {'mage': 15, 'cleric': 16, 'thief': 18, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_identify, merc.TAR_OBJ_INV, merc.POS_STANDING, None,
                          const.SLOT(53), 12, 24, "", "!Identify!", ""))
