import const
import handler_game
import handler_magic
import merc
import state_checks


def spell_sleep(sn, level, ch, victim, target):
    if victim.is_affected( merc.AFF_SLEEP) \
            or (victim.is_npc() and victim.act.is_set(merc.ACT_UNDEAD)) \
            or (level + 2) < victim.level \
            or handler_magic.saves_spell(level - 4, victim, merc.DAM_CHARM):
        return
    af = handler_game.AFFECT_DATA()
    af.where = merc.TO_AFFECTS
    af.type = sn
    af.level = level
    af.duration = 4 + level
    af.location = merc.APPLY_NONE
    af.modifier = 0
    af.bitvector = merc.AFF_SLEEP
    victim.affect_join(af)

    if state_checks.IS_AWAKE(victim):
        victim.send("You feel very sleepy ..... zzzzzz.\n")
        handler_game.act("$n goes to sleep.", victim, None, None, merc.TO_ROOM)
        victim.position = merc.POS_SLEEPING


const.register_spell(const.skill_type("sleep",
                          {'mage': 10, 'cleric': 53, 'thief': 11, 'warrior': 53},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_sleep, merc.TAR_CHAR_OFFENSIVE, merc.POS_STANDING, None,
                          const.SLOT(38), 15, 12, "", "You feel less tired.", ""))
