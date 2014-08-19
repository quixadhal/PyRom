

import const
import game_utils
import handler_game
import merc
import state_checks


def spell_fireproof(sn, level, ch, victim, target):
    obj = victim
    if obj.flags.burn_proof:
        handler_game.act("$p is already protected from burning.", ch, obj, None, merc.TO_CHAR)
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_OBJECT
    af.type = sn
    af.level = level
    af.duration = game_utils.number_fuzzy(level // 4)
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.ITEM_BURN_PROOF

    obj.affect_add(af)

    handler_game.act("You protect $p from fire.", ch, obj, None, merc.TO_CHAR)
    handler_game.act("$p is surrounded by a protective aura.", ch, obj, None, merc.TO_ROOM)


const.register_spell(const.skill_type("fireproof",
                          {'mage': 13, 'cleric': 12, 'thief': 19, 'warrior': 18},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_fireproof, merc.TAR_OBJ_INV, merc.POS_STANDING, None,
                          const.SLOT(523), 10, 12, "", "", "$p's protective aura fades."))
