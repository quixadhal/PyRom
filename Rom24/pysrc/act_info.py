"""
#**************************************************************************
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

#**************************************************************************
*   ROM 2.4 is copyright 1993-1998 Russ Taylor                             *
*   ROM has been brought to you by the ROM consortium                      *
*       Russ Taylor (rtaylor@hypercube.org)                                *
*       Gabrielle Taylor (gtaylor@hypercube.org)                           *
*       Brian Moore (zump@rom.org)                                         *
*   By using this code, you have agreed to follow the terms of the         *
*   ROM license, in the file Rom24/doc/rom.license                         *
***************************************************************************/
#***********
 * Ported to Python by Davion of MudBytes.net
 * Using Miniboa https://code.google.com/p/miniboa/
 ************/
"""
from collections import OrderedDict
from merc import *
from nanny import con_playing, con_gen_groups
from handler import *
from act_move import dir_name
from db import get_extra_descr

where_name = ["<used as light>     ",
              "<worn on finger>    ",
              "<worn on finger>    ",
              "<worn around neck>  ",
              "<worn around neck>  ",
              "<worn on torso>     ",
              "<worn on head>      ",
              "<worn on legs>      ",
              "<worn on feet>      ",
              "<worn on hands>     ",
              "<worn on arms>      ",
              "<worn as shield>    ",
              "<worn about body>   ",
              "<worn about waist>  ",
              "<worn around wrist> ",
              "<worn around wrist> ",
              "<wielded>           ",
              "<held>              ",
              "<floating nearby>   "]

# for  keeping track of the player count */
max_on = 0

def format_obj_to_char(obj, ch, fShort):
    buf = ''
    if (fShort and not obj.short_descr) or not obj.description:
        return buf

    if IS_OBJ_STAT(obj, ITEM_INVIS): buf += "(Invis) "
    if IS_AFFECTED(ch, AFF_DETECT_EVIL) \
         and IS_OBJ_STAT(obj, ITEM_EVIL): buf += "(Red Aura) "
    if IS_AFFECTED(ch, AFF_DETECT_GOOD) \
    and  IS_OBJ_STAT(obj, ITEM_BLESS): buf += "(Blue Aura) "
    if IS_AFFECTED(ch, AFF_DETECT_MAGIC) \
         and IS_OBJ_STAT(obj, ITEM_MAGIC): buf += "(Magical) "
    if IS_OBJ_STAT(obj, ITEM_GLOW): buf += "(Glowing) "
    if IS_OBJ_STAT(obj, ITEM_HUM): buf += "(Humming) "

    if fShort:
        if obj.short_descr:
            buf += obj.short_descr
    else:
        if obj.description:
            buf += obj.description
    return buf

# * Show a list to a character.
# * Can coalesce duplicated items.
def show_list_to_char(clist, ch, fShort, fShowNothing):
    if not ch.desc:
        return
    objects = OrderedDict()
    for obj in clist:
        if obj.wear_loc == WEAR_NONE and can_see_obj(ch, obj):
            frmt = format_obj_to_char(obj, ch, fShort)
            if frmt not in objects:
                objects[frmt] = 1
            else:
                objects[frmt] += 1


    if not objects and fShowNothing:
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE):
            ch.send("     ")
        ch.send("Nothing.\r\n")

     #* Output the formatted list.
    for desc, count in objects:
        if IS_NPC(ch) or IS_SET(ch.comm, COMM_COMBINE) and count > 1:
            ch.send("(%2d) %s\r\n" % (count, desc))
        else:
            for i in range(count):
                ch.send("     %s\r\n")

def show_char_to_char_0(victim, ch):
    buf = ''
    if IS_SET(victim.comm, COMM_AFK): buf += "[AFK] "
    if IS_AFFECTED(victim, AFF_INVISIBLE): buf += "(Invis) "
    if victim.invis_level >= LEVEL_HERO: buf += "(Wizi) "
    if IS_AFFECTED(victim, AFF_HIDE): buf += "(Hide) "
    if IS_AFFECTED(victim, AFF_CHARM): buf += "(Charmed) "
    if IS_AFFECTED(victim, AFF_PASS_DOOR): buf += "(Translucent) "
    if IS_AFFECTED(victim, AFF_FAERIE_FIRE): buf += "(Pink Aura) "
    if IS_EVIL(victim) and IS_AFFECTED(ch, AFF_DETECT_EVIL): buf += "(Red Aura) "
    if IS_GOOD(victim) and IS_AFFECTED(ch, AFF_DETECT_GOOD): buf += "(Golden Aura) "
    if IS_AFFECTED(victim, AFF_SANCTUARY): buf += "(White Aura) "
    if not IS_NPC(victim) and IS_SET(victim.act, PLR_KILLER): buf += "(KILLER) "
    if not IS_NPC(victim) and IS_SET(victim.act, PLR_THIEF): buf += "(THIEF) "

    if victim.position == victim.start_pos and victim.long_descr:
        buf += victim.long_descr
        ch.send(buf)
        return

    buf += PERS(victim, ch)
    if not IS_NPC(victim) and not IS_SET(ch.comm, COMM_BRIEF) \
    and victim.position == POS_STANDING and not ch.on:
        buf += victim.pcdata.title

    if victim.position == POS_DEAD: buf += " is DEAD!!"
    elif victim.position == POS_MORTAL: buf += " is mortally wounded."
    elif victim.position == POS_INCAP: buf += " is incapacitated."
    elif victim.position == POS_STUNNED: buf += " is lying here stunned."
    elif victim.position == POS_SLEEPING:
        if victim.on:
            if IS_SET(victim.on.value[2], SLEEP_AT):
                buf += " is sleeping at %s." % (victim.on.short_descr)
            elif IS_SET(victim.on.value[2], SLEEP_ON):
                buf += " is sleeping on %s." % (victim.on.short_descr)
            else:
                buf += " is sleeping in %s." % (victim.on.short_descr)
        else:
            buf += " is sleeping here."
    elif victim.position == POS_RESTING:
        if victim.on:
            if IS_SET(victim.on.value[2], REST_AT):
                buf += " is resting at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], REST_ON):
                buf += " is resting on %s." % victim.on.short_descr
            else:
                buf += " is resting in %s." % victim.on.short_descr
        else:
            buf += " is resting here."
    elif victim.position == POS_SITTING:
        if victim.on:
            if IS_SET(victim.on.value[2], SIT_AT):
                buf += " is sitting at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], SIT_ON):
                buf += " is sitting on %s." % victim.on.short_descr
            else:
                buf += " is sitting in %s." % victim.on.short_descr
        else:
            buf += " is sitting here."
    elif victim.position == POS_STANDING:
        if victim.on:
            if IS_SET(victim.on.value[2], STAND_AT):
                buf += " is standing at %s." % victim.on.short_descr
            elif IS_SET(victim.on.value[2], STAND_ON):
                buf += " is standing on %s." % victim.on.short_descr
            else:
                buf += " is standing in %s." % victim.on.short_descr
        else:
            buf += " is here."
    elif victim.position == POS_FIGHTING:
        buf += " is here, fighting "
        if not victim.fighting:
            buf += "thin air??"
        elif victim.fighting == ch:
            buf += "YOU!"
        elif victim.in_room == victim.fighting.in_room:
            buf += "%s." % PERS(victim.fighting, ch)
        else:
            buf += "someone who left??"
    buf += "\n\r"
    buf = buf.capitalize()
    ch.send(buf)
    return

