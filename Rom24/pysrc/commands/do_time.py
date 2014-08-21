import logging

logger = logging.getLogger()

import merc
import interp
import handler_game


day_name = ["the Moon", "the Bull", "Deception", "Thunder", "Freedom",
            "the Great Gods", "the Sun"]
month_name = ["Winter", "the Winter Wolf", "the Frost Giant", "the Old Forces",
              "the Grand Struggle", "the Spring", "Nature", "Futility", "the Dragon",
              "the Sun", "the Heat", "the Battle", "the Dark Shades", "the Shadows",
              "the Long Shadows", "the Ancient Darkness", "the Great Evil"]

#TODO: Known broken. Doesn't show startup or longevity.
def do_time(ch, argument):
    day = handler_game.time_info.day + 1
    suf = ''
    if day > 4 and day < 20:
        suf = "th"
    elif day % 10 == 1:
        suf = "st"
    elif day % 10 == 2:
        suf = "nd"
    elif day % 10 == 3:
        suf = "rd"
    else:
        suf = "th"

    ch.send("It is %d o'clock %s, Day of %s, %d%s the Month of %s.\n" % (
        12 if (handler_game.time_info.hour % 12 == 0) else handler_game.time_info.hour % 12,
        "pm" if handler_game.time_info.hour >= 12 else "am",
        day_name[day % 7], day, suf, month_name[handler_game.time_info.month]))
    # ch.send("ROM started up at %s\nThe system time is %s.\n", str_boot_time, (char *) ctime(&current_time)
    return


interp.register_command(interp.cmd_type('time', do_time, merc.POS_DEAD, 0, merc.LOG_NORMAL, 1))
