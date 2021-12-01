import const
import handler_game
import merc


def spell_faerie_fire(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_FAERIE_FIRE):
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level
    af.location = merc.APPLY_AC
    af.modifier = 2 * level
    af.bitvector = merc.AFF_FAERIE_FIRE
    victim.affect_add(af)
    victim.send("You are surrounded by a pink outline.\n")
    handler_game.act("$n is surrounded by a pink outline.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("faerie fire",
                          {'mage': 6, 'cleric': 3, 'thief': 5, 'warrior': 8},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_faerie_fire, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(72), 5, 12, "faerie fire", "The pink aura around you fades away.", ""))
