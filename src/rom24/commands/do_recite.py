import logging

logger = logging.getLogger(__name__)

import random
from rom24 import merc
from rom24 import interp
from rom24 import game_utils
from rom24 import handler_game
from rom24 import handler_magic


def do_recite(ch, argument):
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    scroll = ch.get_item_carry(arg1, ch)
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
        obj = ch.get_item_here(arg2)
        if not victim and not obj:
            ch.send("You can't find it.\n")
            return
        handler_game.act("$n recites $p.", ch, scroll, None, merc.TO_ROOM)
        handler_game.act("You recite $p.", ch, scroll, None, merc.TO_CHAR)

    if random.randint(1, 99) >= 20 + ch.get_skill("scrolls") * 4 // 5:
        ch.send("You mispronounce a syllable.\n")
        if ch.is_pc:
            ch.check_improve("scrolls", False, 2)
    else:
        handler_magic.obj_cast_spell(scroll.value[1], scroll.value[0], ch, victim, obj)
        handler_magic.obj_cast_spell(scroll.value[2], scroll.value[0], ch, victim, obj)
        handler_magic.obj_cast_spell(scroll.value[3], scroll.value[0], ch, victim, obj)
        if ch.is_pc:
            ch.check_improve("scrolls", True, 2)
    scroll.extract()
    return


interp.register_command(
    interp.cmd_type("recite", do_recite, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1)
)
