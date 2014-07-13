import const
import game_utils
import handler_game
import merc


def spell_pass_door(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_PASS_DOOR):
        if victim == ch:
            ch.send("You are already out of phase.\n")
        else:
            handler_game.act("$N is already shifted out of phase.", ch, None, victim, merc.TO_CHAR)
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = game_utils.number_fuzzy(level // 4)
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_PASS_DOOR
    victim.affect_add(af)
    handler_game.act("$n turns translucent.", victim, None, None, merc.TO_ROOM)
    victim.send("You turn translucent.\n")


const.register_spell(const.skill_type("pass door",
                          {'mage': 24, 'cleric': 32, 'thief': 25, 'warrior': 37},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_pass_door, merc.TAR_CHAR_SELF, merc.POS_STANDING, None,
                          const.SLOT(74), 20, 12, "", "You feel solid again.", ""))
