"""
/***************************************************************************
 *  Original Diku Mud copyright (C) 1990, 1991 by Sebastian Hammer,        *
 *  Michael Seifert, Hans Henrik St{rfeldt, Tom Madsen, and Katja Nyboe.   *
 *                                                                         *
 *  Merc Diku Mud improvments copyright (C) 1992, 1993 by Michael          *
 *  Chastain, Michael Quan, and Mitchell Tse.                              *
 *                                                                         *
 *  In order to use any part of this Merc Diku Mud, you must comply with   *
 *  both the original Diku license in 'license.doc' as well the Merc       *
 *  license in 'license.txt'.  In particular, you may not remove either of *
 *  these copyright notices.                                               *
 *                                                                         *
 *  Much time and thought has gone into this software and you are          *
 *  benefitting.  We hope that you share your changes too.  What goes      *
 *  around, comes around.                                                  *
 ***************************************************************************/

/***************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
/************
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/ 
 ************/
"""

from merc import *
from handler import get_trust, extract_char, wiznet
from save import save_char_obj
import comm

def do_delet(self, argument):
    ch = self
    ch.send("You must type the full command to delete yourself.\n")


def do_delete(self, argument):
    ch = self
    if IS_NPC(ch):
        return

    if ch.pcdata.confirm_delete:
        if argument:
            ch.send("Delete status removed.\n")
            ch.pcdata.confirm_delete = False
            return
        else:
            pfile = os.path.join(PLAYER_DIR, ch.name + '.js')
            wiznet("$N turns $Mself into line noise.",ch,None,0,0,0)
            stop_fighting(ch,True)
            ch.do_quit("")
            os.remove(pfile)
            return
    if argument:
        ch.send("Just type delete. No argument.\n")
        return

    ch.send("Type delete again to confirm this command.\n")
    ch.send("WARNING: this command is irreversible.\n")
    ch.send("Typing delete with an argument will undo delete status.\n")
    ch.pcdata.confirm_delete = True
    wiznet("$N is contemplating deletion.",ch,None,0,0,get_trust(ch))

# RT code to display channel status */
def do_channels(self, argument):
    ch = self
    # lists all channels and their status */
    ch.send("   channel     status\n")
    ch.send("---------------------\n")
    ch.send("gossip         ")
    if not IS_SET(ch.comm, COMM_NOGOSSIP):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("auction        ")
    if not IS_SET(ch.comm, COMM_NOAUCTION):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("music          ")
    if not IS_SET(ch.comm, COMM_NOMUSIC):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("Q/A            ")
    if not IS_SET(ch.comm, COMM_NOQUESTION):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("Quote          ")
    if not IS_SET(ch.comm, COMM_NOQUOTE):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("grats          ")
    if not IS_SET(ch.comm, COMM_NOGRATS):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")

    if IS_IMMORTAL(ch):
        ch.send("god channel    ")
        if not IS_SET(ch.comm, COMM_NOWIZ):
            ch.send("ON\n")
        else:
            ch.send("OFF\n")
    ch.send("shouts         ")
    if not IS_SET(ch.comm, COMM_SHOUTSOFF):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("tells          ")
    if not IS_SET(ch.comm, COMM_DEAF):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    ch.send("quiet mode     ")
    if IS_SET(ch.comm, COMM_QUIET):
        ch.send("ON\n")
    else:
        ch.send("OFF\n")
    if IS_SET(ch.comm, COMM_AFK):
        ch.send("You are AFK.\n")
    if IS_SET(ch.comm, COMM_SNOOP_PROOF):
        ch.send("You are immune to snooping.\n")
    if ch.lines != PAGELEN:
        if ch.lines:
            ch.send("You display %d lines of scroll.\n" % ch.lines + 2)
        else:
            ch.send("Scroll buffering is off.\n")
    if ch.prompt:
        ch.send("Your current prompt is: %s\n" % ch.prompt)
    if IS_SET(ch.comm, COMM_NOSHOUT):
        ch.send("You cannot shout.\n")
    if IS_SET(ch.comm, COMM_NOTELL):
        ch.send("You cannot use tell.\n")
    if IS_SET(ch.comm, COMM_NOCHANNELS):
        ch.send("You cannot use channels.\n")
    if IS_SET(ch.comm, COMM_NOEMOTE):
        ch.send("You cannot show emotions.\n")

# RT deaf blocks out all shouts */
def do_deaf(self, argument):
    ch = self
    if IS_SET(ch.comm, COMM_DEAF):
        ch.send("You can now hear tells again.\n")
        REMOVE_BIT(ch.comm,COMM_DEAF)
    else:
        ch.send("From now on, you won't hear tells.\n")
        SET_BIT(ch.comm,COMM_DEAF)

# RT quiet blocks out all communication */
def do_quiet(self, argument):
    ch = self
    if IS_SET(ch.comm, COMM_QUIET):
        ch.send("Quiet mode removed.\n")
        REMOVE_BIT(ch.comm,COMM_QUIET)
    else:
        ch.send("From now on, you will only hear says and emotes.\n")
        SET_BIT(ch.comm,COMM_QUIET)
# afk command */
def do_afk(self, argument):
    ch = self
    if IS_SET(ch.comm, COMM_AFK):
        ch.send("AFK mode removed. Type 'replay' to see tells.\n")
        REMOVE_BIT(ch.comm,COMM_AFK)
    else:
        ch.send("You are now in AFK mode.\n")
        SET_BIT(ch.comm,COMM_AFK)

