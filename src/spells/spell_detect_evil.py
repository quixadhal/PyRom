import const
import handler_game
import merc


def spell_detect_evil(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_DETECT_EVIL):
        if victim == ch:
            ch.send("You can already sense evil.\n")
        else:
            handler_game.act("$N can already detect evil.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = merc.APPLY_NONE
    af.bitvector = merc.AFF_DETECT_EVIL
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("detect evil",
                          {'mage': 11, 'cleric': 4, 'thief': 12, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_evil, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(18), 5, 12, "", "The red in your vision disappears.", ""))
