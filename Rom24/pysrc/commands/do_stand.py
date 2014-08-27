import logging

logger = logging.getLogger()

import handler_game
import interp
import merc
import state_checks


def do_stand(ch, argument):
    obj = None
    if argument:
        if ch.position == merc.POS_FIGHTING:
            ch.send("Maybe you should finish fighting first?\n")
            return
        obj = ch.get_item_list(argument, ch.in_room.items)
        if not obj:
            ch.send("You don't see that here.\n")
            return
        if obj.item_type != merc.ITEM_FURNITURE \
                or (not state_checks.IS_SET(obj.value[2], merc.STAND_AT)
                    and not state_checks.IS_SET(obj.value[2], merc.STAND_ON)
                    and not state_checks.IS_SET(obj.value[2], merc.STAND_IN)):
            ch.send("You can't seem to find a place to stand.\n")
            return
        if ch.on != obj and obj.count_users() >= obj.value[0]:
            handler_game.act("There's no room to stand on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            return
        ch.on = obj

    if ch.position == merc.POS_SLEEPING:
        if ch.is_affected(merc.AFF_SLEEP):
            ch.send("You can't wake up!\n")
            return
        if not obj:
            ch.send("You wake and stand up.\n")
            handler_game.act("$n wakes and stands up.", ch, None, None, merc.TO_ROOM)
            ch.on = None
        elif state_checks.IS_SET(obj.value[2], merc.STAND_AT):
            handler_game.act("You wake and stand at $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and stands at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.STAND_ON):
            handler_game.act("You wake and stand on $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and stands on $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You wake and stand in $p.", ch, obj, None, merc.TO_CHAR, merc.POS_DEAD)
            handler_game.act("$n wakes and stands in $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_STANDING
        ch.do_look("auto")
        return
    elif ch.position == merc.POS_RESTING or ch.position == merc.POS_SITTING:
        if not obj:
            ch.send("You stand up.\n")
            handler_game.act("$n stands up.", ch, None, None, merc.TO_ROOM)
            ch.on = None
        elif state_checks.IS_SET(obj.value[2], merc.STAND_AT):
            handler_game.act("You stand at $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n stands at $p.", ch, obj, None, merc.TO_ROOM)
        elif state_checks.IS_SET(obj.value[2], merc.STAND_ON):
            handler_game.act("You stand on $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n stands on $p.", ch, obj, None, merc.TO_ROOM)
        else:
            handler_game.act("You stand in $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n stands on $p.", ch, obj, None, merc.TO_ROOM)
        ch.position = merc.POS_STANDING
        return
    elif ch.position == merc.POS_STANDING:
        ch.send("You are already standing.\n")
        return
    elif ch.position == merc.POS_FIGHTING:
        ch.send("You are already fighting!\n")
        return


interp.register_command(interp.cmd_type('stand', do_stand, merc.POS_SLEEPING, 0, merc.LOG_NORMAL, 1))
