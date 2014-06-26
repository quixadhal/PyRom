import merc
import interp
import skills


def do_recite(ch, argument):
    argument, arg1 = merc.read_word(argument)
    argument, arg2 = merc.read_word(argument)
    scroll = ch.get_obj_carry(arg1, ch)
    if not scroll:
        ch.send("You do not have that scroll.\n")
        return
    if scroll.item_type != merc.ITEM_SCROLL:
        ch.send("You can recite only scrolls.\n")
        return
    if ch.level < scroll.level:
        ch.send("This scroll is too complex for you to comprehend.\n")
        return
    obj = None
    victim = None
    if not arg2:
        victim = ch
    else:
        victim = ch.get_char_room(arg2)
        obj = ch.get_obj_here(arg2)
        if not victim and not obj:
            ch.send("You can't find it.\n")
            return
        merc.act( "$n recites $p.", ch, scroll, None, merc.TO_ROOM)
        merc.act( "You recite $p.", ch, scroll, None, merc.TO_CHAR)

    if random.randint(1,99) >= 20 + ch.get_skill("scrolls") * 4 // 5:
        ch.send("You mispronounce a syllable.\n")
        skills.check_improve(ch,"scrolls", False, 2)
    else:
        merc.obj_cast_spell(scroll.value[1], scroll.value[0], ch, victim, obj)
        merc.obj_cast_spell(scroll.value[2], scroll.value[0], ch, victim, obj)
        merc.obj_cast_spell(scroll.value[3], scroll.value[0], ch, victim, obj)
        skills.check_improve(ch,"scrolls",True,2)
    scroll.extract()
    return

interp.cmd_table['recite'] = interp.cmd_type('recite', do_recite, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)