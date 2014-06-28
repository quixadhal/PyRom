from const import SLOT, skill_type
from merc import TARGET_OBJ, ITEM_FOOD, ITEM_DRINK_CON, IS_OBJ_STAT, ITEM_BLESS, ITEM_BURN_PROOF, act, TO_CHAR, TO_ALL, \
    ITEM_WEAPON, IS_WEAPON_STAT, WEAPON_FLAMING, WEAPON_FROST, WEAPON_VAMPIRIC, WEAPON_SHARP, WEAPON_VORPAL, \
    WEAPON_SHOCKING, WEAPON_POISON, AFFECT_DATA, TO_WEAPON, saves_spell, DAM_POISON, TO_ROOM, TO_AFFECTS, APPLY_STR, \
    AFF_POISON, POS_FIGHTING, TAR_OBJ_CHAR_OFF


def spell_poison(sn, level, ch, victim, target):
    if target == TARGET_OBJ:
        obj = victim

        if obj.item_type == ITEM_FOOD or obj.item_type == ITEM_DRINK_CON:
            if IS_OBJ_STAT(obj, ITEM_BLESS) or IS_OBJ_STAT(obj, ITEM_BURN_PROOF):
                act("Your spell fails to corrupt $p.", ch, obj, None, TO_CHAR)
                return
            obj.value[3] = 1
            act("$p is infused with poisonous vapors.", ch, obj, None, TO_ALL)
            return
        if obj.item_type == ITEM_WEAPON:
            if IS_WEAPON_STAT(obj, WEAPON_FLAMING) \
                    or IS_WEAPON_STAT(obj, WEAPON_FROST) \
                    or IS_WEAPON_STAT(obj, WEAPON_VAMPIRIC) \
                    or IS_WEAPON_STAT(obj, WEAPON_SHARP) \
                    or IS_WEAPON_STAT(obj, WEAPON_VORPAL) \
                    or IS_WEAPON_STAT(obj, WEAPON_SHOCKING) \
                    or IS_OBJ_STAT(obj, ITEM_BLESS) \
                    or IS_OBJ_STAT(obj, ITEM_BURN_PROOF):
                act("You can't seem to envenom $p.", ch, obj, None, TO_CHAR)
                return
            if IS_WEAPON_STAT(obj, WEAPON_POISON):
                act("$p is already envenomed.", ch, obj, None, TO_CHAR)
                return
            af = AFFECT_DATA()
            af.where = TO_WEAPON
            af.type = sn
            af.level = level // 2
            af.duration = level // 8
            af.location = 0
            af.modifier = 0
            af.bitvector = WEAPON_POISON
            obj.affect_add(af)
            act("$p is coated with deadly venom.", ch, obj, None, TO_ALL)
            return
        act("You can't poison $p.", ch, obj, None, TO_CHAR)
        return

    if saves_spell(level, victim, DAM_POISON):
        act("$n turns slightly green, but it passes.", victim, None, None, TO_ROOM)
        victim.send("You feel momentarily ill, but it passes.\n")
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = APPLY_STR
    af.modifier = -2
    af.bitvector = AFF_POISON
    victim.affect_join(af)
    victim.send("You feel very sick.\n")
    act("$n looks very ill.", victim, None, None, TO_ROOM)

skill_type("poison",
           { 'mage':17, 'cleric':12, 'thief':15, 'warrior':21 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_poison, TAR_OBJ_CHAR_OFF, POS_FIGHTING, None,
           SLOT(33), 10, 12, "poison", "You feel less sick.",
           "The poison on $p dries up.")