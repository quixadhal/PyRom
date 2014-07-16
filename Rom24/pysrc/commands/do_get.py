import logging
import handler_game

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_item
import state_checks


def do_get(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    if arg2 == "from":
        argument, arg2 = game_utils.read_word(argument)
    found = False
    # Get type.
    if not arg1:
        ch.send("Get what?\n")
        return
    if not arg2:
        if not arg1.startswith('all'):
            # 'get obj'
            item = ch.get_item_list(arg1, ch.in_room.items)
            if not item:
                handler_game.act("I see no $T here.", ch, None, arg1, merc.TO_CHAR)
                return
            handler_item.get_item(ch, item, None)
        else:
            # 'get all' or 'get all.obj'
            for item_id in ch.in_room.items:
                item = merc.items[item_id]
                if (len(arg1) == 3 or arg1[4:] in item.name) and ch.can_see_item(item_id):
                    found = True
                    handler_item.get_item(ch, item, None)
            if not found:
                if len(arg1) == 3:
                    ch.send("I see nothing here.\n")
                else:
                    handler_game.act("I see no $T here.", ch, None, arg1[4:], merc.TO_CHAR)
    else:
        # 'get ... container'
        if arg2.startswith("all"):
            ch.send("You can't do that.\n")
            return
        container = ch.get_item_here(arg2)
        if not container:
            handler_game.act("I see no $T here.", ch, None, arg2, merc.TO_CHAR)
            return
        if container.item_type == merc.ITEM_CONTAINER \
                or container.item_type == merc.ITEM_CORPSE_NPC:
            pass
        elif container.item_type == merc.ITEM_CORPSE_PC:
            if not ch.can_loot(container):
                ch.send("You can't do that.\n")
                return
        else:
            ch.send("That's not a container.\n")
            return
        if state_checks.IS_SET(container.value[1], merc.CONT_CLOSED):
            handler_game.act("The $d is closed.", ch, None, container.name, merc.TO_CHAR)
            return
        if not arg1.startswith('all'):
            # 'get obj container'
            item = ch.get_item_list(arg1, container.contents)
            if not item is None:
                handler_game.act("I see nothing like that in the $T.", ch, None, arg2, merc.TO_CHAR)
                return
            handler_item.get_item(ch, item, container)
        else:
            # 'get all container' or 'get all.obj container'
            found = False
            for item in container.contents[:]:
                if (len(arg1) == 3 or arg1[4:] in item.name) and ch.can_see_item(item):
                    found = True
                    if container.pIndexData.vnum == merc.OBJ_VNUM_PIT and not ch.is_immortal():
                        ch.send("Don't be so greedy!\n")
                        return
                    handler_item.get_item(ch, item, container)
            if not found:
                if len(arg1) == 3:
                    handler_game.act("I see nothing in the $T.", ch, None, arg2, merc.TO_CHAR)
                else:
                    handler_game.act("I see nothing like that in the $T.", ch, None, arg2, merc.TO_CHAR)


interp.register_command(interp.cmd_type('get', do_get, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('take', do_get, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
