import merc
import interp


def do_owhere(ch, argument):
    found = False
    number = 0
    max_found = 200

    if not argument:
        ch.send("Find what?\n")
        return
    for obj in merc.object_list:
        if not ch.can_see_obj(obj) or not merc.is_name(argument, obj.name) or ch.level < obj.level:
            continue
        found = True
        number += 1
        in_obj = obj.in_obj
        while in_obj.in_obj:
            in_obj = in_obj.in_obj

        if in_obj.carried_by and ch.can_see(in_obj.carried_by) and in_obj.carried_by.in_room:
            ch.send("%3d) %s is carried by %s [Room %d]\n" % (
                        number, obj.short_descr, merc.PERS(in_obj.carried_by, ch), in_obj.carried_by.in_room.vnum ) )
        elif in_obj.in_room and ch.can_see_room(in_obj.in_room):
            ch.send("%3d) %s is in %s [Room %d]\n" % (
                        number, obj.short_descr,in_obj.in_room.name, in_obj.in_room.vnum) )
        else:
            ch.send("%3d) %s is somewhere\n" % (number, obj.short_descr))

        if number >= max_found:
            break
    if not found:
        ch.send("Nothing like that in heaven or earth.\n")

interp.cmd_table['owhere'] = interp.cmd_type('owhere', do_owhere, merc.POS_DEAD, merc.IM, merc.LOG_NORMAL, 1)