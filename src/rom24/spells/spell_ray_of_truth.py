import const
import fight
import game_utils
import handler_game
import handler_magic
import merc
import state_checks


def spell_ray_of_truth(sn, level, ch, victim, target):
    if ch.is_evil():
        victim = ch
        ch.send("The energy explodes inside you! \n")
    if victim != ch:
        handler_game.act("$n raises $s hand, and a blinding ray of light shoots forth! ", ch, None, None, merc.TO_ROOM)
        ch.send("You raise your hand and a blinding ray of light shoots forth! \n")

    if state_checks.IS_GOOD(victim):
        handler_game.act("$n seems unharmed by the light.", victim, None, victim, merc.TO_ROOM)
        victim.send("The light seems powerless to affect you.\n")
        return

    dam = game_utils.dice(level, 10)
    if handler_magic.saves_spell(level, victim, merc.DAM_HOLY):
        dam = dam // 2

    align = victim.alignment
    align -= 350

    if align < -1000:
        align = -1000 + (align + 1000) // 3

    dam = (dam * align * align) // 1000000

    fight.damage(ch, victim, dam, sn, merc.DAM_HOLY, True)
    const.skill_table['blindness'].spell_fun('blindness', 3 * level // 4, ch, victim, merc.TARGET_CHAR)


const.register_spell(const.skill_type("ray of truth",
                          {'mage': 53, 'cleric': 35, 'thief': 53, 'warrior': 47},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_ray_of_truth, merc.TAR_CHAR_OFFENSIVE, merc.POS_FIGHTING,
                          None, const.SLOT(518), 20, 12, "ray of truth", "!Ray of Truth!", ""))
