from const import SLOT, skill_type, skill_table
from fight import damage
from merc import IS_EVIL, act, TO_ROOM, IS_GOOD, dice, saves_spell, DAM_HOLY, TARGET_CHAR, TAR_CHAR_OFFENSIVE, \
    POS_FIGHTING
from spells.spell_blindness import spell_blindness


def spell_ray_of_truth(sn, level, ch, victim, target):
    if IS_EVIL(ch):
        victim = ch
        ch.send("The energy explodes inside you! \n")
    if victim != ch:
        act("$n raises $s hand, and a blinding ray of light shoots forth! ", ch, None, None, TO_ROOM)
        ch.send("You raise your hand and a blinding ray of light shoots forth! \n")

    if IS_GOOD(victim):
        act("$n seems unharmed by the light.", victim, None, victim, TO_ROOM)
        victim.send("The light seems powerless to affect you.\n")
        return

    dam = dice(level, 10)
    if saves_spell(level, victim, DAM_HOLY):
        dam = dam // 2

    align = victim.alignment
    align -= 350

    if align < -1000:
        align = -1000 + (align + 1000) // 3

    dam = (dam * align * align) // 1000000

    damage(ch, victim, dam, sn, DAM_HOLY, True)
    skill_table['blindness'].spell_fun('blindness', 3 * level // 4, ch, victim, TARGET_CHAR)

skill_type("ray of truth",
           { 'mage':53, 'cleric':35, 'thief':53, 'warrior':47 },
           { 'mage':1, 'cleric':1, 'thief':2, 'warrior':2 },
           spell_ray_of_truth, TAR_CHAR_OFFENSIVE, POS_FIGHTING,
           None, SLOT(518), 20, 12, "ray of truth", "!Ray of Truth!", "")