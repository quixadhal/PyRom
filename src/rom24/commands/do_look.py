import logging

logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import game_utils
from rom24 import handler_ch
from rom24 import handler_game
from rom24 import state_checks
from rom24 import interp
from rom24 import const
from rom24 import instance


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
    room = ch.in_room
    if (
        not ch.is_npc()
        and not ch.act.is_set(merc.PLR_HOLYLIGHT)
        and ch.in_room.is_dark()
    ):
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
        if ch.is_immortal() and (
            ch.is_npc()
            or (ch.act.is_set(merc.PLR_HOLYLIGHT) or ch.act.is_set(merc.PLR_OMNI))
        ):
            ch.send(
                " Room[[{room.instance_id}]] Template[[{room.vnum}]]".format(room=room)
            )
        ch.send("\n")
        if not arg1 or (not ch.is_npc() and not ch.comm.is_set(merc.COMM_BRIEF)):
            ch.send("  %s\n" % room.description)
        if not ch.is_npc() and ch.act.is_set(merc.PLR_AUTOEXIT):
            ch.send("\n")
            ch.do_exits("auto")
        handler_ch.show_list_to_char(room.items, ch, False, False)
        handler_ch.show_char_to_char(room.people, ch)
        return
    if arg1 == "i" or arg1 == "in" or arg1 == "on":
        # 'look in'
        if not arg2:
            ch.send("Look in what?\n")
            return
        item = ch.get_item_here(arg2)
        if not item:
            ch.send("You do not see that here.\n")
            return
        item_type = item.item_type
        if item_type == merc.ITEM_DRINK_CON:
            if item.value[1] <= 0:
                ch.send("It is empty.\n")
                return
            if item.value[1] < item.value[0] // 4:
                amnt = "less than half-"
            elif item.value[1] < 3 * item.value[0] // 4:
                amnt = "abount half-"
            else:
                amnt = "more than half-"
            ch.send(
                "It's %sfilled with a %s liquid.\n"
                % (amnt, const.liq_table[item.value[2]].color)
            )
        elif (
            item_type == merc.ITEM_CONTAINER
            or item_type == merc.ITEM_CORPSE_NPC
            or item_type == merc.ITEM_CORPSE_PC
        ):
            if state_checks.IS_SET(item.value[1], merc.CONT_CLOSED):
                ch.send("It is closed.\n")
                return
            handler_game.act("$p holds:", ch, item, None, merc.TO_CHAR)
            handler_ch.show_list_to_char(item.inventory, ch, True, True)
            return
        else:
            ch.send("That is not a container.\n")
            return
    victim = ch.get_char_room(arg1)
    if victim:
        handler_ch.show_char_to_char_1(victim, ch)
        return
    item_list = list(ch.items) + list(room.items)
    for obj_id in item_list:
        item = instance.items[obj_id]
        if ch.can_see_item(item):
            # player can see object
            pdesc = game_utils.get_extra_descr(arg3, item.extra_descr)
            if pdesc:
                count += 1
                if count == number:
                    ch.send(pdesc)
                    return
                else:
                    continue
            if game_utils.is_name(arg3, item.name.lower()):
                count += 1
                if count == number:
                    ch.send("%s\n" % item.description)
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
    if door not in room.exit or not room.exit[door]:
        ch.send("Nothing special there.\n")
        return
    pexit = room.exit[door]

    if pexit.description:
        ch.send(pexit.description)
    else:
        ch.send("Nothing special there.\n")
    if pexit.keyword and pexit.keyword.strip():
        if pexit.exit_info.is_set(merc.EX_CLOSED):
            handler_game.act("The $d is closed.", ch, None, pexit.keyword, merc.TO_CHAR)
        elif pexit.exit_info.is_set(merc.EX_ISDOOR):
            handler_game.act("The $d is open.", ch, None, pexit.keyword, merc.TO_CHAR)
    return


interp.register_command(
    interp.cmd_type("look", do_look, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
interp.register_command(
    interp.cmd_type("read", do_look, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
