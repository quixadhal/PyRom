import const
import handler_game
import merc


def spell_detect_magic(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_DETECT_MAGIC):
        if victim == ch:
            ch.send("You can already sense magical auras.\n")
        else:
            handler_game.act("$N can already detect magic.", ch, None, victim, merc.TO_CHAR)
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.modifier = 0
    af.location = merc.APPLY_NONE
    af.bitvector = merc.AFF_DETECT_MAGIC
    victim.affect_add(af)
    victim.send("Your eyes tingle.\n")
    if ch != victim:
        ch.send("Ok.\n")


const.register_spell(const.skill_type("detect magic",
                          {'mage': 2, 'cleric': 6, 'thief': 5, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_detect_magic, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(20), 5, 12, "", "The detect magic wears off.", ""))
