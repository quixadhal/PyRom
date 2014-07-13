import random

import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_change_sex(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn):
        if victim == ch:
            ch.send("You've already been changed.\n")
        else:
            handler_game.act("$N has already had $s(?) sex changed.", ch, None, victim, merc.TO_CHAR)
        return

    if handler_magic.saves_spell(level, victim, merc.DAM_OTHER):
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = merc.APPLY_SEX

    while af.modifier == 0:
        af.modifier = random.randint(0, 2) - victim.sex

    af.bitvector = 0
    victim.affect_add(af)
    victim.send("You feel different.\n")
    handler_game.act("$n doesn't look like $mself anymore...", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("change sex",
                          {'mage': 53, 'cleric': 53, 'thief': 53, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_change_sex, merc.TAR_CHAR_DEFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(82), 15, 12, "", "Your body feels familiar again.", ""))
