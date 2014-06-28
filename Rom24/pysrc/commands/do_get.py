import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import handler_obj
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
            obj = ch.get_obj_list(arg1, ch.in_room.contents)
            if not obj:
                handler_game.act("I see no $T here.", ch, None, arg1, merc.TO_CHAR)
                return
            handler_obj.get_obj(ch, obj, None)
        else:
            # 'get all' or 'get all.obj'
            for obj in ch.in_room.contents[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and ch.can_see_obj(obj):
                    found = True
                    handler_obj.get_obj(ch, obj, None)
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
        container = ch.get_obj_here(arg2)
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
            obj = ch.get_obj_list(arg1, container.contains)
            if not obj is None:
                handler_game.act("I see nothing like that in the $T.", ch, None, arg2, merc.TO_CHAR)
                return
            handler_obj.get_obj(ch, obj, container)
        else:
            # 'get all container' or 'get all.obj container'
            found = False
            for obj in container.contains[:]:
                if (len(arg1) == 3 or arg1[4:] in obj.name) and ch.can_see_obj(obj):
                    found = True
                    if container.pIndexData.vnum == merc.OBJ_VNUM_PIT and not state_checks.IS_IMMORTAL(ch):
                        ch.send("Don't be so greedy!\n")
                        return
                    handler_obj.get_obj(ch, obj, container)
            if not found:
                if len(arg1) == 3:
                    handler_game.act("I see nothing in the $T.", ch, None, arg2, merc.TO_CHAR)
                else:
                    handler_game.act("I see nothing like that in the $T.", ch, None, arg2, merc.TO_CHAR)


interp.register_command(interp.cmd_type('get', do_get, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('take', do_get, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