def show_char_to_char_1(victim, ch):
    if can_see(victim, ch):
        if ch == victim:
            act("$n looks at $mself.", ch, None, None, TO_ROOM)
        else:
            act("$n looks at you.", ch, None, victim, TO_VICT)
            act("$n looks at $N.",  ch, None, victim, TO_NOTVICT)
    if victim.description:
        ch.send(victim.description)
    else:
        act("You see nothing special about $M.", ch, None, victim, TO_CHAR)
    if victim.max_hit > 0:
        percent = (100 * victim.hit) / victim.max_hit
    else:
        percent = -1
    buf = PERS(victim, ch)
    if percent >= 100: buf += " is in excellent condition.\n\r"
    elif percent >= 90: buf += " has a few scratches.\n\r"
    elif percent >= 75: buf += " has some small wounds and bruises.\n\r"
    elif percent >=  50: buf += " has quite a few wounds.\n\r"
    elif percent >= 30: buf += " has some big nasty wounds and scratches.\n\r"
    elif percent >= 15: buf += " looks pretty hurt.\n\r"
    elif percent >= 0: buf += " is in awful condition.\n\r"
    else: buf += " is bleeding to death.\n\r"

    buf = buf.capitalize()
    ch.send(buf)

    found = False
    for iWear in range(MAX_WEAR):
        obj = get_eq_char(victim,iWear)
        if obj and can_see_obj(ch, obj):
            if not found:
                ch.send("\n\r")
                act("$N is using:", ch, None, victim, TO_CHAR)
                found = True
            ch.send(where_name[iWear])
            ch.send(format_obj_to_char(obj, ch, True))
            ch.send("\n\r")

    if victim != ch and not IS_NPC(ch) and random.randint(1,99) < get_skill(ch,gsn_peek):
        ch.send("\n\rYou peek at the inventory:\n\r")
        check_improve(ch,'peek',True,4)
        show_list_to_char(victim.carrying, ch, True, True)
    return

def show_char_to_char(list, ch):
    for rch in list:
        if rch == ch:
                continue

        if get_trust(ch) < rch.invis_level:
            continue

        if can_see(ch, rch):
            show_char_to_char_0(rch, ch);
        elif room_is_dark(ch.in_room) and IS_AFFECTED(rch, AFF_INFRARED):
            ch.send("You see glowing red eyes watching YOU!\r\n")

def check_blind(ch):
    if not IS_NPC(ch) and IS_SET(ch.act,PLR_HOLYLIGHT):
        return True
    if IS_AFFECTED(ch, AFF_BLIND):
        ch.send("You can't see a thing!\n\r") 
        return False 
    return True

# changes your scroll */
def do_scroll(self, argument):
    ch=self
    argument, arg = read_word(argument)
    
    if not arg:
        if ch.lines == 0:
            ch.send("You do not page long messages.\n\r")
        else:
            ch.send("You currently display %d lines per page.\n\r" % ch.lines + 2)
        return
    if not arg.is_digit():
        ch.send("You must provide a number.\n\r")
        return
    lines = int(arg)
    if lines == 0:
        ch.send("Paging disabled.\n\r")
        ch.lines = 0
        return
    if lines < 10 or lines > 100:
        ch.send("You must provide a reasonable number.\n\r")
        return
    ch.send("Scroll set to %d lines.\n\r" % lines)
    ch.lines = lines - 2

# RT does socials */
def do_socials(self, argument):
    ch=self
    for col, social in enumerate(social_list):
        ch.send("%-12s" % social.name)
        if col % 6 == 0:
            ch.send("\n\r")
    if len(social_list) % 6 != 0:
        ch.send("\n\r")
    return

# RT Commands to replace news, motd, imotd, etc from ROM */
def do_motd(self, argument):
    ch=self
    ch.do_help("motd")

def do_imotd(self, argument):
    ch=self
    ch.do_help("imotd")

def do_rules(self, argument):
    ch=self
    ch.do_help("rules")

def do_story(self, argument):
    ch=self
    ch.do_help("story")

def do_wizlist(self, argument):
    ch=self
    ch.do_help("wizlist")
# RT this following section holds all the auto commands from ROM, as well as
#   replacements for config */

def do_autolist(self, argument):
    ch=self
    # lists most player flags */
    if IS_NPC(ch):
      return

    ch.send("   action     status\n\r")
    ch.send("---------------------\n\r")
 
    ch.send("autoassist     ")
    if IS_SET(ch.act, PLR_AUTOASSIST):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r") 

    ch.send("autoexit       ")
    if IS_SET(ch.act, PLR_AUTOEXIT):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("autogold       ")
    if IS_SET(ch.act, PLR_AUTOGOLD):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("autoloot       ")
    if IS_SET(ch.act, PLR_AUTOLOOT):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("autosac        ")
    if IS_SET(ch.act, PLR_AUTOSAC):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("autosplit      ")
    if IS_SET(ch.act, PLR_AUTOSPLIT):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("compact mode   ")
    if IS_SET(ch.comm, COMM_COMPACT):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("prompt         ")
    if IS_SET(ch.comm, COMM_PROMPT):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")

    ch.send("combine items  ")
    if IS_SET(ch.comm, COMM_COMBINE):
        ch.send("ON\n\r")
    else:
        ch.send("OFF\n\r")
    if not IS_SET(ch.act, PLR_CANLOOT):
        ch.send("Your corpse is safe from thieves.\n\r")
    else: 
        ch.send("Your corpse may be looted.\n\r")
    if IS_SET(ch.act, PLR_NOSUMMON):
        ch.send("You cannot be summoned.\n\r")
    else:
        ch.send("You can be summoned.\n\r")
    if IS_SET(ch.act, PLR_NOFOLLOW):
        ch.send("You do not welcome followers.\n\r")
    else:
        ch.send("You accept followers.\n\r")

