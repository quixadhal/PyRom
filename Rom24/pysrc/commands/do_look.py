import logging
import game_utils
import handler_ch
import handler_game
import state_checks

logger = logging.getLogger()

from const import liq_table
import merc
import interp


def do_look(ch, argument):
    if ch.is_npc() or not ch.desc:
        return
    if ch.position < merc.POS_SLEEPING:
        ch.send("You can't see anything but stars!\n")
        return
    if ch.position == merc.POS_SLEEPING:
        ch.send("You can't see anything, you're sleeping!\n")
        return
    if not ch.check_blind():
        return
    room = merc.rooms[ch.in_room]
    if not ch.is_npc() and not ch.act.is_set(merc.PLR_HOLYLIGHT) \
            and ch.room_template.is_dark():
        ch.send("It is pitch black ... \n")
        handler_ch.show_char_to_char(room.people, ch)
        return
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    number, arg3 = game_utils.number_argument(arg1)
    count = 0
    if not arg1 or arg1 == "auto":
        # 'look' or 'look auto'
        ch.send(room.name)
        if ch.is_immortal() \
                and (ch.is_npc()
                     or (ch.act.is_set(merc.PLR_HOLYLIGHT)
                         or ch.act.is_set(merc.PLR_OMNI))):
            ch.send(" [Room %d]" % room.instance_id)
        ch.send("\n")
        if not arg1 or (not ch.is_npc()
                        and not ch.comm.is_set(merc.COMM_BRIEF)):
            ch.send("  %s" % room.description)
        if not ch.is_npc() \
                and ch.act.is_set(merc.PLR_AUTOEXIT):
            ch.send("\n")
            ch.do_exits("auto")
        handler_ch.show_list_to_char(room.contents, ch, False, False)
        handler_ch.show_char_to_char(room.people, ch)
        return
    if arg1 == "i" or arg1 == "in" or arg1 == "on":
        # 'look in'
        if not arg2:
            ch.send("Look in what?\n")
            return
        obj = ch.get_item_here(arg2)
        if not obj:
            ch.send("You do not see that here.\n")
            return
        item_type = obj.item_type
        if item_type == merc.ITEM_DRINK_CON:
            if obj.value[1] <= 0:
                ch.send("It is empty.\n")
                return
            if obj.value[1] < obj.value[0] // 4:
                amnt = "less than half-"
            elif obj.value[1] < 3 * obj.value[0] // 4:
                amnt = "abount half-"
            else:
                amnt = "more than half-"
            ch.send("It's %sfilled with a %s liquid.\n" % (
                amnt, liq_table[obj.value[2]].liq_color))
        elif item_type == merc.ITEM_CONTAINER or item_type == merc.ITEM_CORPSE_NPC \
                or item_type == merc.ITEM_CORPSE_PC:
            if state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
                ch.send("It is closed.\n")
                return
            handler_game.act("$p holds:", ch, obj, None, merc.TO_CHAR)
            handler_ch.show_list_to_char(obj.contains, ch, True, True)
            return
        else:
            ch.send("That is not a container.\n")
            return
    victim = ch.get_char_room(arg1)
    if victim:
        handler_ch.show_char_to_char_1(victim, ch)
        return
    obj_list = ch.contents
    obj_list.extend(room.contents)
    for obj in obj_list:
        if ch.can_see_item(obj):
            # player can see object
            pdesc = game_utils.get_extra_descr(arg3, obj.extra_descr)
            if pdesc:
                count += 1
                if count == number:
                    ch.send(pdesc)
                    return
            else:
                continue
            pdesc = game_utils.get_extra_descr(arg3, obj.extra_descr)
            if pdesc:
                count += 1
                if count == number:
                    ch.send(pdesc)
                    return
            else:
                continue
            if arg3.lower() in obj.name.lower:
                count += 1
                if count == number:
                    ch.send("%s\n" % obj.description)
                    return
    pdesc = game_utils.get_extra_descr(arg3, room.extra_descr)
    if pdesc:
        count += 1
        if count == number:
            ch.send(pdesc)
            return
    if count > 0 and count != number:
        if count == 1:
            ch.send("You only see one %s here.\n" % arg3)
        else:
            ch.send("You only see %d of those here.\n" % count)
        return
    if "north".startswith(arg1):
        door = 0
    elif "east".startswith(arg1):
        door = 1
    elif "south".startswith(arg1):
        door = 2
    elif "west".startswith(arg1):
        door = 3
    elif "up".startswith(arg1):
        door = 4
    elif "down".startswith(arg1):
        door = 5
    else:
        ch.send("You do not see that here.\n")
        return
    # 'look direction'
    if door not in room.exit \
            or not room.exit[door]:
        ch.send("Nothing special there.\n")
        return
    pexit = room.exit[door]

    if pexit.description:
        ch.send(pexit.description)
    else:
        ch.send("Nothing special there.\n")
    if pexit.keyword and pexit.keyword.strip():
        if state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED):
            handler_game.act("The $d is closed.", ch, None, pexit.keyword, merc.TO_CHAR)
        elif state_checks.IS_SET(pexit.exit_info, merc.EX_ISDOOR):
            handler_game.act("The $d is open.", ch, None, pexit.keyword, merc.TO_CHAR)
    return


interp.register_command(interp.cmd_type('look', do_look, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('read', do_look, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
