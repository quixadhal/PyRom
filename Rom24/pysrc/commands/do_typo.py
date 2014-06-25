import merc
import interp
import settings


def do_typo(ch, argument):
    merc.append_file(ch, settings.TYPO_FILE, argument)
    ch.send("Typo logged.\n")
    return

interp.cmd_table['typo'] = interp.cmd_type('typo', do_typo, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1)