import merc
import comm
import interp
import save


def do_purge(ch, argument):
    argument, arg = merc.read_word(argument)
    if not arg:
        for victim in ch.in_room.people[:]:
            if IS_NPC(victim) and not merc.IS_SET(victim.act, merc.ACT_NOPURGE) and victim != ch: # safety precaution */ )
                victim.extract(True)
        for obj in ch.in_room.contents[:]:
            if not merc.IS_OBJ_STAT(obj, merc.ITEM_NOPURGE):
                obj.extract()
        merc.act( "$n purges the room!", ch, None, None, merc.TO_ROOM)
        ch.send("Ok.\n")
        return
    victim = ch.get_char_world(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if not merc.IS_NPC(victim):
        if ch == victim:
            ch.send("Ho ho ho.\n")
            return
        if ch.get_trust() <= victim.get_trust():
            ch.send("Maybe that wasn't a good idea...\n")
            victim.send("%s tried to purge you!\n" % ch.name)
            return
        merc.act("$n disintegrates $N.", ch, 0, victim, merc.TO_NOTVICT)

        if victim.level > 1:
            save.save_char_obj(victim)
        d = victim.desc
        victim.extract(True)
        if d:
            comm.close_socket(d)
        return
    merc.act("$n purges $N.", ch, None, victim, merc.TO_NOTVICT)
    victim.extract(True)
    return

interp.cmd_table['purge'] = interp.cmd_type('purge', do_purge, merc.POS_DEAD, merc.L4, merc.LOG_ALWAYS, 1)