import logging


logger = logging.getLogger(__name__)

from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import handler_game
from rom24 import instance


def do_sacrifice(ch, argument):
    argument, arg = game_utils.read_word(argument)

    if not arg or arg == ch.name.lower():
        handler_game.act(
            "$n offers $mself to Mota, who graciously declines.",
            ch,
            None,
            None,
            merc.TO_ROOM,
        )
        ch.send("Mota appreciates your offer and may accept it later.\n")
        return
    item = ch.get_item_list(arg, ch.in_room.items)
    if item is None:
        ch.send("You can't find it.\n")
        return
    if item.item_type == merc.ITEM_CORPSE_PC:
        if item.inventory:
            ch.send("Mota wouldn't like that.\n")
            return
    if not item.flags.take or item.flags.no_sac:
        handler_game.act(
            "$p is not an acceptable sacrifice.", ch, item, 0, merc.TO_CHAR
        )
        return
    if item.in_room:
        for gch_id in item.in_room.people:
            gch = instance.characters[gch_id]
            if gch.on == item.instance_id:
                handler_game.act(
                    "$N appears to be using $p.", ch, item, gch, merc.TO_CHAR
                )
                return

    silver = max(1, item.level * 3)
    if item.item_type != merc.ITEM_CORPSE_NPC and item.item_type != merc.ITEM_CORPSE_PC:
        silver = min(silver, item.cost)

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
    handler_game.act("$n sacrifices $p to Mota.", ch, item, None, merc.TO_ROOM)
    handler_game.wiznet(
        "$N sends up $p as a burnt offering.", ch, item, merc.WIZ_SACCING, 0, 0
    )
    ch.in_room.get(item)
    item.extract()
    return


interp.register_command(
    interp.cmd_type("sacrifice", do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
interp.register_command(
    interp.cmd_type("junk", do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)
)
interp.register_command(
    interp.cmd_type("tap", do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)
)
