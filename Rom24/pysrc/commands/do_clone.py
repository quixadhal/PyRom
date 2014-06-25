import merc
import interp


# command that is similar to load */
def do_clone(ch, argument):
    rest, arg = merc.read_word(argument)
    mob = None
    obj = None
    if not arg:
        ch.send("Clone what?\n")
        return
    if "object".startswith(arg):
        mob = None
        obj = ch.get_obj_here(rest)
        if not obj:
            ch.send("You don't see that here.\n")
            return
    elif "character".startswith(arg) or "mobile".startswith(arg):
        obj = None
        mob = ch.get_char_room(rest)
        if not mob:
            ch.send("You don't see that here.\n")
            return
    else: # find both */
        mob = ch.get_char_room(argument)
        obj = ch.get_obj_here(argument)
        if mob == None and obj == None:
            ch.send("You don't see that here.\n")
            return
      # clone an object */
    if obj:
        if not merc.obj_check(ch,obj):
            ch.send("Your powers are not great enough for such a task.\n")
            return
        clone = db.create_object(obj.pIndexData,0)
        db.clone_object(obj,clone)
        if obj.carried_by:
            clone.to_char(ch)
        else:
            clone.to_room(ch.in_room)
        merc.recursive_clone(ch,obj,clone)

        merc.act("$n has created $p.",ch, clone, None, merc.TO_ROOM)
        merc.act("You clone $p.", ch, clone, None, merc.TO_CHAR)
        merc.wiznet("$N clones $p.", ch, clone, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.get_trust())
        return
    elif mob:
        if not merc.IS_NPC(mob):
            ch.send("You can only clone mobiles.\n")
            return
        if (mob.level > 20 and not merc.IS_TRUSTED(ch, merc.GOD)) \
        or (mob.level > 10 and not merc.IS_TRUSTED(ch, merc.IMMORTAL)) \
        or (mob.level >  5 and not merc.IS_TRUSTED(ch, merc.DEMI)) \
        or (mob.level >  0 and not merc.IS_TRUSTED(ch, merc.ANGEL)) \
        or not merc.IS_TRUSTED(ch, merc.AVATAR):
            ch.send(    "Your powers are not great enough for such a task.\n")
            return
        clone = merc.create_mobile(mob.pIndexData)
        db.clone_mobile(mob,clone)

        for obj in mob.carrying:
            if merc.obj_check(ch,obj):
                new_obj = db.create_object(obj.pIndexData,0)
                db.clone_object(obj,new_obj)
                merc.recursive_clone(ch,obj,new_obj)
                new_obj.to_char(clone)
                new_obj.wear_loc = obj.wear_loc
        clone.to_room(ch.in_room)
        merc.act("$n has created $N.",ch,None,clone,TO_ROOM)
        merc.act("You clone $N.", ch, None, clone, merc.TO_CHAR)
        merc.wiznet("$N clones %s." % clone.short_descr,ch,None, merc.WIZ_LOAD, merc.WIZ_SECURE, ch.get_trust())
        return

interp.cmd_table['clone'] = interp.cmd_type('clone', do_clone, merc.POS_DEAD, merc.L5, merc.LOG_ALWAYS, 1)