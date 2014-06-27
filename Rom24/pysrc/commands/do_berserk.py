import logging

logger = logging.getLogger()

import random
import merc
import const
import fight
import interp
import skills


def do_berserk(ch, argument):
    chance = ch.get_skill('berserk')
    if chance == 0 or (merc.IS_NPC(ch) and not merc.IS_SET(ch.off_flags, merc.OFF_BERSERK)) \
            or (not merc.IS_NPC(ch) and ch.level < const.skill_table['berserk'].skill_level[ch.guild.name]):
        ch.send("You turn red in the face, but nothing happens.\n")
        return

    if merc.IS_AFFECTED(ch, merc.AFF_BERSERK) or merc.is_affected(ch, 'berserk') or merc.is_affected(ch, "frenzy"):
        ch.send("You get a little madder.\n")
        return
    if merc.IS_AFFECTED(ch, merc.AFF_CALM):
        ch.send("You're feeling to mellow to berserk.\n")
        return
    if ch.mana < 50:
        ch.send("You can't get up enough energy.\n")
        return
    # modifiers
    # fighting
    if ch.position == merc.POS_FIGHTING:
        chance += 10

    # damage -- below 50% of hp helps, above hurts
    hp_percent = 100 * ch.hit // ch.max_hit
    chance += 25 - hp_percent // 2

    if random.randint(1, 99) < chance:
        merc.WAIT_STATE(ch, merc.PULSE_VIOLENCE)
        ch.mana -= 50
        ch.move //= 2
        # heal a little damage
        ch.hit += ch.level * 2
        ch.hit = min(ch.hit, ch.max_hit)
        ch.send("Your pulse races as you are consumed by rage!\n")
        merc.act("$n gets a wild look in $s eyes.", ch, None, None, merc.TO_ROOM)
        skills.check_improve(ch, 'berserk', True, 2)
        af = merc.AFFECT_DATA()
        af.where = merc.TO_AFFECTS
        af.type = 'berserk'
        af.level = ch.level
        af.duration = merc.number_fuzzy(ch.level // 8)
        af.modifier = max(1, ch.level // 5)
        af.bitvector = merc.AFF_BERSERK

        af.location = merc.APPLY_HITROLL
        ch.affect_add(af)

        af.location = merc.APPLY_DAMROLL
        ch.affect_add(af)

        af.modifier = max(10, 10 * (ch.level // 5))
        af.location = merc.APPLY_AC
        ch.affect_add(af)
    else:
        merc.WAIT_STATE(ch, 3 * merc.PULSE_VIOLENCE)
        ch.mana -= 25
        ch.move //= 2

        ch.send("Your pulse speeds up, but nothing happens.\n")
        fight.check_improve(ch, 'berserk', False, 2)


interp.register_command(interp.cmd_type('berserk', do_berserk, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 1))
