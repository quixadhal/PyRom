import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_weaken(sn, level, ch, victim, target):
    if state_checks.is_affected(victim, sn) or handler_magic.saves_spell(level, victim, merc.DAM_OTHER):
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = level // 2
    af.location = merc.APPLY_STR
    af.modifier = -1 * (level // 5)
    af.bitvector = merc.AFF_WEAKEN
    victim.affect_add(af)
    victim.send("You feel your strength slip away.\n")
    handler_game.act("$n looks tired and weak.", victim, None, None, merc.TO_ROOM)


const.register_spell(const.skill_type("weaken",
                          {'mage': 11, 'cleric': 14, 'thief': 16, 'warrior': 17},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_weaken, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING, None,
                          const.SLOT(68), 20, 12, "spell", "You feel stronger.", ""))
