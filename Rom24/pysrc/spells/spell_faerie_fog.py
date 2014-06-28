from const import SLOT, skill_type
from merc import act, TO_ROOM, saves_spell, DAM_OTHER, REMOVE_BIT, AFF_HIDE, AFF_INVISIBLE, AFF_SNEAK, POS_STANDING, \
    TAR_IGNORE


def spell_faerie_fog(sn, level, ch, victim, target):
    act("$n conjures a cloud of purple smoke.", ch, None, None, TO_ROOM)
    ch.send("You conjure a cloud of purple smoke.\n")

    for ich in ch.in_room.people:
        if ich.invis_level > 0:
            continue

        if ich == ch or saves_spell(level, ich, DAM_OTHER):
            continue

        ich.affect_strip('invis')
        ich.affect_strip('mass_invis')
        ich.affect_strip('sneak')
        REMOVE_BIT(ich.affected_by, AFF_HIDE)
        REMOVE_BIT(ich.affected_by, AFF_INVISIBLE)
        REMOVE_BIT(ich.affected_by, AFF_SNEAK)
        act("$n is revealed! ", ich, None, None, TO_ROOM)
        ich.send("You are revealed! \n")

skill_type("faerie fog",
           { 'mage':14, 'cleric':21, 'thief':16, 'warrior':24 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_faerie_fog, TAR_IGNORE, POS_STANDING, None,
           SLOT(73), 12, 12, "faerie fog", "!Faerie Fog!", "")