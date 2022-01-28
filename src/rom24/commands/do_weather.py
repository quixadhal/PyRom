import logging

logger = logging.getLogger(__name__)

from rom24 import handler_game
from rom24 import merc
from rom24 import interp
from rom24 import state_checks


def do_weather(ch, argument):
    sky_look = ["cloudless", "cloudy", "rainy", "lit by flashes of lightning"]
    if not state_checks.IS_OUTSIDE(ch):
        ch.send("You can't see the weather indoors.\n")
        return

    ch.send(
        "The sky is %s and %s.\n"
        % (
            sky_look[handler_game.weather_info.sky],
            "a warm southerly breeze blows"
            if handler_game.weather_info.change >= 0
            else "a cold northern gust blows",
        )
    )
    return


interp.register_command(
    interp.cmd_type("weather", do_weather, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
