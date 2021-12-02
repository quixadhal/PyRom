import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import game_utils
from rom24 import instance
from rom24 import interp
from rom24 import state_checks


distance = [
    "right here.",
    "nearby to the %s.",
    "not far %s.",
    "off in the distance %s.",
]

# Thanks to Zrin for auto-exit part.
def do_scan(ch, argument):
    argument, arg1 = game_utils.read_word(argument)

    if not arg1:
        handler_game.act("$n looks all around.", ch, None, None, merc.TO_ROOM)
        ch.send("Looking around you see:\n")
        scan_list(ch.in_room, ch, 0, -1)

        for door, pexit in enumerate(ch.in_room.exit):
            if pexit is not None and pexit.to_room:
                scan_room = instance.rooms[pexit.to_room]
                scan_list(scan_room, ch, 1, door)
        return

    if arg1.startswith("n"):
        door = 0
    elif arg1.startswith("e"):
        door = 1
    elif arg1.startswith("s"):
        door = 2
    elif arg1.startswith("w"):
        door = 3
    elif arg1.startswith("u"):
        door = 4
    elif arg1.startswith("d"):
        door = 5
    else:
        ch.send("Which way do you want to scan?\n")
        return

    handler_game.act(
        "You peer intently $T.", ch, None, merc.dir_name[door], merc.TO_CHAR
    )
    handler_game.act(
        "$n peers intently $T.", ch, None, merc.dir_name[door], merc.TO_ROOM
    )

    scan_room = ch.in_room

    for depth in range(1, 4):
        pexit = scan_room.exit[door]
        if pexit:
            scan_room = instance.rooms[pexit.to_room]
            scan_list(scan_room, ch, depth, door)

    return


def scan_list(scan_room, ch, depth, door):
    if not scan_room:
        return

    for person_id in scan_room.people:
        person = instance.characters[person_id]
        if person == ch:
            continue
        if person.is_pc and person.invis_level > ch.trust:
            continue
        if ch.can_see(person):
            scan_ch(person, ch, depth, door)
    return


def scan_ch(victim, ch, depth, door):
    buf = state_checks.PERS(victim, ch)
    buf = buf + ", "
    if door != -1:
        buf2 = distance[depth] % (merc.dir_name[door])
    else:
        buf2 = distance[depth]
    buf = buf + buf2 + "\n"
    ch.send(buf)
    return


interp.register_command(
    interp.cmd_type("scan", do_scan, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1)
)
