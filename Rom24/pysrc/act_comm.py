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
from const import guild_table
from fight import stop_fighting

from merc import *
from nanny import con_playing
from save import save_char_obj
from nanny import con_playing
import interp
import comm
import os
from settings import PLAYER_DIR


def do_delet(self, argument):
    ch=self
    ch.send("You must type the full command to delete yourself.\n")


def do_delete(self, argument):
    ch=self
    if IS_NPC(ch):
        return

    if ch.pcdata.confirm_delete:
        if argument:
            ch.send("Delete status removed.\n")
            ch.pcdata.confirm_delete = False
            return
        else:
            pfile = os.path.join(PLAYER_DIR, ch.name+'.js')
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
    wiznet("$N is contemplating deletion.",ch,None,0,0,ch.get_trust())

# RT code to display channel status */

def do_channels(self, argument):
    ch=self
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
            ch.send("You display %d lines of scroll.\n" % ch.lines+2)
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
    ch=self
    if IS_SET(ch.comm, COMM_DEAF):
        ch.send("You can now hear tells again.\n")
        REMOVE_BIT(ch.comm,COMM_DEAF)
    else:
        ch.send("From now on, you won't hear tells.\n")
        SET_BIT(ch.comm,COMM_DEAF)

# RT quiet blocks out all communication */
def do_quiet(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_QUIET):
        ch.send("Quiet mode removed.\n")
        REMOVE_BIT(ch.comm,COMM_QUIET)
    else:
        ch.send("From now on, you will only hear says and emotes.\n")
        SET_BIT(ch.comm,COMM_QUIET)
# afk command */
def do_afk(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_AFK):
        ch.send("AFK mode removed. Type 'replay' to see tells.\n")
        REMOVE_BIT(ch.comm,COMM_AFK)
    else:
        ch.send("You are now in AFK mode.\n")
        SET_BIT(ch.comm,COMM_AFK)

def do_replay(self, argument):
    ch=self
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
    ch=self
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
        ch.send("You auction '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(D)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOAUCTION) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n auctions '$t'", ch,argument,d.character,TO_VICT,POS_DEAD)
