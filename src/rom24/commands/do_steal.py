import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import fight
from rom24 import game_utils
from rom24 import handler_game
from rom24 import state_checks
from rom24 import const


def do_steal(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)

    if not arg1 or not arg2:
        ch.send("Steal what from whom?\n")
        return
    victim = ch.get_char_room(arg2)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim == ch:
        ch.send("That's pointless.\n")
        return
    if fight.is_safe(ch, victim):
        return

    if victim.is_npc() and victim.position == merc.POS_FIGHTING:
        ch.send(
            "Kill stealing is not permitted.\nYou'd better not -- you might get hit.\n"
        )
        return
    state_checks.WAIT_STATE(ch, const.skill_table["steal"].beats)
    percent = random.randint(1, 99)

    if not state_checks.IS_AWAKE(victim):
        percent -= 10
    elif not victim.can_see(ch):
        percent += 25
    else:
        percent += 50

    if (
        (
            (ch.level + 7 < victim.level or ch.level - 7 > victim.level)
            and not victim.is_npc()
            and not ch.is_npc()
        )
        or (not ch.is_npc() and percent > ch.get_skill("steal"))
        or (not ch.is_npc() and not ch.is_clan())
    ):
        # Failure.
        ch.send("Oops.\n")
        ch.affect_strip("sneak")
        ch.affected_by = ch.affected_by.rem_bit(merc.AFF_SNEAK)
        handler_game.act(
            "$n tried to steal from you.\n", ch, None, victim, merc.TO_VICT
        )
        handler_game.act(
            "$n tried to steal from $N.\n", ch, None, victim, merc.TO_NOTVICT
        )
        outcome = random.randint(0, 3)
        buf = ""
        if outcome == 0:
            buf = "%s is a lousy thief!" % ch.name
        elif outcome == 1:
            buf = "%s couldn't rob %s way out of a paper bag!" % (
                ch.name,
                ("her" if ch.sex == 2 else "his"),
            )
        elif outcome == 2:
            buf = "%s tried to rob me!" % ch.name
        elif outcome == 3:
            buf = "Keep your hands out of there, %s!" % ch.name
        if not state_checks.IS_AWAKE(victim):
            victim.do_wake("")
        if state_checks.IS_AWAKE(victim):
            victim.do_yell(buf)
        if not ch.is_npc():
            if victim.is_npc():
                if ch.is_pc:
                    ch.check_improve("steal", False, 2)
                fight.multi_hit(victim, ch, merc.TYPE_UNDEFINED)
            else:
                handler_game.wiznet(
                    "$N tried to steal from %s." % victim.name,
                    ch,
                    None,
                    merc.WIZ_FLAGS,
                    0,
                    0,
                )
                if not ch.act.is_set(merc.PLR_THIEF):
                    ch.act.set_bit(merc.PLR_THIEF)
                    ch.send("*** You are now a THIEF!! ***\n")
                    ch.save()
        return
    currency = ["coins", "coin", "gold", "silver"]
    if arg1 in currency:
        gold = victim.gold * random.randint(1, ch.level) // merc.MAX_LEVEL
        silver = victim.silver * random.randint(1, ch.level) // merc.MAX_LEVEL
        if gold <= 0 and silver <= 0:
            ch.send("You couldn't get any coins.\n")
            return
        ch.gold += gold
        ch.silver += silver
        victim.silver -= silver
        victim.gold -= gold
        if silver <= 0:
            ch.send("Bingo!  You got %d gold coins.\n" % gold)
        elif gold <= 0:
            ch.send("Bingo!  You got %d silver coins.\n" % silver)
        else:
            ch.send("Bingo!  You got %d silver and %d gold coins.\n" % (silver, gold))
        if ch.is_pc:
            ch.check_improve("steal", True, 2)
        return
    item = victim.get_item_carry(arg1, ch)
    if not item:
        ch.send("You can't find it.\n")
        return
    if not ch.can_drop_item(item) or item.flags.shop_inventory or item.level > ch.level:
        ch.send("You can't pry it away.\n")
        return
    if ch.carry_number + item.get_number() > ch.can_carry_n():
        ch.send("You have your hands full.\n")
        return
    if ch.carry_weight + item.get_weight() > ch.can_carry_w():
        ch.send("You can't carry that much weight.\n")
        return
    item.get()
    ch.put(item)
    handler_game.act("You pocket $p.", ch, item, None, merc.TO_CHAR)
    if ch.is_pc:
        ch.check_improve("steal", True, 2)
    ch.send("Got it!\n")
    return


interp.register_command(
    interp.cmd_type("steal", do_steal, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1)
)
