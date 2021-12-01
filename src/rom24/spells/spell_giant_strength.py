import const
import handler_game
import merc
import state_checks


def spell_giant_strength(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already as strong as you can get! \n")
        else:
            handler_game.act("$N can't get any stronger.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = merc.APPLY_STR
    af.modifier = 1 + (level >= 18) + (level >= 25) + (level >= 32)
    af.bitvector = 0
    victim.affect_add(af)
    victim.send("Your muscles surge with heightened power! \n")
    handler_game.act("$n's muscles surge with heightened power.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("giant strength",
                          {'mage': 11, 'cleric': 53, 'thief': 22, 'warrior': 20},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_giant_strength, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(39), 20, 12, "", "You feel weaker.", ""))