# RT chat replaced with ROM gossip */
def do_gossip(self, argument):
    ch=self
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
        ch.send("You gossip '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOGOSSIP) and not IS_SET(victim.comm,COMM_QUIET):
                act( "$n gossips '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING )

def do_grats(self, argument):
    ch=self
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
        ch.send("You grats '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOGRATS) and not IS_SET(victim.comm,COMM_QUIET):
                act( "$n grats '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING )

def do_quote(self, argument):
    ch=self
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

        ch.send("You quote '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)

            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOQUOTE) and not IS_SET(victim.comm,COMM_QUIET):
                act( "$n quotes '$t'", ch,argument, d.character, TO_VICT,POS_SLEEPING )

# RT question channel */
def do_question(self, argument):
    ch=self
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

        ch.send( "You question '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOQUESTION) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n questions '$t'", ch,argument,d.character,TO_VICT,POS_SLEEPING)

# RT answer channel - uses same line as questions */
def do_answer(self, argument):
    ch=self
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
        ch.send("You answer '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOQUESTION) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n answers '$t'", ch,argument,d.character,TO_VICT,POS_SLEEPING)

# RT music channel */
def do_music(self, argument):
    ch=self
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

        ch.send("You MUSIC: '%s'\n" % argument )
        for d in descriptor_list:
            victim = CH(d)
            if d.is_connected(con_playing) and d.character != ch and not IS_SET(victim.comm,COMM_NOMUSIC) and not IS_SET(victim.comm,COMM_QUIET):
                act("$n MUSIC: '$t'",ch,argument,d.character,TO_VICT,POS_SLEEPING)

# clan channels */
def do_clantalk(self, argument):
    ch=self
    if not ch.is_clan() or ch.clan.independent:
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

    ch.send("You clan '%s'\n" % argument )
    for d in descriptor_list:
        if d.is_connected(con_playing) and d.character != ch and ch.is_same_clan(d.character) \
        and not IS_SET(d.character.comm,COMM_NOCLAN) and not IS_SET(d.character.comm,COMM_QUIET):
            act("$n clans '$t'",ch,argument,d.character,TO_VICT,POS_DEAD)

def do_immtalk(self, argument):
    ch=self
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
        if d.is_connected(con_playing) and IS_IMMORTAL(d.character) and not IS_SET(d.character.comm,COMM_NOWIZ):
            act("$n: $t",ch,argument,d.character,TO_VICT,POS_DEAD)

def do_say(self, argument):
    ch=self
    if not argument:
        ch.send("Say what?\n")
        return
    act( "$n says '$T'", ch, None, argument, TO_ROOM )
    act( "You say '$T'", ch, None, argument, TO_CHAR )
    return

def do_shout(self, argument):
    ch=self
    if not argument:
        if IS_SET(ch.comm, COMM_SHOUTSOFF):
            ch.send("You can hear shouts again.\n")
            REMOVE_BIT(ch.comm,COMM_SHOUTSOFF)
        else:
            ch.send("You will no longer hear shouts.\n")
            SET_BIT(ch.comm,COMM_SHOUTSOFF)
        return
    if IS_SET(ch.comm, COMM_NOSHOUT):
        ch.send("You can't shout.\n")
        return
    REMOVE_BIT(ch.comm,COMM_SHOUTSOFF)
    WAIT_STATE( ch, 12 )
    act( "You shout '$T'", ch, None, argument, TO_CHAR )
    for d in descriptor_list:
        victim = CH(d)
        if d.is_connected(con_playing) and d.character != ch \
        and not IS_SET(victim.comm, COMM_SHOUTSOFF) and not IS_SET(victim.comm, COMM_QUIET):
            act("$n shouts '$t'",ch,argument,d.character,TO_VICT)

def do_tell(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_NOTELL) or IS_SET(ch.comm, COMM_DEAF):
        ch.send("Your message didn't get through.\n")
        return
    if IS_SET(ch.comm, COMM_QUIET):
        ch.send("You must turn off quiet mode first.\n")
        return
    if IS_SET(ch.comm, COMM_DEAF):
        ch.send("You must turn off deaf mode first.\n")
        return
    argument, arg  = read_word(argument)

    if not arg or not argument:
        ch.send("Tell whom what?\n")
        return
     # Can tell to PC's anywhere, but NPC's only in same room.
     # -- Furey
    victim = ch.get_char_world(arg)
    if not victim or ( IS_NPC(victim) and victim.in_room != ch.in_room ):
        ch.send("They aren't here.\n")
        return
    if victim.desc == None and not IS_NPC(victim):
        act("$N seems to have misplaced $S link...try again later.", ch,None,victim,TO_CHAR)
        buf = "%s tells you '%s'\n" % (PERS(ch,victim),argument)
        victim.pcdata.buffer.append(buf)
        return

    if not (IS_IMMORTAL(ch) and ch.level > LEVEL_IMMORTAL) and not IS_AWAKE(victim):
        act( "$E can't hear you.", ch, 0, victim, TO_CHAR )
        return
  
    if (IS_SET(victim.comm,COMM_QUIET) or IS_SET(victim.comm,COMM_DEAF)) and not IS_IMMORTAL(ch):
        act( "$E is not receiving tells.", ch, 0, victim, TO_CHAR )
        return

    if IS_SET(victim.comm, COMM_AFK):
        if IS_NPC(victim):
            act("$E is AFK, and not receiving tells.",ch,None,victim,TO_CHAR)
            return
        act("$E is AFK, but your tell will go through when $E returns.", ch,None,victim,TO_CHAR)
        buf = "%s tells you '%s'\n" % (PERS(ch,victim),argument)
        victim.pcdata.buffer.append(buf)
        return
    act("You tell $N '$t'", ch, argument, victim, TO_CHAR )
    act("$n tells you '$t'",ch,argument,victim,TO_VICT,POS_DEAD)
    victim.reply   = ch
    return

def do_reply(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_NOTELL):
        ch.send("Your message didn't get through.\n")
        return
    if not ch.reply:
        ch.send("They aren't here.\n")
        return
    victim = ch
    if not victim.desc and not IS_NPC(victim):
        act("$N seems to have misplaced $S link...try again later.", ch,None,victim,TO_CHAR)
        buf = "%s tells you '%s'\n" % (PERS(ch,victim),argument)
        victim.pcdata.buffer.append(buf)
        return
    if not IS_IMMORTAL(ch) and not IS_AWAKE(victim):
        act( "$E can't hear you.", ch, 0, victim, TO_CHAR )
        return

    if (IS_SET(victim.comm,COMM_QUIET) or IS_SET(victim.comm,COMM_DEAF)) \
    and not IS_IMMORTAL(ch) and not IS_IMMORTAL(victim):
        act( "$E is not receiving tells.", ch, None, victim, TO_CHAR,POS_DEAD)
        return
    if not IS_IMMORTAL(victim) and not IS_AWAKE(ch):
        ch.send("In your dreams, or what?\n")
        return
    if IS_SET(victim.comm, COMM_AFK):
        if IS_NPC(victim):
            act("$E is AFK, and not receiving tells.", ch,None,victim,TO_CHAR,POS_DEAD)
            return
        act("$E is AFK, but your tell will go through when $E returns.", ch,None,victim,TO_CHAR,POS_DEAD)
        buf = "%s tells you '%s'\n" % ( PERS(ch,victim),argument)
        victim.pcdata.buffer.append(buf)
        return
    act("You tell $N '$t'",ch,argument,victim,TO_CHAR,POS_DEAD)
    act("$n tells you '$t'",ch,argument,victim,TO_VICT,POS_DEAD)
    victim.reply = ch
    return

def do_yell(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_NOSHOUT):
        ch.send("You can't yell.\n")
        return
 
    if not argument:
        ch.send("Yell what?\n")
        return

    act("You yell '$t'",ch,argument,None,TO_CHAR)
    for d in descriptor_list:
        if d.is_connected(con_playing) \
        and d.character != ch \
        and d.character.in_room != None \
        and d.character.in_room.area == ch.in_room.area \
        and not IS_SET(d.character.comm,COMM_QUIET):
            act("$n yells '$t'",ch,argument,d.character,TO_VICT)

def do_emote(self, argument):
    ch=self
    if not IS_NPC(ch) and IS_SET(ch.comm, COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    act( "$n $T", ch, None, argument, TO_ROOM )
    act( "$n $T", ch, None, argument, TO_CHAR )
    return

def do_pmote(self, argument):
    ch=self

    if not IS_NPC(ch) and IS_SET(ch.comm, COMM_NOEMOTE):
        ch.send("You can't show your emotions.\n")
        return
    if not argument:
        ch.send("Emote what?\n")
        return
    act( "$n $t", ch, argument, None, TO_CHAR )
    for vch in ch.in_room.people:
        if vch.desc == None or vch == ch:
            continue
        if vch.name not in argument:
            act("$N $t",vch,argument,ch,TO_CHAR)
            continue
        temp = mass_replace({vch.name:" you "}, argument)
        act("$N $t",vch,temp,ch,TO_CHAR)
    return

# All the posing stuff.
pose_table = [ [ [  "You sizzle with energy.",
                    "$n sizzles with energy.",
                    "You feel very holy.",
                    "$n looks very holy.",
                    "You perform a small card trick.",
                    "$n performs a small card trick.",
                    "You show your bulging muscles.",
                    "$n shows $s bulging muscles."
                 ]
               ],
               [ [  "You turn into a butterfly, then return to your normal shape.",
                    "$n turns into a butterfly, then returns to $s normal shape.",
                    "You nonchalantly turn wine into water.",
                    "$n nonchalantly turns wine into water.",
                    "You wiggle your ears alternately.",
                    "$n wiggles $s ears alternately.",
                    "You crack nuts between your fingers.",
                    "$n cracks nuts between $s fingers."
              ]  ],
              [  [  "Blue sparks fly from your fingers.",
                    "Blue sparks fly from $n's fingers.",
                    "A halo appears over your head.",
                    "A halo appears over $n's head.",
                    "You nimbly tie yourself into a knot.",
                    "$n nimbly ties $mself into a knot.",
                    "You grizzle your teeth and look mean.",
                    "$n grizzles $s teeth and looks mean."
              ]  ],
              [  [  "Little red lights dance in your eyes.",
                    "Little red lights dance in $n's eyes.",
                    "You recite words of wisdom.",
                    "$n recites words of wisdom.",
                    "You juggle with daggers, apples, and eyeballs.",
                    "$n juggles with daggers, apples, and eyeballs.",
                    "You hit your head, and your eyes roll.",
                    "$n hits $s head, and $s eyes roll."
              ]  ],
              [  [  "A slimy green monster appears before you and bows.",
                    "A slimy green monster appears before $n and bows.",
                    "Deep in prayer, you levitate.",
                    "Deep in prayer, $n levitates.",
                    "You steal the underwear off every person in the room.",
                    "Your underwear is gone!  $n stole it!",
                    "Crunch, crunch -- you munch a bottle.",
                    "Crunch, crunch -- $n munches a bottle."
              ]  ],
              [  [  "You turn everybody into a little pink elephant.",
                    "You are turned into a little pink elephant by $n.",
                    "An angel consults you.",
                    "An angel consults $n.",
                    "The dice roll ... and you win again.",
                    "The dice roll ... and $n wins again.",
                    "... 98, 99, 100 ... you do pushups.",
                    "... 98, 99, 100 ... $n does pushups."
              ]  ],
              [  [  "A small ball of light dances on your fingertips.",
                    "A small ball of light dances on $n's fingertips.",
                    "Your body glows with an unearthly light.",
                    "$n's body glows with an unearthly light.",
                    "You count the money in everyone's pockets.",
                    "Check your money, $n is counting it.",
                    "Arnold Schwarzenegger admires your physique.",
                    "Arnold Schwarzenegger admires $n's physique."
              ]  ],
              [  [  "Smoke and fumes leak from your nostrils.",
                    "Smoke and fumes leak from $n's nostrils.",
                    "A spot light hits you.",
                    "A spot light hits $n.",
                    "You balance a pocket knife on your tongue.",
                    "$n balances a pocket knife on your tongue.",
                    "Watch your feet, you are juggling granite boulders.",
                    "Watch your feet, $n is juggling granite boulders."
              ]  ],
              [  [  "The light flickers as you rap in magical languages.",
                    "The light flickers as $n raps in magical languages.",
                    "Everyone levitates as you pray.",
                    "You levitate as $n prays.",
                    "You produce a coin from everyone's ear.",
                    "$n produces a coin from your ear.",
                    "Oomph!  You squeeze water out of a granite boulder.",
                    "Oomph!  $n squeezes water out of a granite boulder."
              ]  ],
              [  [  "Your head disappears.",
                    "$n's head disappears.",
                    "A cool breeze refreshes you.",
                    "A cool breeze refreshes $n.",
                    "You step behind your shadow.",
                    "$n steps behind $s shadow.",
                    "You pick your teeth with a spear.",
                    "$n picks $s teeth with a spear."
              ]  ],
              [  [  "A fire elemental singes your hair.",
                    "A fire elemental singes $n's hair.",
                    "The sun pierces through the clouds to illuminate you.",
                    "The sun pierces through the clouds to illuminate $n.",
                    "Your eyes dance with greed.",
                    "$n's eyes dance with greed.",
                    "Everyone is swept off their foot by your hug.",
                    "You are swept off your feet by $n's hug."
              ]  ],
              [  [  "The sky changes color to match your eyes.",
                    "The sky changes color to match $n's eyes.",
                    "The ocean parts before you.",
                    "The ocean parts before $n.",
                    "You deftly steal everyone's weapon.",
                    "$n deftly steals your weapon.",
                    "Your karate chop splits a tree.",
                    "$n's karate chop splits a tree."
              ]  ],
              [  [  "The stones dance to your command.",
                    "The stones dance to $n's command.",
                    "A thunder cloud kneels to you.",
                    "A thunder cloud kneels to $n.",
                    "The Grey Mouser buys you a beer.",
                    "The Grey Mouser buys $n a beer.",
                    "A strap of your armor breaks over your mighty thews.",
                    "A strap of $n's armor breaks over $s mighty thews."
              ]  ],
              [  [  "The heavens and grass change colour as you smile.",
                    "The heavens and grass change colour as $n smiles.",
                    "The Burning Man speaks to you.",
                    "The Burning Man speaks to $n.",
                    "Everyone's pocket explodes with your fireworks.",
                    "Your pocket explodes with $n's fireworks.",
                    "A boulder cracks at your frown.",
                    "A boulder cracks at $n's frown."
              ]  ],
              [  [  "Everyone's clothes are transparent, and you are laughing.",
                    "Your clothes are transparent, and $n is laughing.",
                    "An eye in a pyramid winks at you.",
                    "An eye in a pyramid winks at $n.",
                    "Everyone discovers your dagger a centimeter from their eye.",
                    "You discover $n's dagger a centimeter from your eye.",
                    "Mercenaries arrive to do your bidding.",
                    "Mercenaries arrive to do $n's bidding."
              ]  ],
              [  [  "A black hole swallows you.",
                    "A black hole swallows $n.",
                    "Valentine Michael Smith offers you a glass of water.",
                    "Valentine Michael Smith offers $n a glass of water.",
                    "Where did you go?",
                    "Where did $n go?",
                    "Four matched Percherons bring in your chariot.",
                    "Four matched Percherons bring in $n's chariot."
              ]  ],
              [  [  "The world shimmers in time with your whistling.",
                    "The world shimmers in time with $n's whistling.",
                    "The great god Mota gives you a staff.",
                    "The great god Mota gives $n a staff.",
                    "Click.",
                    "Click.",
                    "Atlas asks you to relieve him.",
                    "Atlas asks $n to relieve him."
              ]  ]  ]

def do_pose(self, argument):
    ch=self

    if IS_NPC(ch):
        return
    level = min( ch.level, sizeof(pose_table) / sizeof(pose_table[0]) - 1 )
    pose  = random.randint(0, level)
    gn = 0
    for n, guild in enumerate(guild_table.values()):
        if guild == ch.guild:
          gn = n
    act( pose_table[pose][2*n+0], ch, None, None, TO_CHAR )
    act( pose_table[pose].message[2*n+1], ch, None, None, TO_ROOM )
    return

def do_bug(self, argument):
    ch=self
    append_file( ch, BUG_FILE, argument )
    ch.send("Bug logged.\n")
    return

def do_typo(self, argument):
    ch=self
    append_file( ch, TYPO_FILE, argument )
    ch.send("Typo logged.\n")
    return

def do_rent(self, argument):
    ch=self
    ch.send("There is no rent here.  Just save and quit.\n")
    return

def do_qui(self, argument):
    ch=self
    ch.send("If you want to QUIT, you have to spell it out.\n")
    return

def do_quit(self, argument):
    ch=self
    if IS_NPC(ch):
        return
    if ch.position == POS_FIGHTING:
        ch.send("No way! You are fighting.\n")
        return
    if ch.position < POS_STUNNED:
        ch.send("You're not DEAD yet.\n")
        return
    ch.send( "Alas, all good things must come to an end.\n")
    act( "$n has left the game.", ch, None, None, TO_ROOM )
    print ("%s has quit." % ch.name)
    wiznet("$N rejoins the real world.",ch,None,WIZ_LOGINS,0,ch.get_trust())
    #* After extract_char the ch is no longer valid!
    save_char_obj( ch )
    id = ch.id
    d = ch.desc
    ch.extract(True)
    if d != None:
        comm.close_socket( d )

    # toast evil cheating bastards */
    for d in descriptor_list[:]:
        tch = CH(d)
        if tch and tch.id == id:
            tch.extract(True)
            comm.close_socket(d)
    return

def do_save(self, argument):
    ch=self
    if IS_NPC(ch):
        return
    save_char_obj( ch )
    ch.send("Saving. Remember that ROM has automatic saving now.\n")
    WAIT_STATE(ch,4 * PULSE_VIOLENCE)
    return

def do_follow(self, argument):
    ch=self
# RT changed to allow unlimited following and follow the NOFOLLOW rules */
    argument, arg = read_word( argument )
    if not arg:
        ch.send("Follow whom?\n")
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if IS_AFFECTED(ch, AFF_CHARM) and ch.master:
        act( "But you'd rather follow $N!", ch, None, ch.master, TO_CHAR )
        return
    if victim == ch:
        if ch.master == None:
            ch.send("You already follow yourself.\n")
            return
        stop_follower(ch)
        return
    if not IS_NPC(victim) and IS_SET(victim.act,PLR_NOFOLLOW) and not IS_IMMORTAL(ch):
        act("$N doesn't seem to want any followers.\n", ch,None,victim, TO_CHAR)
        return
    REMOVE_BIT(ch.act,PLR_NOFOLLOW)
    if ch.master:
        stop_follower( ch )
    add_follower( ch, victim )
    return

def add_follower( ch, master ):
    if ch.master:
        print ("BUG: Add_follower: non-null master.")
        return
    ch.master        = master
    ch.leader        = None
    if master.can_see(ch):
        act( "$n now follows you.", ch, None, master, TO_VICT )
    act( "You now follow $N.",  ch, None, master, TO_CHAR )
    return

def stop_follower( ch ):
    if not ch.master:
        print ("BUG: Stop_follower: null master.")
        return

    if IS_AFFECTED(ch, AFF_CHARM):
        REMOVE_BIT( ch.affected_by, AFF_CHARM )
        ch.affect_strip('charm person')

    if ch.master.can_see(ch) and ch.in_room:
        act( "$n stops following you.", ch, None, ch.master, TO_VICT)
        act( "You stop following $N.", ch, None, ch.master, TO_CHAR)
    if ch.master.pet == ch:
        ch.master.pet = None
    ch.master = None
    ch.leader = None
    return

# nukes charmed monsters and pets */
def nuke_pets( ch ):
    if ch.pet:
        stop_follower(ch.pet)
        if ch.pet.in_room:
            act("$N slowly fades away.",ch,None,ch.pet,TO_NOTVICT)
        ch.pet.extract(True)
    ch.pet = None
    return

def die_follower(ch):
    if ch.master:
        if ch.master.pet == ch:
            ch.master.pet = None
        stop_follower( ch )
    ch.leader = None

    for fch in char_list[:]:
        if fch.master == ch:
            stop_follower( fch )
        if fch.leader == ch:
            fch.leader = fch
    return

def do_order(self, argument):
    ch=self

    argument, arg  = read_word(argument)
    remainder, arg2  = read_word(argument)

    if arg2 == "delete":
        ch.send("That will NOT be done.\n")
        return
    if not arg or not argument:
        ch.send("Order whom to do what?\n")
        return

    if IS_AFFECTED( ch, AFF_CHARM ):
        ch.send("You feel like taking, not giving, orders.\n")
        return
    victim = None
    if  arg == "all":
        fAll   = True
        victim = None
    else:
        fAll   = False
        victim = ch.get_char_room(arg)
        if not victim:
            ch.send("They aren't here.\n")
            return
        if victim == ch:
            ch.send("Aye aye, right away!\n")
            return
        if not IS_AFFECTED(victim, AFF_CHARM) or victim.master != ch  \
        or (IS_IMMORTAL(victim) and victim.trust >= ch.trust):
            ch.send("Do it yourself!\n")
            return
    found = False
    for och in ch.in_room.people[:]:
        if IS_AFFECTED(och, AFF_CHARM) \
        and och.master == ch \
        and ( fAll or och == victim ):
            found = True
            act( "$n orders you to '%s'." % argument, ch, None, och, TO_VICT )
            interpret( och, argument )

    if found:
        WAIT_STATE(ch,PULSE_VIOLENCE)
        ch.send("Ok.\n")
    else:
        ch.send("You have no followers here.\n")
    return

def do_group(self, argument):
    ch=self

    argument, arg = read_word(argument)
    if not arg:
        leader = ch.leader if ch.leader else ch
        ch.send("%s's group:\n" % PERS(leader, ch) )

        for gch in char_list:
            if gch.is_same_group(ch):
                ch.send( "[%2d %s] %-16s %4d/%4d hp %4d/%4d mana %4d/%4d mv %5d xp\n" % (
                          gch.level,
                          "Mob" if IS_NPC(gch) else gch.guild.who_name,
                          PERS(gch, ch),
                          gch.hit,   gch.max_hit,
                          gch.mana,  gch.max_mana,
                          gch.move,  gch.max_move,
                          gch.exp    ) )
        return
    victim = ch.get_char_room(arg)
    if not victim:
        ch.send("They aren't here.\n")
        return
    if ch.master or ( ch.leader and ch.leader != ch ):
        ch.send("But you are following someone else:!\n")
        return
    if victim.master != ch and ch != victim:
        act_new("$N isn't following you.",ch,None,victim,TO_CHAR,POS_SLEEPING)
        return
    if IS_AFFECTED(victim,AFF_CHARM):
        ch.send("You can't remove charmed mobs from your group.\n")
        return
    if IS_AFFECTED(ch,AFF_CHARM):
        act("You like your master too much to leave $m!", ch,None,victim,TO_VICT,POS_SLEEPING)
        return
    if victim.is_same_group(ch) and ch != victim:
        victim.leader = None
        act("$n removes $N from $s group.", ch,None,victim,TO_NOTVICT,POS_RESTING)
        act("$n removes you from $s group.", ch,None,victim,TO_VICT,POS_SLEEPING)
        act("You remove $N from your group.", ch,None,victim,TO_CHAR,POS_SLEEPING)
        return
    victim.leader = ch
    act_new("$N joins $n's group.",ch,None,victim,TO_NOTVICT,POS_RESTING)
    act_new("You join $n's group.",ch,None,victim,TO_VICT,POS_SLEEPING)
    act_new("$N joins your group.",ch,None,victim,TO_CHAR,POS_SLEEPING)
    return

# * 'Split' originally by Gnort, God of Chaos.
def do_split(self, argument):
    ch=self
    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)
    if not arg1:
        ch.send("Split how much?\n")
        return
    amount_gold = 0
    amount_silver = 0

    if arg1.is_digit():
        amount_silver = int(arg1)
    if arg2.is_digit():
        amount_gold = int(arg2)
    if amount_gold < 0 or amount_silver < 0:
        ch.send("Your group wouldn't like that.\n")
        return
    if amount_gold == 0 and amount_silver == 0:
        ch.send("You hand out zero coins, but no one notices.\n")
        return
    if ch.gold <  amount_gold or ch.silver < amount_silver:
        ch.send("You don't have that much to split.\n")
        return
    members = 0
    for gch in ch.in_room.people[:]:
        if gch.is_same_group(ch) and not IS_AFFECTED(gch,AFF_CHARM):
            members+=1
    if members < 2:
        ch.send("Just keep it all.\n")
        return
    share_silver = amount_silver / members
    extra_silver = amount_silver % members
    share_gold   = amount_gold / members
    extra_gold   = amount_gold % members
    if share_gold == 0 and share_silver == 0:
        ch.send("Don't even bother, cheapskate.\n")
        return
    ch.silver -= amount_silver
    ch.silver += share_silver + extra_silver
    ch.gold -= amount_gold
    ch.gold += share_gold + extra_gold
    if share_silver > 0:
        ch.send("You split %d silver coins. Your share is %d silver.\n" % (amount_silver,share_silver + extra_silver))
    if share_gold > 0:
        ch.send("You split %d gold coins. Your share is %d gold.\n" % (amount_gold,share_gold + extra_gold))
    if share_gold == 0:
        buf = "$n splits %d silver coins. Your share is %d silver." % (amount_silver,share_silver)
    elif share_silver == 0:
        buf = "$n splits %d gold coins. Your share is %d gold." % (amount_gold,share_gold)
    else:
        buf = '$n splits %d silver and %d gold coins, giving you %d silver and %d gold.\n' % (amount_silver,amount_gold,share_silver,share_gold)

    for gch in ch.in_room.people[:]:
        if gch != ch and gch.is_same_group(ch) and not IS_AFFECTED(gch,AFF_CHARM):
            act( buf, ch, None, gch, TO_VICT )
            gch.gold += share_gold
            gch.silver += share_silver
    return

def do_gtell(self, argument):
    ch=self
    if not argument:
        ch.send("Tell your group what?\n")
        return
    if IS_SET(ch.comm, COMM_NOTELL ):
        ch.send("Your message didn't get through!\n")
        return

    for gch in char_list[:]:
        if gch.is_same_group(ch):
          act("$n tells the group '$t'", ch,argument,gch,TO_VICT,POS_SLEEPING)
    return

def do_commands(self, argument):
    ch = self
    col = 0;
    for key, cmd in interp.cmd_table.items():
        if cmd.level <  LEVEL_HERO and cmd.level <= ch.get_trust() and cmd.show:
            ch.send("%-12s" % key)
            col += 1
            if col % 6 == 0:
                ch.send("\n")
    if col % 6 != 0:
        ch.send("\n")
    return
def do_wizhelp(self, argument):
    ch = self
    col = 0;
    for key, cmd in interp.cmd_table.items():
        if cmd.level >= LEVEL_HERO and cmd.level <= ch.get_trust()  and cmd.show:
            ch.send("%-12s" % key)
            col += 1
            if col % 6 == 0:
                ch.send("\n")

    if col % 6 != 0:
        ch.send("\n")
    return
