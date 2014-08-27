import logging

logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import handler_item
import object_creator
import state_checks


# command that is similar to load
def do_clone(ch, argument):
    rest, arg = game_utils.read_word(argument)
    mob = None
    obj = None
    if not arg:
        ch.send("Clone what?\n")
        return
    if "object".startswith(arg):
        mob = None
        obj = ch.get_item_here(rest)
        if not obj:
            ch.send("You don't see that here.\n")
            return
    elif "character".startswith(arg) or "mobile".startswith(arg):
        obj = None
        mob = ch.get_char_room(rest)
        if not mob:
            ch.send("You don't see that here.\n")
            return
    else:  # find both
        mob = ch.get_char_room(argument)
        obj = ch.get_item_here(argument)
        if mob is None and obj is None:
            ch.send("You don't see that here.\n")
            return
            # clone an object
    if obj:
        if not handler_item.item_check(ch, obj):
            ch.send("Your powers are not great enough for such a task.\n")
            return
        clone = object_creator.create_item(obj.vnum, 0)
        object_creator.clone_item(obj, clone)
        if obj.in_living:
            clone.put(ch)
        else:
            clone.put(ch.in_room)
        handler_item.recursive_clone(ch, obj, clone)

        handler_game.act("$n has created $p.", ch, clone, None, merc.TO_ROOM)
        handler_game.act("You clone $p.", ch, clone, None, merc.TO_CHAR)
        handler_game.wiznet("$N clones $p.", ch, clone, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.trust)
        return
    elif mob:
        if not state_checks.IS_NPC(mob):
            ch.send("You can only clone mobiles.\n")
            return
        if (mob.level > 20 and not state_checks.IS_TRUSTED(ch, merc.L4)) \
                or (mob.level > 10 and not state_checks.IS_TRUSTED(ch, merc.L5)) \
                or (mob.level > 5 and not state_checks.IS_TRUSTED(ch, merc.L6)) \
                or (mob.level > 0 and not state_checks.IS_TRUSTED(ch, merc.L7)) \
                or not state_checks.IS_TRUSTED(ch, merc.L8):
            ch.send("Your powers are not great enough for such a task.\n")
            return
        clone = object_creator.create_mobile(mob.vnum)
        object_creator.clone_mobile(mob, clone)

        for obj in mob.contents:
            if handler_item.item_check(ch, obj):
                new_obj = object_creator.create_item(obj.vnum, 0)
                object_creator.clone_item(obj, new_obj)
                handler_item.recursive_clone(ch, obj, new_obj)
                new_obj.put(clone)
                new_obj.equips_to = obj.equips_to
        clone.put(ch.in_room)
        handler_game.act("$n has created $N.", ch, None, clone, merc.TO_ROOM)
        handler_game.act("You clone $N.", ch, None, clone, merc.TO_CHAR)
        handler_game.wiznet("$N clones %s." % clone.short_descr, ch, None, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.trust)
        return


interp.register_command(interp.cmd_type('clone', do_clone, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1))
