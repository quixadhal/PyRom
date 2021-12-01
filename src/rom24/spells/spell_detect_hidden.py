import const
import handler_game
import merc


def spell_detect_hidden(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_DETECT_HIDDEN):
        if victim == ch:
            ch.send("You are already as alert as you can be. \n")
        else:
            handler_game.act("$N can already sense hidden lifeforms.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_DETECT_HIDDEN
    victim.affect_add(af)
    victim.send("Your awareness improves.\n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("detect hidden",
                          {'mage': 15, 'cleric': 11, 'thief': 12, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_hidden, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(44), 5, 12, "", "You feel less aware of your surroundings.", ""))
