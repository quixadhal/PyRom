import logging

logger = logging.getLogger()

import random
import merc
import interp


# RT Enter portals
def do_enter(ch, argument):
    if ch.fighting:
        return
    # nifty portal stuff
    if argument:
        old_room = ch.in_room
        portal = ch.get_obj_list(argument, ch.in_room.contents)
        if not portal:
            ch.send("You don't see that here.\n")
            return
        if portal.item_type != merc.ITEM_PORTAL \
                or (merc.IS_SET(portal.value[1], merc.EX_CLOSED) and not merc.IS_TRUSTED(ch, merc.L7)):
            ch.send("You can't seem to find a way in.\n")
            return
        if not merc.IS_TRUSTED(ch, merc.L7) and not merc.IS_SET(portal.value[2], merc.GATE_NOCURSE) \
                and (merc.IS_AFFECTED(ch, merc.AFF_CURSE) or merc.IS_SET(old_room.room_flags, merc.ROOM_NO_RECALL)):
            ch.send("Something prevents you from leaving...\n")
            return
        location = None
        if merc.IS_SET(portal.value[2], merc.GATE_RANDOM) or portal.value[3] == -1:
            location = merc.get_random_room(ch)
            portal.value[3] = location.vnum  # for record keeping :)
        elif merc.IS_SET(portal.value[2], merc.GATE_BUGGY) and (random.randint(1, 99) < 5):
            location = merc.get_random_room(ch)
        else:
            location = merc.room_index_hash[portal.value[3]]
        if not location or location == old_room \
                or not ch.can_see_room(location) \
                or (location.is_private() and not merc.IS_TRUSTED(ch, merc.MAX_LEVEL)):
            merc.act("$p doesn't seem to go anywhere.", ch, portal, None, merc.TO_CHAR)
            return
        if merc.IS_NPC(ch) and merc.IS_SET(ch.act, merc.ACT_AGGRESSIVE) \
                and merc.IS_SET(location.room_flags, merc.ROOM_LAW):
            ch.send("Something prevents you from leaving...\n")
            return
        merc.act("$n steps into $p.", ch, portal, None, merc.TO_ROOM)

        if merc.IS_SET(portal.value[2], merc.GATE_NORMAL_EXIT):
            merc.act("You enter $p.", ch, portal, None, merc.TO_CHAR)
        else:
            merc.act("You walk through $p and find yourself somewhere else:...", ch, portal, None, merc.TO_CHAR)
        ch.from_room()
        ch.to_room(location)
        if merc.IS_SET(portal.value[2], merc.GATE_GOWITH):  # take the gate along
            portal.from_room()
            portal.to_room(location)
        if merc.IS_SET(portal.value[2], merc.GATE_NORMAL_EXIT):
            merc.act("$n has arrived.", ch, portal, None, merc.TO_ROOM)
        else:
            merc.act("$n has arrived through $p.", ch, portal, None, merc.TO_ROOM)

        ch.do_look("auto")
        # charges
        if portal.value[0] > 0:
            portal.value[0] -= 1
            if portal.value[0] == 0:
                portal.value[0] = -1
        # protect against circular follows
        if old_room == location:
            return
        for fch in old_room.people[:]:
            if not portal or portal.value[0] == -1:
                # no following through dead portals
                continue
            if fch.master == ch and merc.IS_AFFECTED(fch, merc.AFF_CHARM) \
                    and fch.position < merc.POS_STANDING:
                fch.do_stand("")
            if fch.master == ch and fch.position == merc.POS_STANDING:
                if merc.IS_SET(ch.in_room.room_flags, merc.ROOM_LAW) \
                        and (merc.IS_NPC(fch) and merc.IS_SET(fch.act, merc.ACT_AGGRESSIVE)):
                    merc.act("You can't bring $N into the city.", ch, None, fch, merc.TO_CHAR)
                    merc.act("You aren't allowed in the city.", fch, None, None, merc.TO_CHAR)
                    continue
                merc.act("You follow $N.", fch, None, ch, merc.TO_CHAR)
                fch.do_enter(argument)
        if portal and portal.value[0] == -1:
            merc.act("$p fades out of existence.", ch, portal, None, merc.TO_CHAR)
            if ch.in_room == old_room:
                merc.act("$p fades out of existence.", ch, portal, None, merc.TO_ROOM)
            elif old_room.people:
                merc.act("$p fades out of existence.", old_room.people, portal, None, merc.TO_CHAR)
                merc.act("$p fades out of existence.", old_room.people, portal, None, merc.TO_ROOM)
            portal.extract()
        return
    ch.send("Nope, can't do it.\n")
    return


interp.register_command(interp.cmd_type('enter', do_enter, merc.POS_STANDING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('go', do_enter, merc.POS_STANDING, 0, merc.LOG_NORMAL, 0))
