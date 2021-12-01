import const
import handler_game
import merc


def spell_detect_good(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_DETECT_GOOD):
        if victim == ch:
            ch.send("You can already sense good.\n")
        else:
            handler_game.act("$N can already detect good.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = merc.APPLY_NONE
    af.bitvector = merc.AFF_DETECT_GOOD
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("detect good",
                          {'mage': 11, 'cleric': 4, 'thief': 12, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_good, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(513), 5, 12, "", "The gold in your vision disappears.", ""))
