import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks


#TODO: Known broken.
def do_switch(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Switch into whom?\n")
        return
    if not ch.desc is None:
        return
    if ch.desc.original:
        ch.send("You are already switched.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if victim == ch:
        ch.send("Ok.\n")
        return
    if not victim.is_npc():
        ch.send("You can only switch into mobiles.\n")
        return
    if not ch.is_room_owner(victim.in_room) and ch.in_room != victim.in_room \
            and victim.in_room.is_private() and not state_checks.IS_TRUSTED(ch, merc.MAX_LEVEL):
        ch.send("That character is in a private room.\n")
        return
    if victim.desc:
        ch.send("Character in use.\n")
        return

    handler_game.wiznet("$N switches into %s" % victim.short_descr, ch, None, merc.WIZ_SWITCHES, merc.WIZ_SECURE,
                ch.trust)

    ch.desc.character = victim
    ch.desc.original = ch
    victim.desc = ch.desc
    ch.desc = None
    # change communications to match
    if ch.prompt:
        victim.prompt = ch.prompt
    victim.comm = ch.comm
    victim.lines = ch.lines
    victim.send("Ok.\n")
    return


interp.register_command(interp.cmd_type('switch', do_switch, merc.POS_DEAD, merc.L6, merc.LOG_ALWAYS, 1))
