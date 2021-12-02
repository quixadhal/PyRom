import collections
import random
import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import handler_game
from rom24 import const
from rom24 import state_checks
from rom24 import handler_item
from rom24 import instance

depth = 0


def CH(d):
    return d.original if d.original else d.character


def move_char(ch, door, follow):
    if door < 0 or door > 5:
        logger.error("BUG: Do_move: bad door %d." % door)
        return
    in_room = ch.in_room
    if not ch._room_vnum:
        ch._room_vnum = in_room.vnum
    pexit = in_room.exit[door]
    if not pexit or not pexit.to_room or not ch.can_see_room(pexit.to_room):
        ch.send("Alas, you cannot go that way.\n")
        return
    to_room = instance.rooms[pexit.to_room]
    if (
        pexit.exit_info.is_set(merc.EX_CLOSED)
        and (
            not ch.is_affected(merc.AFF_PASS_DOOR)
            or pexit.exit_info.is_set(merc.EX_NOPASS)
        )
        and not state_checks.IS_TRUSTED(ch, merc.L7)
    ):
        handler_game.act("The $d is closed.", ch, None, pexit.keyword, merc.TO_CHAR)
        return
    if (
        ch.is_affected(merc.AFF_CHARM)
        and ch.master
        and in_room == instance.characters[ch.master].in_room
    ):
        ch.send("What?  And leave your beloved master?\n")
        return
    if not ch.is_room_owner(to_room) and to_room.is_private():
        ch.send("That room is private right now.\n")
        return
    if not ch.is_npc():
        for gn, guild in const.guild_table.items():
            for room_vnum in guild.guild_rooms:
                if room_vnum in instance.instances_by_room:
                    room_id = instance.instances_by_room[room_vnum][0]
                    room = instance.rooms[room_id]
                    if guild != ch.guild and to_room.instance_id == room.instance_id:
                        ch.send("You aren't allowed in there.\n")
                        return
        if in_room.sector_type == merc.SECT_AIR or to_room.sector_type == merc.SECT_AIR:
            if not ch.is_affected(merc.AFF_FLYING) and not ch.is_immortal():
                ch.send("You can't fly.\n")
                return
        if (
            in_room.sector_type == merc.SECT_WATER_NOSWIM
            or to_room.sector_type == merc.SECT_WATER_NOSWIM
        ) and not ch.is_affected(merc.AFF_FLYING):
            # Look for a boat.
            boats = [
                item_id
                for item_id in ch.inventory
                if instance.items[item_id].item_type == merc.ITEM_BOAT
            ]
            if not boats and not ch.is_immortal():
                ch.send("You need a boat to go there.\n")
                return
        move = (
            merc.movement_loss[min(merc.SECT_MAX - 1, in_room.sector_type)]
            + merc.movement_loss[min(merc.SECT_MAX - 1, to_room.sector_type)]
        )
        move /= 2  # i.e. the average */
        # conditional effects */
        if ch.is_affected(merc.AFF_FLYING) or ch.is_affected(merc.AFF_HASTE):
            move //= 2
        if ch.is_affected(merc.AFF_SLOW):
            move *= 2
        if ch.move < move:
            ch.send("You are too exhausted.\n")
            return
        state_checks.WAIT_STATE(ch, 1)
        ch.move -= move
    if not ch.is_affected(merc.AFF_SNEAK) and (
        not ch.is_npc() and ch.invis_level < merc.LEVEL_HERO
    ):
        handler_game.act("$n leaves $T.", ch, None, merc.dir_name[door], merc.TO_ROOM)
    ch.in_room.get(ch)
    to_room.put(ch)
    if not ch.is_affected(merc.AFF_SNEAK) and (
        not ch.is_npc() and ch.invis_level < merc.LEVEL_HERO
    ):
        handler_game.act("$n has arrived.", ch, None, None, merc.TO_ROOM)
    ch.do_look("auto")
    if in_room.instance_id == to_room.instance_id:  # no circular follows */
        return

    for fch_id in in_room.people[:]:
        fch = instance.characters[fch_id]
        if (
            fch.master == ch.instance_id
            and fch.is_affected(merc.AFF_CHARM)
            and fch.position < merc.POS_STANDING
        ):
            fch.do_stand("")

        if (
            fch.master == ch.instance_id
            and fch.position == merc.POS_STANDING
            and fch.can_see_room(to_room.instance_id)
        ):
            if state_checks.IS_SET(ch.in_room.room_flags, merc.ROOM_LAW) and (
                fch.is_npc() and fch.act.is_set(merc.ACT_AGGRESSIVE)
            ):
                handler_game.act(
                    "You can't bring $N into the city.", ch, None, fch, merc.TO_CHAR
                )
                handler_game.act(
                    "You aren't allowed in the city.", fch, None, None, merc.TO_CHAR
                )
                continue
            handler_game.act("You follow $N.", fch, None, ch, merc.TO_CHAR)
            move_char(fch, door, True)


