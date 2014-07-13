import const
import handler_game
import merc


def spell_protection_good(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_PROTECT_GOOD) or victim.is_affected(
                                                                                           merc.AFF_PROTECT_EVIL):
        if victim == ch:
            ch.send("You are already protected.\n")
        else:
            handler_game.act("$N is already protected.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 24
    af.location = merc.APPLY_SAVING_SPELL
    af.modifier = -1
    af.bitvector = merc.AFF_PROTECT_GOOD
    victim.affect_add(af)
    victim.send("You feel aligned with darkness.\n")
    if ch != victim:
        handler_game.act("$N is protected from good.", ch, None, victim, merc.TO_CHAR)


const.register_spell(const.skill_type("protection good",
                          {'mage': 12, 'cleric': 9, 'thief': 17, 'warrior': 11},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_protection_good, merc.TAR_CHAR_SELF, merc.POS_STANDING,
                          None, const.SLOT(514), 5, 12, "", "You feel less protected.", ""))
