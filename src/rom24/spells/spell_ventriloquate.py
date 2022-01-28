from rom24 import game_utils
from rom24 import handler_magic
from rom24 import merc
from rom24 import state_checks


def spell_ventriloquate(sn, level, ch, victim, target):
    target_name, speaker = game_utils.read_word(target_name)
    buf1 = "%s says '%s'.\n" % (speaker.capitalize(), target_name)
    buf2 = "Someone makes %s say '%s'.\n" % (speaker, target_name)

    for vch_id in ch.in_room.people:
        vch = instance.characters[vch_id]
        if not is_exact_name(speaker, vch.name) and state_checks.IS_AWAKE(vch):
            vch.send(
                buf2 if handler_magic.saves_spell(level, vch, merc.DAM_OTHER) else buf1
            )