def add_follower(ch, master):
    if ch.master:
        logger.error("BUG: Add_follower: non-null master.")
        return
    ch.master = master.instance_id
    ch.leader = None
    if master.can_see(ch):
        handler_game.act("$n now follows you.", ch, None, master, merc.TO_VICT)
    handler_game.act("You now follow $N.", ch, None, master, merc.TO_CHAR)
    return


# nukes charmed monsters and pets */
def nuke_pets(ch):
    if ch.pet:
        stop_follower(ch.pet)
        if instance.characters[ch.pet].in_room:
            handler_game.act(
                "$N slowly fades away.",
                ch,
                None,
                instance.characters[ch.pet],
                merc.TO_NOTVICT,
            )
        instance.characters[ch.pet].extract(True)
    ch.pet = None
    return


def die_follower(ch):
    if ch.master:
        if instance.characters[ch.master].pet == ch.instance_id:
            instance.characters[ch.master].pet = None
        stop_follower(ch)
    ch.leader = None

    for fch in instance.characters.values():
        if fch.master == ch.instance_id:
            stop_follower(fch)
        if fch.leader == ch.instance_id:
            fch.leader = fch.instance_id
    return


def stop_follower(ch):
    if not ch.master:
        logger.error("BUG: Stop_follower: null master.")
        return

    if ch.is_affected(merc.AFF_CHARM):
        ch.affected_by.rem_bit(merc.AFF_CHARM)
        ch.affect_strip("charm person")

    if instance.characters[ch.master].can_see(ch) and ch.in_room:
        handler_game.act(
            "$n stops following you.",
            ch,
            None,
            instance.characters[ch.master],
            merc.TO_VICT,
        )
        handler_game.act(
            "You stop following $N.",
            ch,
            None,
            instance.characters[ch.master],
            merc.TO_CHAR,
        )
    if instance.characters[ch.master].pet == ch.instance_id:
        instance.characters[ch.master].pet = None
    ch.master = None
    ch.leader = None
    return

    # * Show a list to a character.


