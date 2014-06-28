from merc import read_word, IS_AWAKE, saves_spell, DAM_OTHER


def spell_ventriloquate(sn, level, ch, victim, target):
    target_name, speaker = read_word(target_name)
    buf1 = "%s says '%s'.\n" % ( speaker.capitalize(), target_name )
    buf2 = "Someone makes %s say '%s'.\n" % ( speaker, target_name )

    for vch in ch.in_room.people:
        if not is_exact_name(speaker, vch.name) and IS_AWAKE(vch):
            vch.send(buf2 if saves_spell(level, vch, DAM_OTHER) else buf1)