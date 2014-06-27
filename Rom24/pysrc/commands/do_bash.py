import logging

logger = logging.getLogger()

import random
import merc
import const
import fight
import interp
import skills


def do_bash(ch, argument):
    arghold, arg = merc.read_word(argument)
    chance = ch.get_skill('bash')
    if chance == 0 or (merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, OFF_BASH)) \
            or (not merc.IS_NPC(ch) and ch.level < const.skill_table['bash'].skill_level[ch.guild.name] ):
        ch.send("Bashing? What's that?\n")
        return
    victim = None
    if not arg:
        victim = ch.fighting
        if not victim:
            ch.send("But you aren't fighting anyone!\n")
            return
    else:
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
    if victim.position < merc.POS_FIGHTING:
        merc.act("You'll have to let $M get back up first.", ch, None, victim, merc.TO_CHAR)
        return
    if victim == ch:
        ch.send("You try to bash your brains out, but fail.\n")
        return
    if fight.is_safe(ch, victim):
        return
    if merc.IS_NPC(victim) and victim.fighting and not ch.is_same_group(victim.fighting):
        ch.send("Kill stealing is not permitted.\n")
        return
    if merc.IS_AFFECTED(ch, merc.AFF_CHARM) and ch.master == victim:
        merc.act("But $N is your friend!", ch, None, victim, merc.TO_CHAR)
        return

    # modifiers
    # size and weight
    chance += ch.carry_weight // 250
    chance -= victim.carry_weight // 200
    if ch.size < victim.size:
        chance += (ch.size - victim.size) * 15
    else:
        chance += (ch.size - victim.size) * 10
    # stats
    chance += ch.get_curr_stat(merc.STAT_STR)
    chance -= (victim.get_curr_stat(merc.STAT_DEX) * 4) // 3
    chance -= merc.GET_AC(victim, merc.AC_BASH) // 25
    # speed
    if merc.IS_SET(ch.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(ch, merc.AFF_HASTE):
        chance += 10
    if merc.IS_SET(victim.off_flags, merc.OFF_FAST) or merc.IS_AFFECTED(victim, merc.AFF_HASTE):
        chance -= 30
    # level
    chance += (ch.level - victim.level)
    if not merc.IS_NPC(victim) and chance < victim.get_skill('dodge'):
        pass
        # act("$n tries to bash you, but you dodge it.",ch,None,victim,TO_VICT)
        # act("$N dodges your bash, you fall flat on your face.",ch,None,victim,TO_CHAR)
        # WAIT_STATE(ch,const.skill_table['bash'].beats)
        # return
        chance -= 3 * (victim.get_skill('dodge') - chance)
    # now the attack
    if random.randint(1, 99) < chance:
        merc.act("$n sends you sprawling with a powerful bash!", ch, None, victim, merc.TO_VICT)
        merc.act("You slam into $N, and send $M flying!", ch, None, victim, merc.TO_CHAR)
        merc.act("$n sends $N sprawling with a powerful bash.", ch, None, victim, merc.TO_NOTVICT)
        skills.check_improve(ch, 'bash', True, 1)
        merc.DAZE_STATE(victim, 3 * merc.PULSE_VIOLENCE)
        merc.WAIT_STATE(ch, const.skill_table['bash'].beats)
        victim.position = merc.POS_RESTING
        fight.damage(ch, victim, random.randint(2, 2 + 2 * ch.size + chance // 20), 'bash', merc.DAM_BASH, False)
    else:
        fight.damage(ch, victim, 0, 'bash', merc.DAM_BASH, False)
        merc.act("You fall flat on your face!", ch, None, victim, merc.TO_CHAR)
        merc.act("$n falls flat on $s face.", ch, None, victim, merc.TO_NOTVICT)
        merc.act("You evade $n's bash, causing $m to fall flat on $s face.", ch, None, victim, merc.TO_VICT)
        skills.check_improve(ch, 'bash', False, 1)
        ch.position = merc.POS_RESTING
        merc.WAIT_STATE(ch, const.skill_table['bash'].beats * 3 // 2)
    fight.check_killer(ch, victim)


interp.register_command(interp.cmd_type('bash', do_bash, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1))
