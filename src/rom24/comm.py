from collections import OrderedDict
from types import MethodType
import random
import time
import logging

logger = logging.getLogger(__name__)

from rom24 import db
from rom24 import game_utils
from rom24 import handler_game
from rom24 import merc
from rom24 import nanny
from rom24 import handler_ch
from rom24 import state_checks
from rom24 import instance


done = False


def process_input():
    for d in merc.descriptor_list:
        if d.active and d.cmd_ready and d.connected:
            d.connected()
            if d.is_connected(nanny.con_playing):
                ch = handler_ch.CH(d)
                if ch:
                    ch.timer = 0


def set_connected(self, state):
    self.connected = MethodType(state, self)


def is_connected(self, state):
    return self.connected == MethodType(state, self)


def process_output(self):
    ch = handler_ch.CH(self)
    if ch and self.is_connected(nanny.con_playing) and self.send_buffer:
        # /* battle prompt */
        if ch.fighting:
            victim = ch.fighting
            if victim and ch.can_see(victim):
                if victim.max_hit > 0:
                    percent = victim.hit * 100 / victim.max_hit
                else:
                    percent = -1
                if percent >= 100:
                    wound = "is in excellent condition."
                elif percent >= 90:
                    wound = "has a few scratches."
                elif percent >= 75:
                    wound = "has some small wounds and bruises."
                elif percent >= 50:
                    wound = "has quite a few wounds."
                elif percent >= 30:
                    wound = "has some big nasty wounds and scratches."
                elif percent >= 15:
                    wound = "looks pretty hurt."
                elif percent >= 0:
                    wound = "is in awful condition."
                else:
                    wound = "is bleeding to death."
                wound = "%s %s \n" % (state_checks.PERS(victim, ch), wound)
                wound = wound.capitalize()
                ch.send(wound)
        if not ch.comm.is_set(merc.COMM_COMPACT):
            self.send("\n")
        bust_a_prompt(ch)
    self.miniboa_send()


def init_descriptor(d):
    d.set_connected = MethodType(set_connected, d)
    d.is_connected = MethodType(is_connected, d)
    d.set_connected(nanny.con_get_name)
    greeting = random.choice(merc.greeting_list)
    d.send(greeting.text)
    d.active = True
    d.character = None
    d.original = None
    d.snoop_by = None
    d.close = d.deactivate
    # Gain control over process output without messing with miniboa.
    d.miniboa_send = d.socket_send
    d.socket_send = MethodType(process_output, d)
    merc.descriptor_list.append(d)
    d.request_terminal_type()
    d.request_naws()


# Check if already playing.
def check_playing(d, name):
    for dold in merc.descriptor_list:
        if (
            dold != d
            and dold.character
            and dold.connected != nanny.con_get_name
            and dold.connected != nanny.con_get_old_password
            and name == (dold.original.name if dold.original else dold.character.name)
        ):
            d.send("That character is already playing.\n")
            d.send("Do you wish to connect anyway (Y/N)?")
            d.set_connected(nanny.con_break_connect)
            return True
    return False


# Look for link-dead player to reconnect.
def check_reconnect(d, name, fConn):
    for ch in instance.players.values():
        if (
            not ch.is_npc()
            and (not fConn or not ch.desc)
            and d.character.name == ch.name
        ):
            if not fConn:
                d.character.pwd = ch.pwd
            else:
                d.character.pwd = ""
                del d.character
                d.character = ch
                ch.desc = d
                ch.timer = 0
                ch.send("Reconnecting. Type replay to see missed tells.\n")
                handler_game.act("$n has reconnected.", ch, None, None, merc.TO_ROOM)
                logger.info("%s@%s reconnected.", ch.name, d.host)
                handler_game.wiznet(
                    "$N groks the fullness of $S link.", ch, None, merc.WIZ_LINKS, 0, 0
                )
                d.set_connected(nanny.con_playing)
            return True
    return False


