import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import state_checks
import handler_game
import instance


def do_group(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        leader = ch.leader if ch.leader else ch
        ch.send("%s's group:\n" % state_checks.PERS(leader, ch))

        for gch in instance.characters.values():
            if gch.is_same_group(ch):
                ch.send("[[%2d %s]] %-16s %4d/%4d hp %4d/%4d mana %4d/%4d mv %5d xp\n" % (
                    gch.level,
                    "Mob" if state_checks.IS_NPC(gch) else gch.guild.who_name,
                    state_checks.PERS(gch, ch),
                    gch.hit, gch.max_hit,
                    gch.mana, gch.max_mana,
                    gch.move, gch.max_move,
                    gch.exp))
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if ch.master or (ch.leader and ch.leader != ch):
        ch.send("But you are following someone else:!\n")
        return
    if victim.master != ch and ch != victim:
        handler_game.act("$N isn't following you.", ch, None, victim, merc.TO_CHAR, merc.POS_SLEEPING)
        return
    if victim.is_affected( merc.AFF_CHARM):
        ch.send("You can't remove charmed mobs from your group.\n")
        return
    if ch.is_affected(merc.AFF_CHARM):
        handler_game.act("You like your master too much to leave $m!", ch, None, victim, merc.TO_VICT,
                         merc.POS_SLEEPING)
        return
    if victim.is_same_group(ch) and ch != victim:
        victim.leader = None
        handler_game.act("$n removes $N from $s group.", ch, None, victim, merc.TO_NOTVICT, merc.POS_RESTING)
        handler_game.act("$n removes you from $s group.", ch, None, victim, merc.TO_VICT, merc.POS_SLEEPING)
        handler_game.act("You remove $N from your group.", ch, None, victim, merc.TO_CHAR, merc.POS_SLEEPING)
        return
    victim.leader = ch
    handler_game.act("$N joins $n's group.", ch, None, victim, merc.TO_NOTVICT, merc.POS_RESTING)
    handler_game.act("You join $n's group.", ch, None, victim, merc.TO_VICT, merc.POS_SLEEPING)
    handler_game.act("$N joins your group.", ch, None, victim, merc.TO_CHAR, merc.POS_SLEEPING)
    return


interp.register_command(interp.cmd_type('group', do_group, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
