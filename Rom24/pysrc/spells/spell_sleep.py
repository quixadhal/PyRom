from const import SLOT, skill_type, register_spell
from merc import IS_AFFECTED, AFF_SLEEP, IS_NPC, IS_SET, ACT_UNDEAD, saves_spell, DAM_CHARM, AFFECT_DATA, TO_AFFECTS, \
    APPLY_NONE, IS_AWAKE, act, TO_ROOM, POS_SLEEPING, POS_STANDING, TAR_CHAR_OFFENSIVE


def spell_sleep(sn, level, ch, victim, target):
    if IS_AFFECTED(victim, AFF_SLEEP) \
            or (IS_NPC(victim) and IS_SET(victim.act, ACT_UNDEAD)) \
            or (level + 2) < victim.level \
            or saves_spell(level - 4, victim, DAM_CHARM):
        return
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 4 + level
    af.location = APPLY_NONE
    af.modifier = 0
    af.bitvector = AFF_SLEEP
    victim.affect_join(af)

    if IS_AWAKE(victim):
        victim.send("You feel very sleepy ..... zzzzzz.\n")
        act("$n goes to sleep.", victim, None, None, TO_ROOM)
        victim.position = POS_SLEEPING


register_spell(skill_type("sleep",
                          {'mage': 10, 'cleric': 53, 'thief': 11, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_sleep, TAR_CHAR_OFFENSIVE, POS_STANDING, None,
                          SLOT(38), 15, 12, "", "You feel less tired.", ""))