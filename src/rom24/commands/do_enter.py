import random
import logging

logger = logging.getLogger(__name__)

from rom24 import handler_game
from rom24 import merc
from rom24 import interp
from rom24 import handler_room
from rom24 import state_checks
from rom24 import instance


# RT Enter portals
def do_enter(ch, argument):
    if ch.fighting:
        return
    # nifty portal stuff
    if argument:
        old_room = ch.in_room
        portal = ch.get_item_list(argument, ch.in_room.items)
        if not portal:
            ch.send("You don't see that here.\n")
            return
        if portal.item_type != merc.ITEM_PORTAL or (
            state_checks.IS_SET(portal.value[1], merc.EX_CLOSED)
            and not state_checks.IS_TRUSTED(ch, merc.L7)
        ):
            ch.send("You can't seem to find a way in.\n")
            return
        if (
            not state_checks.IS_TRUSTED(ch, merc.L7)
            and not state_checks.IS_SET(portal.value[2], merc.GATE_NOCURSE)
            and (
                ch.is_affected(merc.AFF_CURSE)
                or state_checks.IS_SET(old_room.room_flags, merc.ROOM_NO_RECALL)
            )
        ):
            ch.send("Something prevents you from leaving...\n")
            return
        location = None
        if (
            state_checks.IS_SET(portal.value[2], merc.GATE_RANDOM)
            or portal.value[3] == -1
        ):
            location = handler_room.get_random_room(ch)
            portal.value[3] = location.vnum  # for record keeping :)
        elif state_checks.IS_SET(portal.value[2], merc.GATE_BUGGY) and (
            random.randint(1, 99) < 5
        ):
            location = handler_room.get_random_room(ch)
        else:
            location = instance.rooms[portal.value[3]]
        if (
            not location
            or location == old_room
            or not ch.can_see_room(location.instance_id)
            or (
                location.is_private()
                and not state_checks.IS_TRUSTED(ch, merc.MAX_LEVEL)
            )
        ):
            handler_game.act(
                "$p doesn't seem to go anywhere.", ch, portal, None, merc.TO_CHAR
            )
            return
        if (
            ch.is_npc()
            and ch.act.is_set(merc.ACT_AGGRESSIVE)
            and state_checks.IS_SET(location.room_flags, merc.ROOM_LAW)
        ):
            ch.send("Something prevents you from leaving...\n")
            return
        handler_game.act("$n steps into $p.", ch, portal, None, merc.TO_ROOM)

        if state_checks.IS_SET(portal.value[2], merc.GATE_NORMAL_EXIT):
            handler_game.act("You enter $p.", ch, portal, None, merc.TO_CHAR)
        else:
            handler_game.act(
                "You walk through $p and find yourself somewhere else:...",
                ch,
                portal,
                None,
                merc.TO_CHAR,
            )
        ch.in_room.get(ch)
        location.put(ch)
        if state_checks.IS_SET(
            portal.value[2], merc.GATE_GOWITH
        ):  # take the gate along
            portal.get()
            portal.put(location)
        if state_checks.IS_SET(portal.value[2], merc.GATE_NORMAL_EXIT):
            handler_game.act("$n has arrived.", ch, portal, None, merc.TO_ROOM)
        else:
            handler_game.act(
                "$n has arrived through $p.", ch, portal, None, merc.TO_ROOM
            )

        ch.do_look("auto")
        # charges
        if portal.value[0] > 0:
            portal.value[0] -= 1
            if portal.value[0] == 0:
                portal.value[0] = -1
        # protect against circular follows
        if old_room == location:
            return
        for fch_id in old_room.people[:]:
            fch = instance.characters[fch_id]
            if not portal or portal.value[0] == -1:
                # no following through dead portals
                continue
            if (
                fch.master == ch
                and state_checks.IS_AFFECTED(fch, merc.AFF_CHARM)
                and fch.position < merc.POS_STANDING
            ):
                fch.do_stand("")
            if fch.master == ch and fch.position == merc.POS_STANDING:
                if state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_LAW) and (
                    state_checks.IS_NPC(fch) and fch.act.is_set(merc.ACT_AGGRESSIVE)
                ):
                    handler_game.act(
                        "You can't bring $N into the city.", ch, None, fch, merc.TO_CHAR
                    )
                    handler_game.act(
                        "You aren't allowed in the city.", fch, None, None, merc.TO_CHAR
                    )
                    continue
                handler_game.act("You follow $N.", fch, None, ch, merc.TO_CHAR)
                fch.do_enter(argument)
        if portal and portal.value[0] == -1:
            handler_game.act(
                "$p fades out of existence.", ch, portal, None, merc.TO_CHAR
            )
            if ch.in_room == old_room:
                handler_game.act(
                    "$p fades out of existence.", ch, portal, None, merc.TO_ROOM
                )
            elif old_room.people:
                handler_game.act(
                    "$p fades out of existence.",
                    old_room.people,
                    portal,
                    None,
                    merc.TO_CHAR,
                )
                handler_game.act(
                    "$p fades out of existence.",
                    old_room.people,
                    portal,
                    None,
                    merc.TO_ROOM,
                )
            portal.extract()
        return
    ch.send("Nope, can't do it.\n")
    return


interp.register_command(
    interp.cmd_type("enter", do_enter, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1)
)
interp.register_command(
    interp.cmd_type("go", do_enter, merc.POS_STANDING, 0, merc.LOG_NORMAL, 0)
)