def close_socket(d):
    if d in merc.descriptor_list:
        merc.descriptor_list.remove(d)
    d.active = False


# * Bust a prompt (player settable prompt)
# * coded by Morgenes for Aldara Mud
def bust_a_prompt(ch):
    dir_name = ["N", "E", "S", "W", "U", "D"]
    room = ch.in_room
    doors = ""
    pstr = ch.prompt
    if not pstr:
        ch.send("<%dhp %dm %dmv> %s" % (ch.hit, ch.mana, ch.move, ch.prefix))
        return
    if ch.comm.is_set(merc.COMM_AFK):
        ch.send("<AFK> ")
        return
    replace = OrderedDict()
    found = False
    for door, pexit in enumerate(room.exit):
        if (
            pexit
            and (
                pexit.to_room
                and ch.can_see_room(pexit.to_room)
                or (
                    ch.is_affected(merc.AFF_INFRARED)
                    and not ch.is_affected(merc.AFF_BLIND)
                )
            )
            and not pexit.exit_info.is_set(merc.EX_CLOSED)
        ):
            found = True
            doors += dir_name[door]
    if not found:
        replace["%e"] = "none"
    else:
        replace["%e"] = doors
    replace["%c"] = "\n"
    replace["%h"] = "%s" % ch.hit
    replace["%H"] = "%s" % ch.max_hit
    replace["%m"] = "%d" % ch.mana
    replace["%M"] = "%d" % ch.max_mana
    replace["%v"] = "%d" % ch.move
    replace["%V"] = "%d" % ch.max_move
    replace["%x"] = "%d" % ch.exp
    replace["%X"] = "%d" % (
        0 if ch.is_npc() else (ch.level + 1) * ch.exp_per_level(ch.points) - ch.exp
    )
    replace["%g"] = "%ld" % ch.gold
    replace["%s"] = "%ld" % ch.silver
    if ch.level > 9:
        replace["%a"] = "%d" % ch.alignment
    else:
        replace["%a"] = (
            "%s" % "good" if ch.is_good() else "evil" if ch.is_evil() else "neutral"
        )

    if ch.in_room:
        if (not ch.is_npc() and ch.act.is_set(merc.PLR_HOLYLIGHT)) or (
            not ch.is_affected(merc.AFF_BLIND) and not ch.in_room.is_dark()
        ):
            replace["%r"] = ch.in_room.name
        else:
            replace["%r"] = "darkness"
    else:
        replace["%r"] = " "

    if ch.is_immortal() and ch.in_room:
        replace["%R"] = "%d" % ch.in_room.vnum
    else:
        replace["%R"] = " "

    if ch.is_immortal() and ch.in_room:
        replace["%z"] = "%s" % instance.area_templates[ch.in_room.area].name
    else:
        replace["%z"] = " "

    # replace['%%'] = '%'
    prompt = ch.prompt
    prompt = game_utils.mass_replace(prompt, replace)

    ch.send(prompt)
    if ch.prefix:
        ch.send(ch.prefix)

    ch.desc.send_ga()
    return


def is_reconnecting(d, name):
    for ch in instance.players.values():
        if not ch.desc and ch.name == name:
            return True
    return False


def game_loop(server):
    from rom24.update import update_handler
    from rom24.pyom import startup_time

    # import sysutils
    global done

    db.boot_db()

    boot_time = time.time()
    # boot_snapshot = sysutils.ResourceSnapshot()
    # logger.info(boot_snapshot.log_data())

    logger.info("Pyom database booted in %.3f seconds", (boot_time - startup_time))
    logger.info("Saving instances")
    instance.save()
    logger.info("Beginning server polling.")
    logger.info("Pyom is ready to rock on port %d", server.port)

    done = False
    errors = 0
    while not done:
        try:
            server.poll()
            process_input()
            update_handler()
        except Exception as e:
            logger.exception("Exception %s caught - continuing loop.", e)
            # Protect us from infinite errors.
            errors += 1
            if errors > 50:
                done = True