def do_replay(self, argument):
    ch = self
    if IS_NPC(ch):
        ch.send("You can't replay.\n")
        return

    if not ch.pcdata.buffer:
        ch.send("You have no tells to replay.\n")
        return

    [ch.send(tell) for tell in ch.pcdata.buffer]
    ch.pcdata.buffer = []

# RT auction rewritten in ROM style */
def do_auction(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOAUCTION):
            ch.send("Auction channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOAUCTION)
        else:
            ch.send("Auction channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOAUCTION)
    else:  # auction message sent, turn auction on if it is off */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return

        REMOVE_BIT(ch.comm,COMM_NOAUCTION)
        ch.send("You auction '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(D)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOAUCTION) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n auctions '$t'", ch,argument,d.character,TO_VICT,POS_DEAD)
# RT chat replaced with ROM gossip */
def do_gossip(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOGOSSIP):
            ch.send("Gossip channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOGOSSIP)
        else:
            ch.send("Gossip channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOGOSSIP)
    else:  # gossip message sent, turn gossip on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOGOSSIP)
        ch.send("You gossip '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOGOSSIP) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n gossips '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING)

def do_grats(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOGRATS):
            ch.send("Grats channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOGRATS)
        else:
            ch.send("Grats channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOGRATS)
    else:  # grats message sent, turn grats on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOGRATS)
        ch.send("You grats '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOGRATS) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n grats '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING)

def do_quote(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOQUOTE):
            ch.send("Quote channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOQUOTE)
        else:
            ch.send("Quote channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOQUOTE)
    else:  # quote message sent, turn quote on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOQUOTE)

        ch.send("You quote '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)

            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOQUOTE) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n quotes '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING)

# RT question channel */
def do_question(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOQUESTION):
            ch.send("Q/A channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOQUESTION)
        else:
            ch.send("Q/A channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOQUESTION)
    else:  # question sent, turn Q/A on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOQUESTION)

        ch.send("You question '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOQUESTION) and not IS_SET(victim.comm,COMM_QUIET):
                act_new("$n questions '$t'", ch,argument,d.character,TO_VICT,POS_SLEEPING)

# RT answer channel - uses same line as questions */
def do_answer(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOQUESTION):
            ch.send("Q/A channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOQUESTION)
        else:
            ch.send("Q/A channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOQUESTION)
    else:  # answer sent, turn Q/A on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOQUESTION)
        ch.send("You answer '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOQUESTION) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n answers '$t'", ch,argument,d.character,TO_VICT,POS_SLEEPING)

# RT music channel */
def do_music(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOMUSIC):
            ch.send("Music channel is now ON.\n")
            REMOVE_BIT(ch.comm,COMM_NOMUSIC)
        else:
            ch.send("Music channel is now OFF.\n")
            SET_BIT(ch.comm,COMM_NOMUSIC)
    else:  # music sent, turn music on if it isn't already */
        if IS_SET(ch.comm, COMM_QUIET):
            ch.send("You must turn off quiet mode first.\n")
            return
        if IS_SET(ch.comm, COMM_NOCHANNELS):
            ch.send("The gods have revoked your channel priviliges.\n")
            return
        REMOVE_BIT(ch.comm,COMM_NOMUSIC)

        ch.send("You MUSIC: '%s'\n" % argument)
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing and d.character != ch and not IS_SET(victim.comm,COMM_NOMUSIC) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n MUSIC: '$t'",ch,argument,d.character,TO_VICT,POS_SLEEPING)

# clan channels */
def do_clantalk(self, argument):
    ch = self
    if not is_clan(ch) or ch.clan.independent:
        ch.send("You aren't in a clan.\n")
        return
    if not argument:
        if IS_SET(ch.comm, COMM_NOCLAN):
            ch.send("Clan channel is now ON\n")
            REMOVE_BIT(ch.comm,COMM_NOCLAN)
        else:
            ch.send("Clan channel is now OFF\n")
            SET_BIT(ch.comm,COMM_NOCLAN)
        return
    if IS_SET(ch.comm, COMM_NOCHANNELS):
        ch.send("The gods have revoked your channel priviliges.\n")
        return

    REMOVE_BIT(ch.comm,COMM_NOCLAN)

    ch.send("You clan '%s'\n" % argument)
    for d in descriptor_list:
        if d.connected == con_playing and d.character != ch and is_same_clan(ch,d.character) \
        and not IS_SET(d.character.comm,COMM_NOCLAN) and not IS_SET(d.character.comm,COMM_QUIET):
            act("$n clans '$t'",ch,argument,d.character,TO_VICT,POS_DEAD)

def do_immtalk(self, argument):
    ch = self
    if not argument:
        if IS_SET(ch.comm, COMM_NOWIZ):
            ch.send("Immortal channel is now ON\n")
            REMOVE_BIT(ch.comm,COMM_NOWIZ)
        else:
            ch.send("Immortal channel is now OFF\n")
            SET_BIT(ch.comm,COMM_NOWIZ)
        return
  
    REMOVE_BIT(ch.comm,COMM_NOWIZ)
    act("$n: $t",ch,argument,None,TO_CHAR,POS_DEAD)
    for d in descriptor_list:
        if d.connected == CON_PLAYING and IS_IMMORTAL(d.character) and not IS_SET(d.character.comm,COMM_NOWIZ):
            act("$n: $t",ch,argument,d.character,TO_VICT,POS_DEAD)

def do_say(self, argument):
    ch = self
    if not argument:
        ch.send("Say what?\n")
        return
    act("$n says '$T'", ch, None, argument, TO_ROOM)
    act("You say '$T'", ch, None, argument, TO_CHAR)
    return