def do_autoassist(self, argument):
    ch=self
    if IS_NPC(ch):
      return
    
    if IS_SET(ch.act, PLR_AUTOASSIST):
        ch.send("Autoassist removed.\n\r")
        ch.act = REMOVE_BIT(ch.act,PLR_AUTOASSIST)
    else:
        ch.send("You will now assist when needed.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOASSIST)

def do_autoexit(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_AUTOEXIT):
        ch.send("Exits will no longer be displayed.\n\r")
        REMOVE_BIT(ch.act,PLR_AUTOEXIT)
    else:
        ch.send("Exits will now be displayed.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOEXIT)

def do_autogold(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_AUTOGOLD):
        ch.send("Autogold removed.\n\r")
        REMOVE_BIT(ch.act,PLR_AUTOGOLD)
    else:
        ch.send("Automatic gold looting set.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOGOLD)

def do_autoloot(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_AUTOLOOT):
        ch.send("Autolooting removed.\n\r")
        REMOVE_BIT(ch.act,PLR_AUTOLOOT)
    else:
        ch.send("Automatic corpse looting set.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOLOOT)

def do_autosac(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_AUTOSAC):
        ch.send("Autosacrificing removed.\n\r")
        REMOVE_BIT(ch.act,PLR_AUTOSAC)
    else:
        ch.send("Automatic corpse sacrificing set.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOSAC)

def do_autosplit(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_AUTOSPLIT):
        ch.send("Autosplitting removed.\n\r")
        REMOVE_BIT(ch.act,PLR_AUTOSPLIT)
    else:
        ch.send("Automatic gold splitting set.\n\r")
        ch.act = SET_BIT(ch.act,PLR_AUTOSPLIT)

def do_brief(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_BRIEF):
        ch.send("Full descriptions activated.\n\r")
        REMOVE_BIT(ch.comm,COMM_BRIEF)
    else:
        ch.send("Short descriptions activated.\n\r")
        ch.comm = SET_BIT(ch.comm,COMM_BRIEF)

def do_compact(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_COMPACT):
        ch.send("Compact mode removed.\n\r")
        REMOVE_BIT(ch.comm,COMM_COMPACT)
    else:
        ch.send("Compact mode set.\n\r")
        ch.comm = SET_BIT(ch.comm,COMM_COMPACT)

def do_show(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_SHOW_AFFECTS):
        ch.send("Affects will no longer be shown in score.\n\r")
        REMOVE_BIT(ch.comm,COMM_SHOW_AFFECTS)
    else:
        ch.send("Affects will now be shown in score.\n\r")
        ch.comm = SET_BIT(ch.comm,COMM_SHOW_AFFECTS)

def do_prompt(self, argument):
    ch=self
  
    if not argument:
        if IS_SET(ch.comm, COMM_PROMPT):
            ch.send("You will no longer see prompts.\n\r")
            REMOVE_BIT(ch.comm,COMM_PROMPT)
        else:
            ch.send("You will now see prompts.\n\r")
            ch.comm = SET_BIT(ch.comm,COMM_PROMPT)
        return
    if argument.lower() == "all":
        buf = "<%hhp %mm %vmv> "
    else:
        if len(argument) > 50:
            argument = argument[:50]
        buf = argument
        if buf.endswith("%c"):
            buf += " "
  
    ch.prompt = buf
    ch.send("Prompt set to %s\n\r" % ch.prompt)
    return

def do_combine(self, argument):
    ch=self
    if IS_SET(ch.comm, COMM_COMBINE):
        ch.send("Long inventory selected.\n\r")
        REMOVE_BIT(ch.comm,COMM_COMBINE)
    else:
        ch.send("Combined inventory selected.\n\r")
        ch.comm = SET_BIT(ch.comm,COMM_COMBINE)

def do_noloot(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_CANLOOT):
        ch.send("Your corpse is now safe from thieves.\n\r")
        REMOVE_BIT(ch.act,PLR_CANLOOT)
    else:
        ch.send("Your corpse may now be looted.\n\r")
        ch.act = SET_BIT(ch.act,PLR_CANLOOT)

def do_nofollow(self, argument):
    ch=self
    if IS_NPC(ch):
      return
 
    if IS_SET(ch.act, PLR_NOFOLLOW):
        ch.send("You now accept followers.\n\r")
        REMOVE_BIT(ch.act,PLR_NOFOLLOW)
    else:
        ch.send("You no longer accept followers.\n\r")
        ch.act = SET_BIT(ch.act,PLR_NOFOLLOW)
        die_follower(ch)

def do_nosummon(self, argument):
    ch=self
    if IS_NPC(ch):
        if IS_SET(ch.imm_flags, IMM_SUMMON):
            ch.send("You are no longer immune to summon.\n\r")
            REMOVE_BIT(ch.imm_flags,IMM_SUMMON)
        else:
            ch.send("You are now immune to summoning.\n\r")
            ch.imm_flags = SET_BIT(ch.imm_flags,IMM_SUMMON)
    else:
        if IS_SET(ch.act, PLR_NOSUMMON):
            ch.send("You are no longer immune to summon.\n\r")
            REMOVE_BIT(ch.act,PLR_NOSUMMON)
        else:
            ch.send("You are now immune to summoning.\n\r")
            ch.act = SET_BIT(ch.act,PLR_NOSUMMON)

def do_look(self, argument):
    ch = self
    if not ch.desc:
        return

    if ch.position < POS_SLEEPING:
        ch.send("You can't see anything but stars!\r\n")
        return

    if ch.position == POS_SLEEPING:
        ch.send("You can't see anything, you're sleeping!\n\r")
        return

    if not check_blind(ch):
        return

    if not IS_NPC(ch) and not IS_SET(ch.act, PLR_HOLYLIGHT) and room_is_dark(ch.in_room):
        ch.send("It is pitch black ... \n\r")
        show_char_to_char(ch.in_room.people, ch)
        return

    argument, arg1 = read_word(argument)
    argument, arg2 = read_word(argument)
    
    number, arg3 = number_argument(arg1)
    count = 0

    if not arg1 or arg1 == "auto":
        # 'look' or 'look auto' */
        ch.send(ch.in_room.name)

        if IS_IMMORTAL(ch) and (IS_NPC(ch) or IS_SET(ch.act,PLR_HOLYLIGHT)):
            ch.send(" [Room %d]" % ch.in_room.vnum)

        ch.send("\r\n")

        if not arg1 or (not IS_NPC(ch) and not IS_SET(ch.comm, COMM_BRIEF)):
            ch.send("  %s" % ch.in_room.description)
    

        if not IS_NPC(ch) and IS_SET(ch.act, PLR_AUTOEXIT):
            ch.send("\r\n")
            ch.do_exits("auto")


        show_list_to_char(ch.in_room.contents, ch, False, False)
        show_char_to_char(ch.in_room.people,   ch)
        return

    if arg1 == "i" or arg1 == "in" or arg1 == "on":
        # 'look in' */
        if not arg2:
            ch.send("Look in what?\n\r")
            return
    
        obj = get_obj_here(ch, arg2)
        if not obj:
            ch.send("You do not see that here.\n\r")
            return
        
        if item_type == ITEM_DRINK_CON:
            if obj.value[1] <= 0:
                ch.send("It is empty.\r\n")
                return
            if obj.value[1] < obj.value[0] / 4:
                amnt = "less than half-"
            elif obj.value[1] < 3 * obj.value[0] / 4:
                amnt = "abount half-"
            else:
                amnt = "more than half-"
            ch.send("It's %sfilled with a %s liquid.\n\r" % (amnt, liq_table[obj.value[2]].liq_color))
        elif item_type == ITEM_CONTAINER or item_type == ITEM_CORPSE_NPC or item_type == ITEM_CORPSE_PC:
            if IS_SET(obj.value[1], CONT_CLOSED):
                ch.send("It is closed.\n\r")
                return
            act("$p holds:", ch, obj, None, TO_CHAR)
            show_list_to_char(obj.contains, ch, True, True)
            return
        else:
            ch.send("That is not a container.\r\n")
            return
    victim = get_char_room(ch, arg1)
    if victim:
        show_char_to_char_1(victim, ch)
        return
    obj_list = ch.carrying
    obj_list.extend(ch.in_room.contents)
    for obj in obj_list:
        if can_see_obj(ch, obj):
            #player can see object */
            pdesc = get_extra_descr(arg3, obj.extra_descr)

            if pdesc:
                count += 1
                if count == number:
                    ch.send(pdesc)
                    return
            else: continue
        
            pdesc = get_extra_descr(arg3, obj.pIndexData.extra_descr)
            if pdesc:
                count += 1
                if count == number:
                    ch.send(pdesc)
                    return
            else: continue
        
            if arg3.lower() in obj.name.lower:
                count += 1
                if count == number:
                    ch.send("%s\r\n" % obj.description)
                    return
 

    pdesc = get_extra_descr(arg3,ch.in_room.extra_descr)
    if pdesc:
        count += 1
        if count == number:
            ch.send(pdesc)
            return
    
    if count > 0 and count != number:
        if count == 1:
            ch.send("You only see one %s here.\n\r" % arg3)
        else:
            ch.send("You only see %d of those here.\n\r" % count)
        return

    if "north".startswith(arg1): door = 0
    elif "east".startswith(arg1): door = 1
    elif "south".startswith(arg1): door = 2
    elif "west".startswith(arg1): door = 3
    elif "up".startswith(arg1): door = 4
    elif "down".startswith(arg1): door = 5
    else:
        ch.send("You do not see that here.\n\r")
        return
    

    # 'look direction' */
    if door not in ch.in_room.exit or not ch.in_room.exit[door]:
        ch.send("Nothing special there.\n\r")
        return
    pexit = ch.in_room.exit[door]

    if pexit.description:
        ch.send(pexit.description)
    else:
        ch.send("Nothing special there.\n\r")

    if pexit.keyword and pexit.keyword.strip():
        if IS_SET(pexit.exit_info, EX_CLOSED):
            act("The $d is closed.", ch, None, pexit.keyword, TO_CHAR)
        elif IS_SET(pexit.exit_info, EX_ISDOOR):
            act("The $d is open.",   ch, None, pexit.keyword, TO_CHAR)
    return

# RT added back for the hell of it */
def do_read(self, argument):
    ch=self
    ch.do_look(argument)

def do_examine(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Examine what?\n\r")
        return
    ch.do_look(arg)
    buf = ""
    obj = get_obj_here(ch, arg)
    if obj:
        if obj.item_type == ITEM_JUKEBOX:
            ch.do_play("list")
        elif obj.item_type == ITEM_MONEY:
            if obj.value[0] == 0:
                if obj.value[1] == 0:
                    buf = "Odd...there's no coins in the pile.\n\r"
                elif obj.value[1] == 1:
                    buf = "Wow. One gold coin.\n\r"
                else:
                    buf = "There are %d gold coins in the pile.\n\r" % obj.value[1]
            elif obj.value[1] == 0:
                if obj.value[0] == 1:
                    buf = "Wow. One silver coin.\n\r"
                else:
                    buf = "There are %d silver coins in the pile.\n\r" % obj.value[0]
            else:
                buf = "There are %d gold and %d silver coins in the pile.\n\r" % (obj.value[1],obj.value[0])
            ch.send(buf)
        elif obj.item_type == ITEM_DRINK_CON \
          or obj.item_type == ITEM_CONTAINER \
          or obj.item_type == ITEM_CORPSE_NPC \
          or obj.item_type == ITEM_CORPSE_PC:
              ch.do_look("in %s" % argument)

# * Thanks to Zrin for auto-exit part.
def do_exits(self, argument):
    ch=self
    fAuto  = argument == "auto"
    buf = ''
    if not check_blind(ch):
        return
    if fAuto:
        buf += "[Exits:"
    elif IS_IMMORTAL(ch):
        buf += "Obvious exits from room %d:\n\r" % ch.in_room.vnum
    else:
        buf += "Obvious exits:\n\r"

    found = False
    for door, pexit in enumerate(ch.in_room.exit):
        if pexit and pexit.to_room and can_see_room(ch,pexit.to_room) and not IS_SET(pexit.exit_info, EX_CLOSED):
            found = True
            if fAuto:
                buf += " %s" % dir_name[door]
            else:
                buf += "%-5s - %s" % (dir_name[door].capitalize(), 
                  "Too dark to tell" if room_is_dark(pexit.to_room) else pexit.to_room.name)
                if IS_IMMORTAL(ch): buf += " (room %d)\n\r" % pexit.to_room.vnum
                else: buf += "\n\r"
    if not found:
        buf += " none" if fAuto else "None.\n\r"

    if fAuto:
        buf += "]\n\r"
    ch.send(buf)
    return

def do_worth(self, argument):
    ch=self
    if IS_NPC(ch):
        ch.send("You have %ld gold and %ld silver.\n\r" % (ch.gold,ch.silver))
        ch.send(buf)
        return
    ch.send("You have %ld gold, %ld silver, and %d experience (%d exp to level).\n\r" % (
        ch.gold, ch.silver,ch.exp, (ch.level + 1) * exp_per_level(ch,ch.pcdata.points) - ch.exp))

def do_score(self, argument):
    ch=self
    ch.send("You are %s%s, level %d, %d years old (%d hours).\n\r" % (ch.name, "" if IS_NPC(ch) else ch.pcdata.title,
            ch.level, get_age(ch), (ch.played + (int) (current_time - ch.logon)) / 3600))

    if get_trust(ch) != ch.level:
        ch.send("You are trusted at level %d.\n\r" % get_trust(ch))
    ch.send("Race: %s  Sex: %s  Class: %s\n\r" % (ch.race.name, "sexless" if ch.sex == 0 else "male" if ch.sex == 1 else "female",
              "mobile" if IS_NPC(ch) else ch.guild.name))
    ch.send("You have %d/%d hit, %d/%d mana, %d/%d movement.\n\r" % (ch.hit,  ch.max_hit,
              ch.mana, ch.max_mana, ch.move, ch.max_move))
    ch.send("You have %d practices and %d training sessions.\n\r" % (ch.practice, ch.train))
    ch.send("You are carrying %d/%d items with weight %ld/%d pounds.\n\r" % (ch.carry_number, can_carry_n(ch),
              get_carry_weight(ch) / 10, can_carry_w(ch) /10))
    ch.send("Str: %d(%d)  Int: %d(%d)  Wis: %d(%d)  Dex: %d(%d)  Con: %d(%d)\n\r" % (
              ch.perm_stat[STAT_STR], get_curr_stat(ch,STAT_STR),
              ch.perm_stat[STAT_INT], get_curr_stat(ch,STAT_INT),
              ch.perm_stat[STAT_WIS], get_curr_stat(ch,STAT_WIS),
              ch.perm_stat[STAT_DEX], get_curr_stat(ch,STAT_DEX),
              ch.perm_stat[STAT_CON], get_curr_stat(ch,STAT_CON)))

    ch.send("You have scored %d exp, and have %ld gold and %ld silver coins.\n\r" %(ch.exp,  ch.gold, ch.silver))
    # RT shows exp to level */
    if not IS_NPC(ch) and ch.level < LEVEL_HERO:
        ch.send("You need %d exp to level.\n\r" % ((ch.level + 1) * exp_per_level(ch,ch.pcdata.points) - ch.exp))
    ch.send("Wimpy set to %d hit points.\n\r" % ch.wimpy)
    if not IS_NPC(ch) and ch.pcdata.condition[COND_DRUNK]   > 10:
        ch.send("You are drunk.\n\r")
    if not IS_NPC(ch) and ch.pcdata.condition[COND_THIRST] ==  0:
        ch.send("You are thirsty.\n\r")   
    if not IS_NPC(ch) and ch.pcdata.condition[COND_HUNGER]   ==  0:
      ch.send("You are hungry.\n\r")

    if ch.position == POS_DEAD: ch.send("You are DEAD!!\n\r")
    elif ch.position == POS_MORTAL: ch.send("You are mortally wounded.\n\r")
    elif ch.position == POS_INCAP: ch.send("You are incapacitated.\n\r")
    elif ch.position == POS_STUNNED: ch.send("You are stunned.\n\r")
    elif ch.position == POS_SLEEPING: ch.send("You are sleeping.\n\r")
    elif ch.position == POS_RESTING: ch.send("You are resting.\n\r")
    elif ch.position == POS_SITTING: ch.send("You are sitting.\n\r")
    elif ch.position == POS_STANDING: ch.send("You are standing.\n\r")
    elif ch.position == POS_FIGHTING: ch.send("You are fighting.\n\r")
    # print AC values */
    if ch.level >= 25:
        ch.send("Armor: pierce: %d  bash: %d  slash: %d  magic: %d\n\r" % (
                  GET_AC(ch,AC_PIERCE),
                  GET_AC(ch,AC_BASH),
                  GET_AC(ch,AC_SLASH),
                  GET_AC(ch,AC_EXOTIC)))
    for i in range(4):
        temp = ''
        if i == AC_PIERCE: temp = "piercing"
        elif i == AC_BASH: temp = "bashing"
        elif i == AC_SLASH: temp = "slashing"
        elif i == AC_EXOTIC: temp = "magic"
        else: temp = "error"
        ch.send("You are ")

        if GET_AC(ch,i) >=  101: ch.send("hopelessly vulnerable to %s.\n\r" % temp)
        elif GET_AC(ch,i) >= 80: ch.send("defenseless against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= 60: ch.send("barely protected from %s.\n\r" % temp)
        elif GET_AC(ch,i) >= 40: ch.send("slightly armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= 20: ch.send("somewhat armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= 0: ch.send("armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= -20: ch.send("well-armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= -40: ch.send("very well-armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= -60: ch.send("heavily armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= -80: ch.send("superbly armored against %s.\n\r" % temp)
        elif GET_AC(ch,i) >= -100: ch.send("almost invulnerable to %s.\n\r" % temp)
        else: ch.send("divinely armored against %s.\n\r" % temp)

    # RT wizinvis and holy light */
    if IS_IMMORTAL(ch):
        ch.send("Holy Light: ")
        if IS_SET(ch.act, PLR_HOLYLIGHT):
            ch.send("on")
        else:
            ch.send("off")
 
        if ch.invis_level:
            ch.send("  Invisible: level %d" % ch.invis_level)
        if ch.incog_level:
            ch.send("  Incognito: level %d" % ch.incog_level)
        ch.send("\n\r")
    
    if ch.level >= 15:
        ch.send("Hitroll: %d  Damroll: %d.\n\r" % (GET_HITROLL(ch), GET_DAMROLL(ch)))
    if ch.level >= 10:
        ch.send("Alignment: %d.  " % ch.alignment)
    ch.send("You are ")
    if ch.alignment >  900: ch.send("angelic.\n\r")
    elif ch.alignment >  700: ch.send("saintly.\n\r")
    elif ch.alignment >  350: ch.send("good.\n\r")
    elif ch.alignment >  100: ch.send("kind.\n\r")
    elif ch.alignment > -100: ch.send("neutral.\n\r")
    elif ch.alignment > -350: ch.send("mean.\n\r")
    elif ch.alignment > -700: ch.send("evil.\n\r")
    elif ch.alignment > -900: ch.send("demonic.\n\r")
    else: ch.send("satanic.\n\r")

    if IS_SET(ch.comm, COMM_SHOW_AFFECTS):
        ch.do_affects("")

def do_affects(self, argument):
    ch=self
    paf_last = None
    if ch.affected:
        ch.send("You are affected by the following spells:\n\r")
        for paf in ch.affected:
            if paf_last and paf.type == paf_last.type:
                if ch.level >= 20:
                    ch.send("                      ")
                else:
                    continue
            else:
                ch.send("Spell: %-15s" % paf.type.name)
            if ch.level >= 20:
                ch.send(": modifies %s by %d " % (affect_loc_name(paf.location), paf.modifier))
            if paf.duration == -1:
                ch.send("permanently")
            else:
                ch.send("for %d hours" % paf.duration)
            ch.send("\n\r")
            paf_last = paf
    else: 
        ch.send("You are not affected by any spells.\n\r")

day_name = [ "the Moon", "the Bull", "Deception", "Thunder", "Freedom",
    "the Great Gods", "the Sun" ]
month_name = [ "Winter", "the Winter Wolf", "the Frost Giant", "the Old Forces",
    "the Grand Struggle", "the Spring", "Nature", "Futility", "the Dragon",
    "the Sun", "the Heat", "the Battle", "the Dark Shades", "the Shadows",
    "the Long Shadows", "the Ancient Darkness", "the Great Evil" ]

def do_time(self, argument):
    ch=self
    day = time_info.day + 1
    suf = ''
    if day > 4 and day <  20: suf = "th"
    elif day % 10 == 1: suf = "st"
    elif day % 10 == 2: suf = "nd"
    elif day % 10 == 3: suf = "rd"
    else: suf = "th"
    ch.send("It is %d o'clock %s, Day of %s, %d%s the Month of %s.\n\r" % (
        12 if (time_info.hour % 12 == 0) else time_info.hour % 12,
        "pm" if time_info.hour >= 12 else "am",
        day_name[day % 7], day, suf, month_name[time_info.month]))
    #ch.send("ROM started up at %s\n\rThe system time is %s.\n\r", str_boot_time, (char *) ctime(&current_time)
    ch.send(buf)
    return

def do_weather(self, argument):
    ch=self
    sky_look = ["cloudless","cloudy","rainy","lit by flashes of lightning"]
    if not IS_OUTSIDE(ch):
        ch.send("You can't see the weather indoors.\n\r")
        return

    ch.send("The sky is %s and %s.\n\r" % (sky_look[weather_info.sky], 
        "a warm southerly breeze blows" if weather_info.change >= 0 else "a cold northern gust blows"))
    return

def do_help(self, argument):
    ch = self
    if not argument:
        argument = "summary"

    found = [h for h in help_list if h.level <= get_trust(self) and argument.lower() in h.keyword.lower()]

    for pHelp in found:
        if ch.desc.connected == con_playing:
            self.send("\n\r============================================================\n\r")
            ch.send(pHelp.keyword)
            ch.send("\r\n")
        text = pHelp.text
        if pHelp.text[0] == '.':
            text = pHelp.text[1:]
        ch.send(text + "\r\n")
        # small hack :) */
        if ch.desc and ch.desc.connected != con_playing and ch.desc.connected != con_gen_groups:
            break

    if not found:
        self.send("No help on that word.\n\r")


# whois command */
def do_whois(self, argument):
    ch=self
    found = False

    argument, arg = read_word(argument)
  
    if not arg:
        ch.send("You must provide a name.\n\r")
        return
    for d in descriptor_list[:]:
        if d.connected != con_playing or not can_see(ch,d.character):
            continue
        wch = CH(d)
        if not can_see(ch,wch):
            continue
        if arg.startswith(wch.name.lower()):
            found = True
        # work out the printing */
            guild = wch.guild.who_name
            if wch.level == MAX_LEVEL - 0: guild = "IMP"
            elif wch.level == MAX_LEVEL - 1: guild = "CRE"
            elif wch.level == MAX_LEVEL - 2 : guild = "SUP"
            elif wch.level == MAX_LEVEL - 3 : guild = "DEI"
            elif wch.level == MAX_LEVEL - 4 : guild = "GOD"
            elif wch.level == MAX_LEVEL - 5 : guild = "IMM"
            elif wch.level == MAX_LEVEL - 6 : guild = "DEM"
            elif wch.level == MAX_LEVEL - 7 : guild = "ANG"
            elif wch.level == MAX_LEVEL - 8 : guild = "AVA"
            # a little formatting */
            ch.send("[%2d %6s %s] %s%s%s%s%s%s%s%s\n\r" % (
                    wch.level,
                    pc_race_table[wch.race.name].who_name if wch.race.name in pc_race_table else "     ",
                    guild,
                    "(Incog) " if wch.incog_level >= LEVEL_HERO else "",
                    "(Wizi) " if wch.invis_level >= LEVEL_HERO else "",
                    wch.clan.who_name,
                    "[AFK] " if IS_SET(wch.comm, COMM_AFK) else "",
                    "(KILLER) " if IS_SET(wch.act,PLR_KILLER) else "",
                    "(THIEF) " if IS_SET(wch.act,PLR_THIEF) else "",
                    wch.name, 
                    "" if IS_NPC(wch) else wch.pcdata.title))

    if found:
        ch.send("No one of that name is playing.\n\r")
        return
#
# * New 'who' command originally by Alander of Rivers of Mud.
def do_who(self, argument):
    ch=self

    fClassRestrict = False
    fClanRestrict = False
    fClan = False
    fRaceRestrict = False
    fImmortalOnly = False
     #* Set default arguments.
    iLevelLower = 0
    iLevelUpper = MAX_LEVEL
    rgfClass = {k:False for k,g in guild_table.iteritems()}
    rgfRace = {k:False for k,r in pc_race_table.iteritems()}
    rgfClan= {k:False for k,r in clan_table.iteritems()}
 
     #* Parse arguments.
    nNumber = 0
    while True:
        argument, arg  = read_word(argument)
        if not arg:
            break
        if arg.is_digit():
            nNumber +=1
            if nNumber == 1: iLevelLower = int(arg)
            elif nNumber == 2: iLevelUpper = int(arg)
            else:
                ch.send("Only two level numbers allowed.\n\r")
                return
        else:
            # Look for classes to turn on.
            if "immortals".startswith(arg):
                fImmortalOnly = True
            else:
                if arg not in guild_table:
                    if arg not in pc_race_table:
                        if "clan".startswith(arg):
                            fClan = True
                        else:
                            if arg in clan_table:
                                fClanRestrict = True
                                rgfClan[arg] = clan_table[arg]
                            else:
                                ch.send("That's not a valid race, class, or clan.\n\r")
                                return
                    else:
                        fRaceRestrict = True
                        rgfRace[arg] = pc_race_table[arg]
                else:
                    fClassRestrict = True
                    rgfClass[arg] = guild_table[arg]
 
    # Now show matching chars.
    nMatch = 0
    for d in descriptor_list:
        #* Check for match against restrictions.
        #* Don't use trust as that exposes trusted mortals.
        if d.connected != con_playing or not can_see(ch, d.character):
            continue
 
        wch   = CH(d)

        if not can_see(ch,wch):
            continue

        if wch.level < iLevelLower or wch.level > iLevelUpper \
        or (fImmortalOnly  and wch.level < LEVEL_IMMORTAL) \
        or (fClassRestrict and not rgfClass[wch.guild.name]) \
        or (fRaceRestrict and not rgfRace[wch.race.name]) \
        or (fClan and not is_clan(wch)) or (fClanRestrict and not rgfClan[wch.clan.name]):
            continue
 
        nMatch += 1
 
        #
        # Figure out what to print for class.
        guild = wch.guild.who_name
        if wch.level == MAX_LEVEL - 0: guild = "IMP"
        elif wch.level == MAX_LEVEL - 1: guild = "CRE"
        elif wch.level == MAX_LEVEL - 2 : guild = "SUP"
        elif wch.level == MAX_LEVEL - 3 : guild = "DEI"
        elif wch.level == MAX_LEVEL - 4 : guild = "GOD"
        elif wch.level == MAX_LEVEL - 5 : guild = "IMM"
        elif wch.level == MAX_LEVEL - 6 : guild = "DEM"
        elif wch.level == MAX_LEVEL - 7 : guild = "ANG"
        elif wch.level == MAX_LEVEL - 8 : guild = "AVA"
        # a little formatting */
        ch.send("[%2d %6s %s] %s%s%s%s%s%s%s%s\n\r" % (
                wch.level,
                pc_race_table[wch.race.name].who_name if wch.race.name in pc_race_table else "     ",
                guild,
                "(Incog) " if wch.incog_level >= LEVEL_HERO else "",
                "(Wizi) " if wch.invis_level >= LEVEL_HERO else "",
                wch.clan.who_name,
                "[AFK] " if IS_SET(wch.comm, COMM_AFK) else "",
                "(KILLER) " if IS_SET(wch.act,PLR_KILLER) else "",
                "(THIEF) " if IS_SET(wch.act,PLR_THIEF) else "",
                wch.name, 
                "" if IS_NPC(wch) else wch.pcdata.title))
    ch.send("\n\rPlayers found: %d\n\r" % nMatch)
    return

def do_count(self, argument):
    ch=self
    count = len([d for d in descriptor_list if d.connected == con_playing and can_see(ch, CH(d))])
    max_on = max(count,max_on)

    if max_on == count:
        ch.send("There are %d characters on, the most so far today.\n\r" % count)
    else:
        ch.send("There are %d characters on, the most on today was %d.\n\r" % (count,max_on))

def do_inventory(self, argument):
    ch=self
    ch.send("You are carrying:\n\r")
    show_list_to_char(ch.carrying, ch, True, True)
    return

def do_equipment(self, argument):
    ch=self
    ch.send("You are using:\n\r")
    found = False
    for iWear in range(MAX_WEAR):
        obj = get_eq_char(ch, iWear)
        if not obj:
            continue

        ch.send(where_name[iWear])
        if can_see_obj(ch, obj):
            ch.send(format_obj_to_char(obj, ch, True))
            ch.send("\n\r")
        else:
            ch.send("something.\n\r")
        found = True
    if not found:
        ch.send("Nothing.\n\r")

def do_compare(self, argument):
    ch=self
    argument, arg1  = read_word(argument)
    argument, arg2  = read_word(argument)

    if not arg1:
        ch.send("Compare what to what?\n\r")
        return
    obj1 = get_obj_carry(ch, arg1, ch)        
    if not obj1:
        ch.send("You do not have that item.\n\r")
        return
    obj2 = None
    if not arg2:
        for obj2 in ch.carrying:
            if obj2.wear_loc != WEAR_NONE and  can_see_obj(ch,obj2) and  obj1.item_type == obj2.item_type \
            and (obj1.wear_flags & obj2.wear_flags & ~ITEM_TAKE) != 0:
                break

        if not obj2:
            ch.send("You aren't wearing anything comparable.\n\r")
            return
    else:
        obj2 = get_obj_carry(ch,arg2,ch)
        if not obj2:
            ch.send("You do not have that item.\n\r")
            return
    
    msg   = None
    value1  = 0
    value2  = 0

    if obj1 is obj2:
        msg = "You compare $p to itself.  It looks about the same."
    elif obj1.item_type != obj2.item_type:
        msg = "You can't compare $p and $P."
    else:
        if obj1.item_type == ITEM_ARMOR:
            value1 = obj1.value[0] + obj1.value[1] + obj1.value[2]
            value2 = obj2.value[0] + obj2.value[1] + obj2.value[2]
        elif obj1.item_type == ITEM_WEAPON:
            if obj1.pIndexData.new_format:
                value1 = (1 + obj1.value[2]) * obj1.value[1]
            else:
                value1 = obj1.value[1] + obj1.value[2]
            if obj2.pIndexData.new_format:
                value2 = (1 + obj2.value[2]) * obj2.value[1]
            else:
                value2 = obj2.value[1] + obj2.value[2]
        else: msg = "You can't compare $p and $P."
    if msg == None:
        if value1 == value2: msg = "$p and $P look about the same."
        elif value1 > value2: msg = "$p looks better than $P."
        else: msg = "$p looks worse than $P."
    act(msg, ch, obj1, obj2, TO_CHAR)
    return

def do_credits(self, argument):
    ch=self
    ch.do_help("diku")
    return

def do_where(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        ch.send("Players near you:\n\r")
        found = False
        for d in descriptor_list:
            victim = CH(d)
            if d.connected == con_playing \
            and victim \
            and not IS_NPC(victim) \
            and victim.in_room \
            and not IS_SET(victim.in_room.room_flags,ROOM_NOWHERE) \
            and (is_room_owner(ch,victim.in_room) or not room_is_private(victim.in_room)) \
            and victim.in_room.area == ch.in_room.area \
            and can_see(ch, victim):
                found = True
                ch.send("%-28s %s\n\r" % (victim.name, victim.in_room.name))
        if not found:
            ch.send("None\n\r")
    
    else:
        found = False
        for victim in char_list[:]:
            if victim.in_room \
            and victim.in_room.area == ch.in_room.area \
            and not IS_AFFECTED(victim, AFF_HIDE) \
            and not IS_AFFECTED(victim, AFF_SNEAK) \
            and can_see(ch, victim) \
            and arg in victim.name.lower():
                found = True
                ch.send("%-28s %s\n\r" % (PERS(victim, ch), victim.in_room.name))
                break
        if not found:
            act("You didn't find any $T.", ch, None, arg, TO_CHAR)
    return
def do_consider(self, argument):
    ch=self
    argument, arg = read_word(argument)

    if not arg:
        ch.send("Consider killing whom?\n\r")
        return
    victim = get_char_room(ch, arg)
    if not victim:
        ch.send("They're not here.\n\r")
        return

    if is_safe(ch,victim):
        ch.send("Don't even think about it.\n\r")
        return
    diff = victim.level - ch.level

    if diff <= -10: msg = "You can kill $N naked and weaponless."
    elif diff <= -5: msg = "$N is no match for you."
    elif diff <= -2: msg = "$N looks like an easy kill."
    elif diff <= 1: msg = "The perfect match!"
    elif diff <= 4: msg = "$N says 'Do you feel lucky, punk?'."
    elif diff <= 9: msg = "$N laughs at you mercilessly."
    else: msg = "Death will thank you for your gift."
    act(msg, ch, None, victim, TO_CHAR)
    return

def set_title(ch, title):
    if IS_NPC(ch):
        print "BUG: Set_title: NPC."
        return
    buf = ''
    if title[0] != '.' and title[0] != ',' and title[0] != '!' and title[0] != '?':
        buf += ' ' + title
    else:
        buf = title
    ch.pcdata.title = buf

def do_title(self, argument):
    ch=self
    if IS_NPC(ch):
        return

    if not argument:
        ch.send("Change your title to what?\n\r")
        return

    if len(argument) > 45:
        argument = argument[:45]

    set_title(ch, argument)
    ch.send("Ok.\n\r")

def do_description(self, argument):
    ch=self

    if not argument:
        if argument[0] == '-':
            if not ch.description:
                ch.send("No lines left to remove.\n\r")
                return
            buf = ch.description.split('\n')
            buf.pop()
            ch.description = '\n'.join(buf)  
            if len(buf) > 1:
                ch.send("Your description is:\n\r")
                ch.send(ch.description if ch.description else "(None).\n\r")
                return
            else:
                ch.description = ""
                ch.send("Description cleared.\n\r")
                return
        if argument[0] == '+':
            argument = argument[1:].lstrip()

            if len(argument) + len(ch.description) >= 1024:
                ch.send("Description too long.\n\r")
                return
            ch.description += argument + "\n"
            
    ch.send("Your description is:\n\r")
    ch.send(ch.description if ch.description else "(None).\n\r")
    return

def do_report(self, argument):
    ch=self
    ch.send("You say 'I have %d/%d hp %d/%d mana %d/%d mv %d xp.'\n\r" %  (
              ch.hit,  ch.max_hit,
              ch.mana, ch.max_mana,
              ch.move, ch.max_move,
              ch.exp  ))
    buf = "$n says 'I have %d/%d hp %d/%d mana %d/%d mv %d xp.'" % (
              ch.hit,  ch.max_hit,
              ch.mana, ch.max_mana,
              ch.move, ch.max_move,
              ch.exp  )
    act(buf, ch, None, None, TO_ROOM)
    return

def do_practice(self, argument):
    ch=self
    if IS_NPC(ch):
        return
    if not argument:
        col = 0
        for sn, skill in skill_table.iteritems():
            if ch.level < skill.skill_level[ch.guild.name] or ch.pcdata.learned[sn] < 1: # skill is not known */)
                continue

            ch.send("%-18s %3d%%  " % (skill.name, ch.pcdata.learned[sn]))
            col += 1
            if col % 3 == 0:
                ch.send("\n\r")
        if col % 3 != 0:
            ch.send("\n\r")

        ch.send("You have %d practice sessions left.\n\r" % ch.practice)
    else:
        if not IS_AWAKE(ch):
           ch.send("In your dreams, or what?\n\r")
           return
        mob = None
        prac_mobs = [ mob for mob in ch.in_room.people if IS_NPC(mob) and IS_SET(mob.act, ACT_PRACTICE) ][:1]
        if not prac_mob:
            ch.send("You can't do that here.\n\r")
            return
        else:
            mob = prac_mobs[0]
        if ch.practice <= 0:
            ch.send("You have no practice sessions left.\n\r")
            return
        skill = prefix_lookup(skill_table, argument)
        if not skill or not IS_NPC(ch) \
        and (ch.level < skill.skill_level[ch.guild.name] or ch.pcdata.learned[sn] < 1 \
        or skill.rating[ch.guild.name] == 0):
            ch.send("You can't practice that.\n\r")
            return
        adept = 100 if IS_NPC(ch) else ch.guild.skill_adept

        if ch.pcdata.learned[skill.name] >= adept:
            ch.send("You are already learned at %s.\n\r" % skill.name)
        else:
            ch.practice -= 1
            ch.pcdata.learned[skill.name] += int_app[get_curr_stat(ch,STAT_INT)].learn / skill.rating[ch.guild.name]
            if ch.pcdata.learned[skill.name] < adept:
                act("You practice $T.", ch, None, skill_table[sn].name, TO_CHAR)
                act("$n practices $T.", ch, None, skill_table[sn].name, TO_ROOM)
            else:
                ch.pcdata.learned[skill.name] = adept
                act("You are now learned at $T.", ch, None, skill.name, TO_CHAR)
                act("$n is now learned at $T.", ch, None, skill.name, TO_ROOM)
    return
# * 'Wimpy' originally by Dionysos.
def do_wimpy(self, argument):
    ch=self
    argument, arg = read_word(argument)
    if not arg:
        wimpy = ch.max_hit / 5
    else:
        wimpy = int(arg)
    if wimpy < 0:
        ch.send("Your courage exceeds your wisdom.\n\r")
        return
    if wimpy > ch.max_hit/2:
        ch.send("Such cowardice ill becomes you.\n\r")
        return
    ch.wimpy = wimpy
    ch.send("Wimpy set to %d hit points.\n\r" % wimpy)
    return

def do_password(self, argument):
    ch=self
    if IS_NPC(ch):
        return

     #* Can't use read_word here because it smashes case.
     #* So we just steal all its code.  Bleagh.
     # -- It actually doesn't now because it loads areas too. Davion.
    argument, arg1 = read_word(argument, False)
    argument, arg2 = read_word(argument, False)

    if not arg1 or not arg2:
        ch.send("Syntax: password <old> <new>.\n\r")
        return

    if ENCRYPT_PASSWORD:
        arg1 = hashlib.sha512(arg1).hexdigest()
        arg2 = hashlib.sha512(arg2).hexdigest()

    if arg1 == ch.pcdata.pwd:
        WAIT_STATE(ch, 40)
        ch.send("Wrong password.  Wait 10 seconds.\n\r")
        return
    if len(arg2) < 5:
        ch.send("New password must be at least five characters long.\n\r")
        return

     #* No tilde allowed because of player file format.
     # Also now not true. Davion
    
    ch.pcdata.pwd = arg2
    save_char_obj(ch)
    ch.send("Ok.\n\r")
    return