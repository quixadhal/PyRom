import logging

logger = logging.getLogger()

import merc
import game_utils
import update
import interp

def do_advance(ch, argument):
    argument, arg1  = game_utils.read_word(argument)
    argument, arg2  = game_utils.read_word(argument)

    if not arg1 or not arg2 or not arg2.isdigit():
        ch.send("Syntax: advance <char> <level>.\n")
        return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("That player is not here.\n")
        return
    if victim.is_npc():
        ch.send("Not on NPC's.\n")
        return
    level = int(arg2)
    if level < 1 or level > merc.MAX_LEVEL:
        ch.send("Level must be 1 to %d.\n" % merc.MAX_LEVEL)
        return
    if level > ch.trust:
        ch.send("Limited to your trust level.\n")
        return

        # Lower level:
        # Reset to level 1.
        # Then raise again.
        #   Currently, an imp can lower another imp.
        #   -- Swiftest

    if level <= victim.level:
        ch.send("Lowering a player's level!\n")
        victim.send("**** OOOOHHHHHHHHHH  NNNNOOOO ****\n")
        temp_prac = victim.practice
        victim.level = 1
        victim.exp = victim.exp_per_level(victim.points)
        victim.max_hit = 10
        victim.max_mana = 100
        victim.max_move = 100
        victim.practice = 0
        victim.hit = victim.max_hit
        victim.mana = victim.max_mana
        victim.move = victim.max_move
        update.advance_level(victim, True)
        victim.practice = temp_prac
    else:
        ch.send("Raising a player's level!\n")
        victim.send("**** OOOOHHHHHHHHHH  YYYYEEEESSS ****\n")
    for iLevel in range(victim.level, level):
        victim.level += 1
        update.advance_level(victim, True)
    victim.send("You are now level %d.\n" % victim.level)
    victim.exp = victim.exp_per_level(victim.points) * max(1, victim.level)
    victim.trust = 0
    victim.save()
    return


interp.register_command(interp.cmd_type('advance', do_advance, merc.POS_DEAD, merc.ML, merc.LOG_ALWAYS, 1))
