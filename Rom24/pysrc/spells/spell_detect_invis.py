import const
import handler_game
import merc


def spell_detect_invis(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_DETECT_INVIS):
        if victim == ch:
            ch.send("You can already see invisible.\n")
        else:
            handler_game.act("$N can already see invisible things.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = merc.APPLY_NONE
    af.bitvector = merc.AFF_DETECT_INVIS
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("detect invis",
                          {'mage': 3, 'cleric': 8, 'thief': 6, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_invis, merc.TAR_CHAR_SELF, merc.POS_STANDING,
                          None, const.SLOT(19), 5, 12, "", "You no longer see invisible objects.", ""))
