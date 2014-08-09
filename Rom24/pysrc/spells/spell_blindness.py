import const
import handler_game
import handler_magic
import merc


def spell_blindness(sn, level, ch, victim, target):
    if victim.is_affected(merc.AFF_BLIND) or handler_magic.saves_spell(level, victim, merc.DAM_OTHER):
        return

    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.location = merc.APPLY_HITROLL
    af.modifier = -4
    af.duration = 1 + level
    af.bitvector = merc.AFF_BLIND
    victim.affect_add(af)
    victim.send("You are blinded! \n")
    handler_game.act("$n appears to be blinded.", victim, send_to=merc.TO_ROOM)


const.register_spell(const.skill_type("blindness",
                          {'mage': 12, 'cleric': 8, 'thief': 17, 'warrior': 15},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_blindness, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(4), 5, 12, "", "You can see again.", ""))
