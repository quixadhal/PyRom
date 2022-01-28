import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import handler_game
from rom24 import state_checks
from rom24 import instance


# Thanks to Grodyn for pointing out bugs in this function.
def do_force(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg or not argument:
        ch.send("Force whom to do what?\n")
        return
    temp, arg2 = game_utils.read_word(argument)
    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    buf = "$n forces you to '%s'." % argument
    if arg == "all":
        if ch.trust < merc.MAX_LEVEL - 3:
            ch.send("Not at your level!\n")
            return
        for vch in instance.characters.values():
            if not vch.is_npc() and vch.trust < ch.trust:
                handler_game.act(buf, ch, None, vch, merc.TO_VICT)
                vch.interpret(argument)
    elif arg == "players":
        if ch.trust < merc.MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in instance.characters.values():
            if (
                not vch.is_npc()
                and vch.trust < ch.trust
                and vch.level < merc.LEVEL_HERO
            ):
                handler_game.act(buf, ch, None, vch, merc.TO_VICT)
                vch.interpret(argument)
    elif arg == "gods":
        if ch.trust < merc.MAX_LEVEL - 2:
            ch.send("Not at your level!\n")
            return
        for vch in instance.characters.values():
            if (
                not vch.is_npc()
                and vch.trust < ch.trust
                and vch.level >= merc.LEVEL_HERO
            ):
                handler_game.act(buf, ch, None, vch, merc.TO_VICT)
                vch.interpret(argument)
    else:
        victim = ch.get_char_world(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if (
            not ch.is_room_owner(victim.in_room)
            and ch.in_room != victim.in_room
            and victim.in_room.is_private()
            and not state_checks.IS_TRUSTED(ch, merc.MAX_LEVEL)
        ):
            ch.send("That character is in a private room.\n")
            return
        if victim.is_pc and victim.trust >= ch.trust:
            ch.send("Do it yourself!\n")
            return
        if not victim.is_npc() and ch.trust < merc.MAX_LEVEL - 3:
            ch.send("Not at your level!\n")
            return
        handler_game.act(buf, ch, None, victim, merc.TO_VICT)
        # TODO: Known broken. NPCs don't have interpret, so we'll have to figure this out.
        victim.interpret(argument)
    ch.send("Ok.\n")
    return


interp.register_command(
    interp.cmd_type("force", do_force, merc.POS_DEAD, merc.L7, merc.LOG_ALWAYS, 1)
)
