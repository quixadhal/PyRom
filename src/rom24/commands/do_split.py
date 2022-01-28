import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import handler_game
from rom24 import state_checks
from rom24 import instance

# 'Split' originally by Gnort, God of Chaos.
def do_split(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    if not arg1:
        ch.send("Split how much?\n")
        return
    amount_gold = 0
    amount_silver = 0

    if arg1.isdigit():
        amount_silver = int(arg1)
    if arg2.isdigit():
        amount_gold = int(arg2)
    if amount_gold < 0 or amount_silver < 0:
        ch.send("Your group wouldn't like that.\n")
        return
    if amount_gold == 0 and amount_silver == 0:
        ch.send("You hand out zero coins, but no one notices.\n")
        return
    if ch.gold < amount_gold or ch.silver < amount_silver:
        ch.send("You don't have that much to split.\n")
        return
    members = 0
    for gch_id in ch.in_room.people:
        gch = instance.characters[gch_id]
        if gch.is_same_group(ch) and not state_checks.IS_AFFECTED(gch, merc.AFF_CHARM):
            members += 1
    if members < 2:
        ch.send("Just keep it all.\n")
        return
    share_silver = amount_silver // members
    extra_silver = amount_silver % members
    share_gold = amount_gold // members
    extra_gold = amount_gold % members
    if share_gold == 0 and share_silver == 0:
        ch.send("Don't even bother, cheapskate.\n")
        return
    ch.silver -= amount_silver
    ch.silver += share_silver + extra_silver
    ch.gold -= amount_gold
    ch.gold += share_gold + extra_gold
    if share_silver > 0:
        ch.send(
            "You split %d silver coins. Your share is %d silver.\n"
            % (amount_silver, share_silver + extra_silver)
        )
    if share_gold > 0:
        ch.send(
            "You split %d gold coins. Your share is %d gold.\n"
            % (amount_gold, share_gold + extra_gold)
        )
    if share_gold == 0:
        buf = "$n splits %d silver coins. Your share is %d silver." % (
            amount_silver,
            share_silver,
        )
    elif share_silver == 0:
        buf = "$n splits %d gold coins. Your share is %d gold." % (
            amount_gold,
            share_gold,
        )
    else:
        buf = (
            "$n splits %d silver and %d gold coins, giving you %d silver and %d gold.\n"
            % (amount_silver, amount_gold, share_silver, share_gold)
        )

    for gch_id in ch.in_room.people:
        gch = instance.characters[gch_id]
        if (
            gch != ch
            and gch.is_same_group(ch)
            and not state_checks.IS_AFFECTED(gch, merc.AFF_CHARM)
        ):
            handler_game.act(buf, ch, None, gch, merc.TO_VICT)
            gch.gold += share_gold
            gch.silver += share_silver
    return


interp.register_command(
    interp.cmd_type("split", do_split, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
