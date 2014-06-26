import merc
import interp


def do_sacrifice(ch, argument):
    argument, arg = merc.read_word(argument)

    if not arg or arg == ch.name.lower():
        merc.act("$n offers $mself to Mota, who graciously declines.",ch, None, None, merc.TO_ROOM)
        ch.send("Mota appreciates your offer and may accept it later.\n")
        return
    obj = ch.get_obj_list(arg, ch.in_room.contents)
    if obj == None:
        ch.send("You can't find it.\n")
        return
    if obj.item_type == merc.ITEM_CORPSE_PC:
        if obj.contains:
            ch.send( "Mota wouldn't like that.\n")
            return
    if not merc.CAN_WEAR(obj, merc.ITEM_TAKE) or merc.CAN_WEAR(obj, merc.ITEM_NO_SAC):
        merc.act( "$p is not an acceptable sacrifice.", ch, obj, 0, merc.TO_CHAR)
        return
    if obj.in_room:
        for gch in obj.in_room.people:
            if gch.on == obj:
                merc.act("$N appears to be using $p.", ch, obj, gch, merc.TO_CHAR)
                return

    silver = max(1,obj.level * 3)
    if obj.item_type != merc.ITEM_CORPSE_NPC and obj.item_type != merc.ITEM_CORPSE_PC:
        silver = min(silver,obj.cost)

    if silver == 1:
        ch.send("Mota gives you one silver coin for your sacrifice.\n")
    else:
        ch.send("Mota gives you %d silver coins for your sacrifice.\n" % silver)
    ch.silver += silver
    if merc.IS_SET(ch.act, merc.PLR_AUTOSPLIT):
        # AUTOSPLIT code */
        members = len([gch for gch in ch.in_room.people if gch.is_same_group(ch)])
        if members > 1 and silver > 1:
            ch.do_split("%d"%silver)
    merc.act("$n sacrifices $p to Mota.", ch, obj, None, merc.TO_ROOM)
    merc.wiznet("$N sends up $p as a burnt offering.", ch, obj, merc.WIZ_SACCING, 0, 0)
    obj.extract()
    return

interp.cmd_table['sacrifice'] = interp.cmd_type('sacrifice', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
interp.cmd_table['junk'] = interp.cmd_type('junk', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)
interp.cmd_table['tap'] = interp.cmd_type('tap', do_sacrifice, merc.POS_RESTING, 0, merc.LOG_NORMAL, 0)