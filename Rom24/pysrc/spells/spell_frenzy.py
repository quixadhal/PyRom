from const import SLOT, skill_type, register_spell
import const
from merc import is_affected, IS_AFFECTED, AFF_BERSERK, act, TO_CHAR, IS_GOOD, IS_NEUTRAL, IS_EVIL, AFFECT_DATA, \
    TO_AFFECTS, APPLY_HITROLL, APPLY_DAMROLL, APPLY_AC, TO_ROOM, TAR_CHAR_DEFENSIVE, POS_STANDING


def spell_frenzy(sn, level, ch, victim, target):
    # RT clerical berserking spell */
    if is_affected(victim, sn) or IS_AFFECTED(victim, AFF_BERSERK):
        if victim == ch:
            ch.send("You are already in a frenzy.\n")
        else:
            act("$N is already in a frenzy.", ch, None, victim, TO_CHAR)
        return

    if is_affected(victim, const.skill_table['calm']):
        if victim == ch:
            ch.send("Why don't you just relax for a while?\n")
        else:
            act("$N doesn't look like $e wants to fight anymore.", ch, None, victim, TO_CHAR)
        return
    if (IS_GOOD(ch) and not IS_GOOD(victim)) or \
            (IS_NEUTRAL(ch) and not IS_NEUTRAL(victim)) or \
            (IS_EVIL(ch) and not IS_EVIL(victim)):
        act("Your god doesn't seem to like $N", ch, None, victim, TO_CHAR)
        return

    af = AFFECT_DATA()
    af.where = TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 3
    af.modifier = level // 6
    af.bitvector = 0

    af.location = APPLY_HITROLL
    victim.affect_add(af)

    af.location = APPLY_DAMROLL
    victim.affect_add(af)

    af.modifier = 10 * (level // 12)
    af.location = APPLY_AC
    victim.affect_add(af)

    victim.send("You are filled with holy wrath! \n")
    act("$n gets a wild look in $s eyes! ", victim, None, None, TO_ROOM)


register_spell(skill_type("frenzy",
                          {'mage': 53, 'cleric': 24, 'thief': 53, 'warrior': 26},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_frenzy, TAR_CHAR_DEFENSIVE, POS_STANDING, None,
                          SLOT(504), 30, 24, "", "Your rage ebbs.", ""))