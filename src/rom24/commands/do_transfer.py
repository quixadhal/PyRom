import logging

logger = logging.getLogger(__name__)

from rom24 import handler_game
from rom24 import merc
from rom24 import fight
from rom24 import interp
from rom24 import nanny
from rom24 import game_utils


def do_transfer(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    if not arg1:
        ch.send("Transfer whom (and where)?\n")
        return
    if arg1 == "all":
        for d in merc.descriptor_list:
            if (
                d.is_connected(nanny.con_playing)
                and d.character != ch
                and d.character.in_room
                and ch.can_see(d.character)
            ):
                ch.do_transfer("%s %s" % d.character.name, arg2)
        return
    # Thanks to Grodyn for the optional location parameter.
    if not arg2:
        location = ch.in_room
    else:
        location = game_utils.find_location(ch, arg2)
        if not location:
            ch.send("No such location.\n")
            return
        if (
            not ch.is_room_owner(location)
            and location.is_private()
            and ch.trust < merc.MAX_LEVEL
        ):
            ch.send("That room is private right now.\n")
            return
    victim = ch.get_char_world(arg1)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim.in_room is None:
        ch.send("They are in limbo.\n")
        return

    if victim.fighting:
        fight.stop_fighting(victim, True)
    handler_game.act(
        "$n disappears in a mushroom cloud.", victim, None, None, merc.TO_ROOM
    )
    victim.in_room.get(victim)
    location.put(victim)
    handler_game.act(
        "$n arrives from a puff of smoke.", victim, None, None, merc.TO_ROOM
    )
    if ch != victim:
        handler_game.act("$n has transferred you.", ch, None, victim, merc.TO_VICT)
    victim.do_look("auto")
    ch.send("Ok.\n")


interp.register_command(
    interp.cmd_type("teleport", do_transfer, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)
)
interp.register_command(
    interp.cmd_type("transfer", do_transfer, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)
)
