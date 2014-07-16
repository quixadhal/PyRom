import logging


logger = logging.getLogger()

import merc
import interp
import game_utils
import handler_game
import state_checks

def do_sacrifice(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg or arg == ch.name.lower():
        act("$n offers $mself to Mota, who graciously declines.", ch, None, None, merc.TO_ROOM)
        ch.send("Mota appreciates your offer and may accept it later.\n")
        return
    obj = ch.get_item_list(arg, ch.in_room.items)
    if obj is None:
        ch.send("You can't find it.\n")
        return
    if obj.item_type == merc.ITEM_CORPSE_PC:
        if obj.contents:
            ch.send("Mota wouldn't like that.\n")
            return
    if not state_checks.CAN_WEAR(obj, merc.ITEM_TAKE) or state_checks.CAN_WEAR(obj, merc.ITEM_NO_SAC):
        act("$p is not an acceptable sacrifice.", ch, obj, 0, merc.TO_CHAR)
        return
    if obj.in_room:
        for gch in obj.in_room.people:
            if gch.on == obj:
                act("$N appears to be using $p.", ch, obj, gch, merc.TO_CHAR)
                return

    silver = max(1, obj.level * 3)
    if obj.item_type != merc.ITEM_CORPSE_NPC and obj.item_type != merc.ITEM_CORPSE_PC:
        silver = min(silver, obj.cost)

    if silver == 1:
        ch.send("Mota gives you one silver coin for your sacrifice.\n")
    else:
        ch.send("Mota gives you %d silver coins for your sacrifice.\n" % silver)
    ch.silver += silver
    if ch.act.is_set(merc.PLR_AUTOSPLIT):
        # AUTOSPLIT code
        members = len([gch for gch in ch.in_room.people if gch.is_same_group(ch)])
        if members > 1 and silver > 1:
            ch.do_split("%d" % silver)
    act("$n sacrifices $p to Mota.", ch, obj, None, merc.TO_ROOM)
    handler_game.wiznet("$N sends up $p as a burnt offering.", ch, obj, merc.WIZ_SACCING, 0, 0)
    obj.extract()
    return


interp.register_command(interp.cmd_type('sacrifice', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
interp.register_command(interp.cmd_type('junk', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0))
interp.register_command(interp.cmd_type('tap', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0))