# * Can coalesce duplicated items.
def show_list_to_char(clist, ch, fShort, fShowNothing):
    if not ch.desc:
        return
    item_dict = collections.OrderedDict()
    for item_id in clist:
        item = instance.items[item_id]
        if ch.can_see_item(item):
            # logger.trace("Showing an item")
            frmt = handler_item.format_item_to_char(item, ch, fShort)
            if frmt not in item_dict:
                item_dict[frmt] = 1
            else:
                item_dict[frmt] += 1

    if not item_dict and fShowNothing:
        if ch.is_npc() or ch.comm.is_set(merc.COMM_COMBINE):
            ch.send("     ")
        ch.send("Nothing.\n")

        # * Output the formatted list.
    for desc, count in item_dict.items():
        if ch.is_npc() or ch.comm.is_set(merc.COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\n" % (count, desc))
        else:
            for i in range(count):
                ch.send("     %s\n" % desc)


def show_char_to_char_0(victim, ch):
    buf = ""
    if victim.comm.is_set(merc.COMM_AFK):
        buf += "[[AFK]] "
    if victim.is_affected(merc.AFF_INVISIBLE):
        buf += "(Invis) "
    if victim.invis_level >= merc.LEVEL_HERO:
        buf += "(Wizi) "
    if victim.is_affected(merc.AFF_HIDE):
        buf += "(Hide) "
    if victim.is_affected(merc.AFF_CHARM):
        buf += "(Charmed) "
    if victim.is_affected(merc.AFF_PASS_DOOR):
        buf += "(Translucent) "
    if victim.is_affected(merc.AFF_FAERIE_FIRE):
        buf += "(Pink Aura) "
    if victim.is_evil() and ch.is_affected(merc.AFF_DETECT_EVIL):
        buf += "(Red Aura) "
    if victim.is_good() and ch.is_affected(merc.AFF_DETECT_GOOD):
        buf += "(Golden Aura) "
    if victim.is_affected(merc.AFF_SANCTUARY):
        buf += "(White Aura) "
    if not victim.is_npc() and victim.act.is_set(merc.PLR_KILLER):
        buf += "(KILLER) "
    if not victim.is_npc() and victim.act.is_set(merc.PLR_THIEF):
        buf += "(THIEF) "

    if victim.is_npc() and victim.position == victim.start_pos and victim.long_descr:
        buf += victim.long_descr
        ch.send(buf)
        if ch.act.is_set(merc.PLR_OMNI):
            ch.send("(%d)" % victim.vnum)
        return

    buf += state_checks.PERS(victim, ch)
    if (
        not victim.is_npc()
        and not ch.comm.is_set(merc.COMM_BRIEF)
        and victim.position == merc.POS_STANDING
        and not ch.on
    ):
        buf += victim.title

    if victim.position == merc.POS_DEAD:
        buf += " is DEAD!!"
    elif victim.position == merc.POS_MORTAL:
        buf += " is mortally wounded."
    elif victim.position == merc.POS_INCAP:
        buf += " is incapacitated."
    elif victim.position == merc.POS_STUNNED:
        buf += " is lying here stunned."
    elif victim.position == merc.POS_SLEEPING:
        if victim.on:
            on_item = instance.items[victim.on]
            if state_checks.IS_SET(on_item.value[2], merc.SLEEP_AT):
                buf += " is sleeping at %s." % on_item.short_descr
            elif state_checks.IS_SET(on_item.value[2], merc.SLEEP_ON):
                buf += " is sleeping on %s." % on_item.short_descr
            else:
                buf += " is sleeping in %s." % on_item.short_descr
        else:
            buf += " is sleeping here."
    elif victim.position == merc.POS_RESTING:
        if victim.on:
            on_item = instance.items[victim.on]
            if state_checks.IS_SET(on_item.value[2], merc.REST_AT):
                buf += " is resting at %s." % on_item.short_descr
            elif state_checks.IS_SET(on_item.value[2], merc.REST_ON):
                buf += " is resting on %s." % on_item.short_descr
            else:
                buf += " is resting in %s." % on_item.short_descr
        else:
            buf += " is resting here."
    elif victim.position == merc.POS_SITTING:
        if victim.on:
            on_item = instance.items[victim.on]
            if state_checks.IS_SET(on_item.value[2], merc.SIT_AT):
                buf += " is sitting at %s." % on_item.short_descr
            elif state_checks.IS_SET(on_item.value[2], merc.SIT_ON):
                buf += " is sitting on %s." % on_item.short_descr
            else:
                buf += " is sitting in %s." % on_item.short_descr
        else:
            buf += " is sitting here."
    elif victim.position == merc.POS_STANDING:
        if victim.on:
            on_item = instance.items[victim.on]
            if state_checks.IS_SET(on_item.value[2], merc.STAND_AT):
                buf += " is standing at %s." % on_item.short_descr
            elif state_checks.IS_SET(on_item.value[2], merc.STAND_ON):
                buf += " is standing on %s." % on_item.short_descr
            else:
                buf += " is standing in %s." % on_item.short_descr
        else:
            buf += " is here."
    elif victim.position == merc.POS_FIGHTING:
        buf += " is here, fighting "
        if not victim.fighting:
            buf += "thin air??"
        elif victim.fighting == ch:
            buf += "YOU!"
        elif victim.in_room == victim.fighting.in_room:
            buf += "%s." % state_checks.PERS(victim.fighting, ch)
        else:
            buf += "someone who left??"
    buf = buf.capitalize()
    if victim.is_npc() and ch.act.is_set(merc.PLR_OMNI):
        buf += "(%s)" % victim.vnum
    ch.send(buf)
    return


def show_char_to_char_1(victim, ch):
    if victim.can_see(ch):
        if ch == victim:
            handler_game.act("$n looks at $mself.", ch, None, None, merc.TO_ROOM)
        else:
            handler_game.act("$n looks at you.", ch, None, victim, merc.TO_VICT)
            handler_game.act("$n looks at $N.", ch, None, victim, merc.TO_NOTVICT)
    if victim.description:
        ch.send(victim.description + "\n")
    else:
        handler_game.act(
            "You see nothing special about $M.", ch, None, victim, merc.TO_CHAR
        )
    if victim.max_hit > 0:
        percent = (100 * victim.hit) // victim.max_hit
    else:
        percent = -1
    buf = state_checks.PERS(victim, ch)
    if percent >= 100:
        buf += " is in excellent condition.\n"
    elif percent >= 90:
        buf += " has a few scratches.\n"
    elif percent >= 75:
        buf += " has some small wounds and bruises.\n"
    elif percent >= 50:
        buf += " has quite a few wounds.\n"
    elif percent >= 30:
        buf += " has some big nasty wounds and scratches.\n"
    elif percent >= 15:
        buf += " looks pretty hurt.\n"
    elif percent >= 0:
        buf += " is in awful condition.\n"
    else:
        buf += " is bleeding to death.\n"
    buf = buf.capitalize()
    ch.send(buf)
    handler_game.act("$N is using:", ch, None, victim, merc.TO_CHAR)
    for location, instance_id in victim.equipped.items():
        if not instance_id:
            continue
        item = instance.items[instance_id]
        if item:
            if ch.can_see_item(item):
                if (
                    item.flags.two_handed
                    and victim.equipped["off_hand"] == item.instance_id
                    and "off_hand" in location
                ):
                    continue
                else:
                    if ch.can_see_item(item):
                        ch.send(merc.eq_slot_strings[location])
                        ch.send(handler_item.format_item_to_char(item, ch, True) + "\n")
    if (
        victim != ch
        and not ch.is_npc()
        and random.randint(1, 99) < ch.get_skill("peek")
    ):
        ch.send("\nYou peek at the inventory:\n")
        if ch.is_pc:
            ch.check_improve("peek", True, 4)
        show_list_to_char(victim.inventory, ch, True, True)
    return


def show_char_to_char(plist, ch):
    for rch in plist:
        character = instance.characters[rch]
        if character == ch:
            continue
        if ch.trust < character.invis_level:
            continue
        if ch.can_see(character):
            show_char_to_char_0(character, ch)
            ch.send("\n")
        elif ch.in_room.is_dark() and character.is_affected(merc.AFF_INFRARED):
            ch.send("You see glowing red eyes watching YOU!\n")
