import logging

logger = logging.getLogger(__name__)

from rom24 import object_creator
from rom24 import handler_game
from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import instance


def do_drop(ch, argument):
    found = False
    argument, arg = game_utils.read_word(argument)

    if not arg:
        ch.send("Drop what?\n")
        return
    if arg.isdigit():
        # 'drop NNNN coins'
        gold = 0
        silver = 0
        amount = int(arg)
        argument, arg = game_utils.read_word(argument)
        if amount <= 0 or (
            arg != "coins" and arg != "coin" and arg != "gold" and arg != "silver"
        ):
            ch.send("Sorry, you can't do that.\n")
            return
        if arg == "coins" or arg == "coin" or arg == "silver":
            if ch.silver < amount:
                ch.send("You don't have that much silver.\n")
                return
            ch.silver -= amount
            silver = amount
        else:
            if ch.gold < amount:
                ch.send("You don't have that much gold.\n")
                return
            ch.gold -= amount
            gold = amount
        for item_id in ch.in_room.items:
            item = instance.items[item_id]
            if item.vnum == merc.OBJ_VNUM_SILVER_ONE:
                silver += 1
                item.extract()
            elif item.vnum == merc.OBJ_VNUM_GOLD_ONE:
                gold += 1
                item.extract()
            elif item.vnum == merc.OBJ_VNUM_SILVER_SOME:
                silver += item.value[0]
                item.extract()
            elif item.vnum == merc.OBJ_VNUM_GOLD_SOME:
                gold += item.value[1]
                item.extract()
            elif item.vnum == merc.OBJ_VNUM_COINS:
                silver += item.value[0]
                gold += item.value[1]
                item.extract()
        object_creator.create_money(gold, silver).to_room(ch.in_room)
        handler_game.act("$n drops some coins.", ch, None, None, merc.TO_ROOM)
        ch.send("OK.\n")
        return
    if not arg.startswith("all"):
        # 'drop obj'
        item = ch.get_item_carry(arg, ch)
        if not item:
            ch.send("You do not have that item.\n")
            return
        if not ch.can_drop_item(item):
            ch.send("You can't let go of it.\n")
            return
        ch.get(item)
        ch.in_room.put(item)
        handler_game.act("$n drops $p.", ch, item, None, merc.TO_ROOM)
        handler_game.act("You drop $p.", ch, item, None, merc.TO_CHAR)
        if item.flags.melt_drop:
            handler_game.act("$p dissolves into smoke.", ch, item, None, merc.TO_ROOM)
            handler_game.act("$p dissolves into smoke.", ch, item, None, merc.TO_CHAR)
            item.extract()
    else:
        # 'drop all' or 'drop all.obj'
        found = False
        for item_id in ch.inventory[:]:
            item = instance.items[item_id]
            if (
                (len(arg) == 3 or arg[4:] in item.name)
                and ch.can_see_item(item)
                and not item.equipped_to
                and ch.can_drop_item(item)
            ):
                found = True
                ch.get(item)
                ch.in_room.put(item)
                handler_game.act("$n drops $p.", ch, item, None, merc.TO_ROOM)
                handler_game.act("You drop $p.", ch, item, None, merc.TO_CHAR)
                if item.flags.melt_drop:
                    handler_game.act(
                        "$p dissolves into smoke.", ch, item, None, merc.TO_ROOM
                    )
                    handler_game.act(
                        "$p dissolves into smoke.", ch, item, None, merc.TO_CHAR
                    )
                    item.extract()
        if not found:
            if arg == "all":
                handler_game.act(
                    "You are not carrying anything.", ch, None, arg, merc.TO_CHAR
                )
            else:
                handler_game.act(
                    "You are not carrying any $T.", ch, None, arg[4:], merc.TO_CHAR
                )


interp.register_command(
    interp.cmd_type("drop", do_drop, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
