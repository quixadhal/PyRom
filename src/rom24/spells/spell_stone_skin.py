import const
import handler_game
import merc
import state_checks


def spell_stone_skin(sn, level, ch, victim, target):
    if state_checks.is_affected(ch, sn):
        if victim == ch:
            ch.send("Your skin is already as hard as a rock.\n")
        else:
            handler_game.act("$N is already as hard as can be.", ch, None, victim, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = merc.APPLY_AC
    af.modifier = -40
    af.bitvector = 0
    victim.affect_add(af)
    handler_game.act("$n's skin turns to stone.", victim, None, None, merc.TO_ROOM)
    victim.send("Your skin turns to stone.\n")


const.register_spell(const.skill_type("stone skin",
                          {'mage': 25, 'cleric': 40, 'thief': 40, 'warrior': 45},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_stone_skin, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(66), 12, 18, "", "Your skin feels soft again.", ""))
