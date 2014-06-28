from const import register_spell, skill_type, SLOT
from fight import is_safe
from merc import IS_AFFECTED, AFF_CHARM, IS_SET, IMM_CHARM, saves_spell, DAM_CHARM, ROOM_LAW, stop_follower, \
    add_follower, AFFECT_DATA, TO_AFFECTS, number_fuzzy, act, TO_VICT, TO_CHAR, TAR_CHAR_OFFENSIVE, POS_STANDING


def spell_charm_person(sn, level, ch, victim, target):
    if is_safe(ch, victim):
        return

    if victim == ch:
        ch.send("You like yourself even better! \n")
        return

    if ( IS_AFFECTED(victim, AFF_CHARM) \
                 or IS_AFFECTED(ch, AFF_CHARM) \
                 or level < victim.level \
                 or IS_SET(victim.imm_flags, IMM_CHARM) \
                 or saves_spell(level, victim, DAM_CHARM) ):
        return

    if IS_SET(victim.in_room.room_flags, ROOM_LAW):
        ch.send("The mayor does not allow charming in the city limits.\n")
        return

    if victim.master:
        stop_follower(victim)
    add_follower(victim, ch)
    victim.leader = ch
    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = number_fuzzy(level // 4)
    af.location = 0
    af.modifier = 0
    af.bitvector = AFF_CHARM
    victim.affect_add(af)
    act("Isn't $n just so nice?", ch, None, victim, TO_VICT)
    if ch is not victim:
        act("$N looks at you with adoring eyes.", ch, None, victim, TO_CHAR)


register_spell(skill_type("charm person",
                          {'mage': 20, 'cleric': 53, 'thief': 25, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_charm_person, TAR_CHAR_OFFENSIVE, POS_STANDING,
                          None, SLOT(7), 5, 12, "", "You feel more self-confident.", "")
)