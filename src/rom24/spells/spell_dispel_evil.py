import const
import fight
import game_utils
import handler_game
import handler_magic
import merc
import state_checks


def spell_dispel_evil(sn, level, ch, victim, target):
    if not ch.is_npc() and ch.is_evil():
        victim = ch

    if state_checks.IS_GOOD(victim):
        handler_game.act("Mota protects $N.", ch, None, victim, merc.TO_ROOM)
        return

    if state_checks.IS_NEUTRAL(victim):
        handler_game.act("$N does not seem to be affected.", ch, None, victim, merc.TO_CHAR)
        return

    if victim.hit > (ch.level * 4):
        dam = game_utils.dice(level, 4)
    else:
        dam = max(victim.hit, game_utils.dice(level, 4))
    if handler_magic.saves_spell(level, victim, merc.DAM_HOLY):
        dam = dam // 2
    fight.damage(ch, victim, dam, sn, merc.DAM_HOLY, True)


const.register_spell(const.skill_type("dispel evil",
                          {'mage': 53, 'cleric': 15, 'thief': 53, 'warrior': 21},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_dispel_evil, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(22), 15, 12, "dispel evil", "!Dispel Evil!", ""))
