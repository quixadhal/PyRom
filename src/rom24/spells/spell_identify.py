from rom24 import const
from rom24 import merc
from rom24.merc import (
    affect_loc_name,
    affect_bit_name,
    extra_bit_name,
    imm_bit_name,
    weapon_bit_name,
    cont_bit_name,
)

# TODO: Make this ROM-like formatting
def spell_identify(sn, level, ch, victim, target):
    item = victim
    if type(item) is int:
        item = instance.items[item]
    ch.send(
        "Item '{item.name}' is type {item.item_type}, "
        "weight is {weight}".format(item=item, weight=(item.weight // 10))
    )
    ch.send("Equips to: {item.equips_to_names}\n".format(item=item))
    ch.send("Item Attribute Flags: {item.item_attribute_names}\n".format(item=item))
    ch.send("Item Restriction Flags: {item.item_restriction_names}\n".format(item=item))
    ch.send("Value is {item.cost}, level is {item.level}.\n".format(item=item))
    if (
        item.item_type == merc.ITEM_SCROLL
        or item.item_type == merc.ITEM_POTION
        or item.item_type == merc.ITEM_PILL
    ):
        ch.send("Level {item.value[0]} spells of:".format(item=item))
        for i in item.value:
            if 0 <= i < merc.MAX_SKILL:
                ch.send(" '{skill}'".format(skill=const.skill_table[i].name))
        ch.send(".\n")
    elif item.item_type == merc.ITEM_WAND or item.item_type == merc.ITEM_STAFF:
        ch.send(
            "Has {item.value[2]} charges of level {item.value[0]}".format(item=item)
        )
        if 0 <= item.value[3] < merc.MAX_SKILL:
            ch.send("' {skill}'".format(skill=const.skill_table[item.value[3]].name))
        ch.send(".\n")
    elif item.item_type == merc.ITEM_DRINK_CON:
        ch.send(
            "It holds {color}-colored {liquid}.\n".format(
                color=const.liq_table[item.value[2]].color,
                liquid=const.liq_table[item.value[2]].name,
            )
        )
    elif item.item_type == merc.ITEM_CONTAINER:
        ch.send(
            "Capacity: {item.value[0]}#  "
            "Maximum weight: {item.value[3]}#  "
            "flags: {cflag}\n".format(item=item, cflag=cont_bit_name(item.value[1]))
        )
        if item.value[4] != 100:
            ch.send("Weight multiplier: {item.value[4]}%%\n".format(item=item))
    elif item.item_type == merc.ITEM_WEAPON:
        ch.send("Weapon type is ")

        weapons = {
            merc.WEAPON_EXOTIC: "exotic",
            merc.WEAPON_SWORD: "sword",
            merc.WEAPON_DAGGER: "dagger",
            merc.WEAPON_SPEAR: "spear//staff",
            merc.WEAPON_MACE: "mace//club",
            merc.WEAPON_AXE: "axe",
            merc.WEAPON_FLAIL: "flail",
            merc.WEAPON_WHIP: "whip",
            merc.WEAPON_POLEARM: "polearm",
        }

        if item.value[0] not in weapons:
            ch.send("unknown")
        else:
            ch.send(weapons[item.value[0]])

        if item.new_format:
            ch.send(
                "Damage is {item.value[1]}d{item.value[2]} "
                "(average {average}).\n".format(
                    item=item, average=((1 + item.value[2]) * item.value[1] // 2)
                )
            )

        else:
            ch.send(
                "Damage is {item.value[1]} to {item.value[2]} "
                "(average {average}).\n".format(
                    item=item, average=((item.value[2] + item.value[1]) // 2)
                )
            )

        if item.weapon_attributes:  # weapon flags */
            ch.send("Weapons flags: {item.weapon_attribute_names}\n".format(item=item))
    elif item.item_type == merc.ITEM_ARMOR:
        ch.send(
            "Armor class is {item.value[0]} pierce, {item.value[1]} bash, "
            "{item.value[2]} slash, and {item.value[3]} vs. magic.\n".format(item=item)
        )

    affected = item.affected
    if not item.enchanted:
        affected.extend(instance.item_templates[item.vnum].affected)

    for paf in affected:
        if paf.location != merc.APPLY_NONE and paf.modifier != 0:
            ch.send(
                "Affects {aff_loc} by {modifier}.\n".format(
                    aff_loc=affect_loc_name(paf.location), modifier=paf.modifier
                )
            )
            if paf.bitvector:
                if paf.where == merc.TO_AFFECTS:
                    ch.send(
                        "Adds {aff_name} affect.\n".format(
                            aff_name=affect_bit_name(paf.bitvector)
                        )
                    )
                elif paf.where == merc.TO_OBJECT:
                    ch.send(
                        "Adds {bit_name} item flag.\n".format(
                            bit_name=extra_bit_name(paf.bitvector)
                        )
                    )
                elif paf.where == merc.TO_IMMUNE:
                    ch.send(
                        "Adds immunity to {imm}.\n".format(
                            imm=imm_bit_name(paf.bitvector)
                        )
                    )
                elif paf.where == merc.TO_RESIST:
                    ch.send(
                        "Adds resistance to {res}.\n".format(
                            res=imm_bit_name(paf.bitvector)
                        )
                    )
                elif paf.where == merc.TO_VULN:
                    ch.send(
                        "Adds vulnerability to {vuln}.\n".format(
                            vuln=imm_bit_name(paf.bitvector)
                        )
                    )
                else:
                    ch.send(
                        "Unknown bit {bit_name}: {bit}\n".format(
                            bit_name=paf.where, bit=paf.bitvector
                        )
                    )


const.register_spell(
    const.skill_type(
        "identify",
        {"mage": 15, "cleric": 16, "thief": 18, "warrior": 53},
        {"mage": 1, "cleric": 1, "thief": 2, "warrior": 2},
        spell_identify,
        merc.TAR_OBJ_INV,
        merc.POS_STANDING,
        None,
        const.SLOT(53),
        12,
        24,
        "",
        "!Identify!",
        "",
    )
)
