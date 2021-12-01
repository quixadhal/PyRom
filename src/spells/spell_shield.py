import const
import handler_game
import merc
import state_checks


def spell_shield(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already shielded from harm.\n")
        else:
            handler_game.act("$N is already protected by a shield.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 8 + level
    af.location = merc.APPLY_AC
    af.modifier = -20
    af.bitvector = 0
    victim.affect_add(af)
    handler_game.act("$n is surrounded by a force shield.", victim, None, None, merc.TO_ROOM)
    victim.send("You are surrounded by a force shield.\n")
    return


const.register_spell(const.skill_type("shield",
                          {'mage': 20, 'cleric': 35, 'thief': 35, 'warrior': 40},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_shield, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING, None,
                          const.SLOT(67), 12, 18, "", "Your force shield shimmers then fades away.", ""))
