import const
import game_utils
import handler_game
import merc


def spell_control_weather(sn, level, ch, victim, target):
    if victim.lower() == "better":
        handler_game.weather_info.change += game_utils.dice(level // 3, 4)
    elif victim.lower() == "worse":
        handler_game.weather_info.change -= game_utils.dice(level // 3, 4)
    else:
        ch.send("Do you want it to get better or worse?\n")

    ch.send("Ok.\n")
    return


const.register_spell(const.skill_type("control weather",
                          {'mage': 15, 'cleric': 19, 'thief': 28, 'warrior': 22},
                          {'mage': 1, 'cleric': 1, 'thief': 2, 'warrior': 2},
                          spell_control_weather, merc.TAR_IGNORE, merc.POS_STANDING,
                          None, const.SLOT(11), 25, 12, "", "!Control Weather!", ""))
