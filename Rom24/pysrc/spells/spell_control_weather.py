from const import SLOT, skill_type
from merc import weather_info, dice, POS_STANDING, TAR_IGNORE


def spell_control_weather(sn, level, ch, victim, target):
    if victim.lower() == "better":
        weather_info.change += dice(level // 3, 4)
    elif victim.lower() == "worse":
        weather_info.change -= dice(level // 3, 4)
    else:
        ch.send("Do you want it to get better or worse?\n")

    ch.send("Ok.\n")
    return


skill_type("control weather",
           {'mage': 15, 'cleric': 19, 'thief': 28, 'warrior': 22},
           {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
           spell_control_weather, TAR_IGNORE, POS_STANDING,
           None, SLOT(11), 25, 12, "", "!Control Weather!", "")