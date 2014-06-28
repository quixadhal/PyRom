import const
import handler_game
import merc
import state_checks


def spell_armor(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn):
        if victim == ch:
            ch.send("You are already armored.\n")
        else:
            handler_game.act("$N is already armored.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 24
    af.modifier = -20
    af.location = merc.APPLY_AC
    af.bitvector = 0
    victim.affect_add(af)
    victim.send("You feel someone protecting you.\n")
    if ch is not victim:
        handler_game.act("$N is protected by your magic.", ch, None, victim, merc.TO_CHAR)


const.register_spell(const.skill_type("armor",
                          {'mage': 7, 'cleric': 2, 'thief': 10, 'warrior': 5},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_armor, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(1), 5, 12, "", "You feel less armored.", ""))
