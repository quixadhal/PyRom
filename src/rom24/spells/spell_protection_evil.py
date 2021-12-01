import const
import handler_game
import merc


def spell_protection_evil(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_PROTECT_EVIL) or victim.is_affected(
                                                                                           merc.AFF_PROTECT_GOOD):
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
    af.bitvector = merc.AFF_PROTECT_EVIL
    victim.affect_add(af)
    victim.send("You feel holy and pure.\n")
    if ch != victim:
        handler_game.act("$N is protected from evil.", ch, None, victim, merc.TO_CHAR)


const.register_spell(const.skill_type("protection evil",
                          {'mage': 12, 'cleric': 9, 'thief': 17, 'warrior': 11},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_protection_evil, merc.TAR_CHAR_SELF, merc.POS_STANDING,
                          None, const.SLOT(34), 5, 12, "", "You feel less protected.", ""))
