import const
import handler_game
import merc


def spell_sanctuary(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_SANCTUARY):
        if victim == ch:
            ch.send("You are already in sanctuary.\n")
        else:
            handler_game.act("$N is already in sanctuary.", ch, None, victim, merc.TO_CHAR)
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 6
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_SANCTUARY
    victim.affect_add(af)
    handler_game.act("$n is surrounded by a white aura.", victim, None, None, merc.TO_ROOM)
    victim.send("You are surrounded by a white aura.\n")


const.register_spell(const.skill_type("sanctuary",
                          {'mage': 36, 'cleric': 20, 'thief': 42, 'warrior': 30},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_sanctuary, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING, None,
                          const.SLOT(36), 75, 12, "", "The white aura around your body fades.", ""))
