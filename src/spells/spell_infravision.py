import const
import handler_game
import merc


def spell_infravision(sn, level, ch, victim, target):
    if victim.is_affected(merc.AFF_INFRARED):
        if victim == ch:
            ch.send("You can already see in the dark.\n")
        else:
            handler_game.act("$N already has infravision.\n", ch, None, victim, merc.TO_CHAR)
        return

    handler_game.act("$n's eyes glow red.\n", ch, None, None, merc.TO_ROOM)
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 2 * level
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_INFRARED
    victim.affect_add(af)
    victim.send("Your eyes glow red.\n")
    return


const.register_spell(const.skill_type("infravision",
                          {'mage': 9, 'cleric': 13, 'thief': 10, 'warrior': 16},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_infravision, merc.TAR_CHAR_DEFENSIVE, merc.POS_STANDING,
                          None, const.SLOT(77), 5, 18, "", "You no longer see in the dark.", ""))
