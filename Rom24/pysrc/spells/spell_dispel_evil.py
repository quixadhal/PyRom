from const import SLOT, skill_type, register_spell
from fight import damage
from merc import IS_NPC, IS_EVIL, IS_GOOD, act, TO_ROOM, IS_NEUTRAL, TO_CHAR, dice, saves_spell, DAM_HOLY, POS_FIGHTING, \
    TAR_CHAR_OFFENSIVE


def spell_dispel_evil(sn, level, ch, victim, target):
    if not IS_NPC(ch) and IS_EVIL(ch):
        victim = ch

    if IS_GOOD(victim):
        act("Mota protects $N.", ch, None, victim, TO_ROOM)
        return

    if IS_NEUTRAL(victim):
        act("$N does not seem to be affected.", ch, None, victim, TO_CHAR)
        return

    if victim.hit > (ch.level * 4):
        dam = dice(level, 4)
    else:
        dam = max(victim.hit, dice(level, 4))
    if saves_spell(level, victim, DAM_HOLY):
        dam = dam // 2
    damage(ch, victim, dam, sn, DAM_HOLY, True)


register_spell(skill_type("dispel evil",
                          {'mage': 53, 'cleric': 15, 'thief': 53, 'warrior': 21},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_dispel_evil, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
                          None, SLOT(22), 15, 12, "dispel evil", "!Dispel Evil!", ""))