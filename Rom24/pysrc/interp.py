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
 * Now using Python 3 version https://code.google.com/p/miniboa-py3/
 ************/
"""
from collections import OrderedDict
from merc import *
from act_info import *
from act_wiz import *
from act_obj import *
from act_enter import *
from act_comm import *
from act_move import *
from alias import *
from healing import do_heal
from magic import do_cast
from fight import *
from skills import do_groups, do_skills, do_spells, do_gain
from settings import LOGALL


class cmd_type:
    def __init__(self, name, do_fun, position, level, log, show):
        self.name=name
        self.do_fun=do_fun
        self.position=position
        self.level=level
        self.log=log
        self.show=show

cmd_table = OrderedDict()

cmd_table['north'] = cmd_type('north', do_north, POS_STANDING, 0, LOG_NEVER, 0)
cmd_table['east'] = cmd_type('east', do_east, POS_STANDING, 0, LOG_NEVER, 0)
cmd_table['south'] = cmd_type('south', do_south, POS_STANDING, 0, LOG_NEVER, 0)
cmd_table['west'] = cmd_type('west', do_west, POS_STANDING, 0, LOG_NEVER, 0)
cmd_table['up'] = cmd_type('up', do_up, POS_STANDING, 0, LOG_NEVER, 0)
cmd_table['down'] = cmd_type('down', do_down, POS_STANDING, 0, LOG_NEVER, 0)
# * Common other commands.
# * Placed here so one and two letter abbreviations work.
cmd_table['at'] = cmd_type('at', do_at, POS_DEAD, L6, LOG_NORMAL, 1)
cmd_table['cast'] = cmd_type('cast', do_cast, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['auction'] = cmd_type('auction', do_auction, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['buy'] = cmd_type('buy', do_buy, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['channels'] = cmd_type('channels', do_channels, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['exits'] = cmd_type('exits', do_exits, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['get'] = cmd_type('get', do_get, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['goto'] = cmd_type('goto', do_goto, POS_DEAD, L8, LOG_NORMAL, 1)
cmd_table['group'] = cmd_type('group', do_group, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['guild'] = cmd_type('guild', do_guild, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['hit'] = cmd_type('hit', do_kill, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['inventory'] = cmd_type('inventory', do_inventory, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['kill'] = cmd_type('kill', do_kill, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['look'] = cmd_type('look', do_look, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['clan'] = cmd_type('clan', do_clantalk, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['music'] = cmd_type('music', do_music, POS_SLEEPING, 0, LOG_NORMAL, 1) 
cmd_table['order'] = cmd_type('order', do_order, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['practice'] = cmd_type('practice', do_practice, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['rest'] = cmd_type('rest', do_rest, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['sit'] = cmd_type('sit', do_sit, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['sockets'] = cmd_type('sockets', do_sockets, POS_DEAD, L4, LOG_NORMAL, 1)
cmd_table['stand'] = cmd_type('stand', do_stand, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['tell'] = cmd_type('tell', do_tell, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['unlock'] = cmd_type('unlock', do_unlock, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['wield'] = cmd_type('wield', do_wear, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['wizhelp'] = cmd_type('wizhelp', do_wizhelp, POS_DEAD, IM, LOG_NORMAL, 1 )
# * Informational commands.
cmd_table['affects'] = cmd_type('affects', do_affects, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['areas'] = cmd_type('areas', do_areas, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['bug'] = cmd_type('bug', do_bug, POS_DEAD, 0, LOG_NORMAL, 1)
#cmd_table['changes'] = cmd_type('changes', do_changes, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['commands'] = cmd_type('commands', do_commands, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['compare'] = cmd_type('compare', do_compare, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['consider'] = cmd_type('consider', do_consider, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['count'] = cmd_type('count', do_count, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['credits'] = cmd_type('credits', do_credits, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['equipment'] = cmd_type('equipment', do_equipment, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['examine'] = cmd_type('examine', do_examine, POS_RESTING, 0, LOG_NORMAL, 1)
# cmd_table['groups'] = cmd_type('groups', do_groups, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['help'] = cmd_type('help', do_help, POS_DEAD, 0, LOG_NORMAL, 1)
#cmd_table['idea'] = cmd_type('idea', do_idea, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['info'] = cmd_type('info', do_groups, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['motd'] = cmd_type('motd', do_motd, POS_DEAD, 0, LOG_NORMAL, 1)
#cmd_table['news'] = cmd_type('news', do_news, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['read'] = cmd_type('read', do_read, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['report'] = cmd_type('report', do_report, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['rules'] = cmd_type('rules', do_rules, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['score'] = cmd_type('score', do_score, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['skills'] = cmd_type('skills', do_skills, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['socials'] = cmd_type('socials', do_socials, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['show'] = cmd_type('show', do_show, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['spells'] = cmd_type('spells', do_spells, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['story'] = cmd_type('story', do_story, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['time'] = cmd_type('time', do_time, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['typo'] = cmd_type('typo', do_typo, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['weather'] = cmd_type('weather', do_weather, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['who'] = cmd_type('who', do_who, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['whois'] = cmd_type('whois', do_whois, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['wizlist'] = cmd_type('wizlist', do_wizlist, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['worth'] = cmd_type('worth', do_worth, POS_SLEEPING, 0, LOG_NORMAL, 1)
# * Configuration commands.
cmd_table['alia'] = cmd_type('alia', do_alia, POS_DEAD, 0, LOG_NORMAL, 0)
cmd_table['alias'] = cmd_type('alias', do_alias, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autolist'] = cmd_type('autolist', do_autolist, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autoassist'] = cmd_type('autoassist', do_autoassist, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autoexit'] = cmd_type('autoexit', do_autoexit, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autogold'] = cmd_type('autogold', do_autogold, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autoloot'] = cmd_type('autoloot', do_autoloot, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autosac'] = cmd_type('autosac', do_autosac, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['autosplit'] = cmd_type('autosplit', do_autosplit, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['brief'] = cmd_type('brief', do_brief, POS_DEAD, 0, LOG_NORMAL, 1)
#cmd_table['channels'] = cmd_type('channels', do_channels, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['combine'] = cmd_type('combine', do_combine, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['compact'] = cmd_type('compact', do_compact, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['description'] = cmd_type('description', do_description, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['delet'] = cmd_type('delet', do_delet, POS_DEAD, 0, LOG_ALWAYS, 0)
cmd_table['delete'] = cmd_type('delete', do_delete, POS_STANDING, 0, LOG_ALWAYS, 1)
cmd_table['nofollow'] = cmd_type('nofollow', do_nofollow, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['noloot'] = cmd_type('noloot', do_noloot, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['nosummon'] = cmd_type('nosummon', do_nosummon, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['outfit'] = cmd_type('outfit', do_outfit, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['password'] = cmd_type('password', do_password, POS_DEAD, 0, LOG_NEVER, 1)
cmd_table['prompt'] = cmd_type('prompt', do_prompt, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['scroll'] = cmd_type('scroll', do_scroll, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['title'] = cmd_type('title', do_title, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['unalias'] = cmd_type('unalias', do_unalias, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['wimpy'] = cmd_type('wimpy', do_wimpy, POS_DEAD, 0, LOG_NORMAL, 1)
# Communication commands.
cmd_table['afk'] = cmd_type('afk', do_afk, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['answer'] = cmd_type('answer', do_answer, POS_SLEEPING, 0, LOG_NORMAL, 1)
# cmd_table['auction'] = cmd_type('auction', do_auction, POS_SLEEPING, 0, LOG_NORMAL, 1) */
cmd_table['deaf'] = cmd_type('deaf', do_deaf, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['emote'] = cmd_type('emote', do_emote, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['pmote'] = cmd_type('pmote', do_pmote, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['.'] = cmd_type('.',  do_gossip,  POS_SLEEPING, 0,  LOG_NORMAL, 0 )
cmd_table['gossip'] = cmd_type('gossip', do_gossip, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table[','] = cmd_type(',', do_emote, POS_RESTING, 0, LOG_NORMAL, 0)
cmd_table['grats'] = cmd_type('grats', do_grats, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['gtell'] = cmd_type('gtell', do_gtell, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table[';'] = cmd_type(';',  do_gtell,   POS_DEAD,    0,  LOG_NORMAL, 0)
#cmd_table['music'] = cmd_type('music', do_music, POS_SLEEPING, 0, LOG_NORMAL, 1) */
#cmd_table['note'] = cmd_type('note', do_note, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['pose'] = cmd_type('pose', do_pose, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['question'] = cmd_type('question', do_question, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['quote'] = cmd_type('quote', do_quote, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['quiet'] = cmd_type('quiet', do_quiet, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['reply'] = cmd_type('reply', do_reply, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['replay'] = cmd_type('replay', do_replay, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['say'] = cmd_type('say', do_say, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table["'"] = cmd_type("'",      do_say,     POS_RESTING,     0,  LOG_NORMAL, 0)
cmd_table['shout'] = cmd_type('shout', do_shout, POS_RESTING, 3, LOG_NORMAL, 1)
#cmd_table['unread'] = cmd_type('unread', do_unread, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['yell'] = cmd_type('yell', do_yell, POS_RESTING, 0, LOG_NORMAL, 1)
# * Object manipulation commands.
cmd_table['brandish'] = cmd_type('brandish', do_brandish, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['close'] = cmd_type('close', do_close, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['drink'] = cmd_type('drink', do_drink, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['drop'] = cmd_type('drop', do_drop, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['eat'] = cmd_type('eat', do_eat, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['envenom'] = cmd_type('envenom', do_envenom, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['fill'] = cmd_type('fill', do_fill, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['give'] = cmd_type('give', do_give, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['heal'] = cmd_type('heal', do_heal, POS_RESTING, 0, LOG_NORMAL, 1) 
cmd_table['hold'] = cmd_type('hold', do_wear, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['list'] = cmd_type('list', do_list, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['lock'] = cmd_type('lock', do_lock, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['open'] = cmd_type('open', do_open, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['pick'] = cmd_type('pick', do_pick, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['pour'] = cmd_type('pour', do_pour, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['put'] = cmd_type('put', do_put, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['quaff'] = cmd_type('quaff', do_quaff, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['recite'] = cmd_type('recite', do_recite, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['remove'] = cmd_type('remove', do_remove, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['sell'] = cmd_type('sell', do_sell, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['take'] = cmd_type('take', do_get, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['sacrifice'] = cmd_type('sacrifice', do_sacrifice, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['junk'] = cmd_type('junk', do_sacrifice, POS_RESTING, 0, LOG_NORMAL, 0)
cmd_table['tap'] = cmd_type('tap', do_sacrifice, POS_RESTING, 0, LOG_NORMAL, 0)   
#cmd_table['unlock'] = cmd_type('unlock', do_unlock, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['value'] = cmd_type('value', do_value, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['wear'] = cmd_type('wear', do_wear, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['zap'] = cmd_type('zap', do_zap, POS_RESTING, 0, LOG_NORMAL, 1)

# * Combat commands.

cmd_table['backstab'] = cmd_type('backstab', do_backstab, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['bash'] = cmd_type('bash', do_bash, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['bs'] = cmd_type('bs', do_backstab, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['berserk'] = cmd_type('berserk', do_berserk, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['dirt'] = cmd_type('dirt', do_dirt, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['disarm'] = cmd_type('disarm', do_disarm, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['flee'] = cmd_type('flee', do_flee, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['kick'] = cmd_type('kick', do_kick, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table['murde'] = cmd_type('murde', do_murde, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['murder'] = cmd_type('murder', do_murder, POS_FIGHTING, 5, LOG_ALWAYS, 1)
cmd_table['rescue'] = cmd_type('rescue', do_rescue, POS_FIGHTING, 0, LOG_NORMAL, 0)
cmd_table['trip'] = cmd_type('trip', do_trip, POS_FIGHTING, 0, LOG_NORMAL, 1)
# * Miscellaneous commands.
cmd_table['enter'] = cmd_type('enter', do_enter, POS_STANDING, 0, LOG_NORMAL, 1)
cmd_table['follow'] = cmd_type('follow', do_follow, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['gain'] = cmd_type('gain', do_gain, POS_STANDING, 0, LOG_NORMAL, 1)
cmd_table['go'] = cmd_type('go', do_enter, POS_STANDING, 0, LOG_NORMAL, 0)
# cmd_table['group'] = cmd_type('group', do_group, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['groups'] = cmd_type('groups', do_groups, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['hide'] = cmd_type('hide', do_hide, POS_RESTING, 0, LOG_NORMAL, 1)
#cmd_table['play'] = cmd_type('play', do_play, POS_RESTING, 0, LOG_NORMAL, 1)
#cmd_table['practice'] = cmd_type('practice', do_practice, POS_SLEEPING, 0, LOG_NORMAL, 1) */
cmd_table['qui'] = cmd_type('qui', do_qui, POS_DEAD, 0, LOG_NORMAL, 0)
cmd_table['quit'] = cmd_type('quit', do_quit, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['recall'] = cmd_type('recall', do_recall, POS_FIGHTING, 0, LOG_NORMAL, 1)
cmd_table["/"] = cmd_type("/", do_recall,  POS_FIGHTING,    0,  LOG_NORMAL, 0)
cmd_table['rent'] = cmd_type('rent', do_rent, POS_DEAD, 0, LOG_NORMAL, 0)
cmd_table['save'] = cmd_type('save', do_save, POS_DEAD, 0, LOG_NORMAL, 1)
cmd_table['sleep'] = cmd_type('sleep', do_sleep, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['sneak'] = cmd_type('sneak', do_sneak, POS_STANDING, 0, LOG_NORMAL, 1)
cmd_table['split'] = cmd_type('split', do_split, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['steal'] = cmd_type('steal', do_steal, POS_STANDING, 0, LOG_NORMAL, 1)
cmd_table['train'] = cmd_type('train', do_train, POS_RESTING, 0, LOG_NORMAL, 1)
cmd_table['visible'] = cmd_type('visible', do_visible, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['wake'] = cmd_type('wake', do_wake, POS_SLEEPING, 0, LOG_NORMAL, 1)
cmd_table['where'] = cmd_type('where', do_where, POS_RESTING, 0, LOG_NORMAL, 1)
#* Immortal commands.
cmd_table['advance'] = cmd_type('advance', do_advance, POS_DEAD,   ML,  LOG_ALWAYS, 1)
cmd_table['dump'] = cmd_type('dump', do_dump,    POS_DEAD,   ML,  LOG_ALWAYS, 0)
cmd_table['trust'] = cmd_type('trust', do_trust,   POS_DEAD,   ML,  LOG_ALWAYS, 1)
cmd_table['violate'] = cmd_type('violate', do_violate, POS_DEAD,   ML,  LOG_ALWAYS, 1)
#cmd_table['allow'] = cmd_type('allow', do_allow, POS_DEAD, L2, LOG_ALWAYS, 1)
#cmd_table['ban'] = cmd_type('ban', do_ban, POS_DEAD, L2, LOG_ALWAYS, 1)
#cmd_table['deny'] = cmd_type('deny', do_deny, POS_DEAD, L1, LOG_ALWAYS, 1)
cmd_table['disconnect'] = cmd_type('disconnect', do_disconnect, POS_DEAD, L3, LOG_ALWAYS, 1)
#cmd_table['flag'] = cmd_type('flag', do_flag, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['freeze'] = cmd_type('freeze', do_freeze, POS_DEAD, L4, LOG_ALWAYS, 1)
#cmd_table['permban'] = cmd_type('permban', do_permban, POS_DEAD, L1, LOG_ALWAYS, 1)
cmd_table['protect'] = cmd_type('protect', do_protect, POS_DEAD, L1, LOG_ALWAYS, 1)
cmd_table['reboo'] = cmd_type('reboo', do_reboo, POS_DEAD, L1, LOG_NORMAL, 0)
cmd_table['reboot'] = cmd_type('reboot', do_reboot, POS_DEAD, L1, LOG_ALWAYS, 1)
cmd_table['set'] = cmd_type('set', do_set, POS_DEAD, L2, LOG_ALWAYS, 1)
cmd_table['mset'] = cmd_type('mset', do_mset, POS_DEAD, L2, LOG_ALWAYS, 1)
cmd_table['sset'] = cmd_type('sset', do_sset, POS_DEAD, L2, LOG_ALWAYS, 1)
cmd_table['oset'] = cmd_type('oset', do_oset, POS_DEAD, L2, LOG_ALWAYS, 1)
cmd_table['shutdow'] = cmd_type('shutdow', do_shutdow, POS_DEAD, L1, LOG_NORMAL, 0)
cmd_table['shutdown'] = cmd_type('shutdown', do_shutdown, POS_DEAD, L1, LOG_ALWAYS, 1)
#cmd_table['sockets'] = cmd_type('sockets', do_sockets, POS_DEAD, L4, LOG_NORMAL, 1) */
cmd_table['wizlock'] = cmd_type('wizlock', do_wizlock, POS_DEAD, L2, LOG_ALWAYS, 1)
cmd_table['force'] = cmd_type('force', do_force, POS_DEAD, L7, LOG_ALWAYS, 1)
cmd_table['load'] = cmd_type('load', do_load, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['mload'] = cmd_type('m load', do_mload, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['oload'] = cmd_type('oload', do_oload, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['newlock'] = cmd_type('newlock', do_newlock, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['nochannels'] = cmd_type('nochannels', do_nochannels, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['noemote'] = cmd_type('noemote', do_noemote, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['noshout'] = cmd_type('noshout', do_noshout, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['notell'] = cmd_type('notell', do_notell, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['pecho'] = cmd_type('pecho', do_pecho, POS_DEAD, L4, LOG_ALWAYS, 1) 
cmd_table['pardon'] = cmd_type('pardon', do_pardon, POS_DEAD, L3, LOG_ALWAYS, 1)
cmd_table['purge'] = cmd_type('purge', do_purge, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['restore'] = cmd_type('restore', do_restore, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['sla'] = cmd_type('sla', do_sla, POS_DEAD, L3, LOG_NORMAL, 0)
cmd_table['slay'] = cmd_type('slay', do_slay, POS_DEAD, L3, LOG_ALWAYS, 1)
cmd_table['teleport'] = cmd_type('teleport', do_transfer, POS_DEAD, L5, LOG_ALWAYS, 1)   
cmd_table['transfer'] = cmd_type('transfer', do_transfer, POS_DEAD, L5, LOG_ALWAYS, 1)
# cmd_table['at'] = cmd_type('at', do_at, POS_DEAD, L6, LOG_NORMAL, 1) */
cmd_table['poofin'] = cmd_type('poofin', do_bamfin, POS_DEAD, L8, LOG_NORMAL, 1)
cmd_table['poofout'] = cmd_type('poofout', do_bamfout, POS_DEAD, L8, LOG_NORMAL, 1)
cmd_table['gecho'] = cmd_type('gecho', do_echo, POS_DEAD, L4, LOG_ALWAYS, 1)
# cmd_table['goto'] = cmd_type('goto', do_goto, POS_DEAD, L8, LOG_NORMAL, 1) */
cmd_table['holylight'] = cmd_type('holylight', do_holylight,   POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['incognito'] = cmd_type('incognito', do_incognito,   POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['invis'] = cmd_type('invis', do_invis,   POS_DEAD,   IM,  LOG_NORMAL, 0)
cmd_table['log'] = cmd_type('log', do_log, POS_DEAD, L1, LOG_ALWAYS, 1)
cmd_table['memory'] = cmd_type('memory', do_memory,  POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['mwhere'] = cmd_type('mwhere', do_mwhere,  POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['owhere'] = cmd_type('owhere', do_owhere,  POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['peace'] = cmd_type('peace', do_peace, POS_DEAD, L5, LOG_NORMAL, 1)
#cmd_table['penalty'] = cmd_type('penalty', do_penalty, POS_DEAD, L7, LOG_NORMAL, 1)
cmd_table['echo'] = cmd_type('echo', do_recho, POS_DEAD, L6, LOG_ALWAYS, 1)
cmd_table['return'] = cmd_type('return', do_return, POS_DEAD, L6, LOG_NORMAL, 1)
cmd_table['snoop'] = cmd_type('snoop', do_snoop, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['stat'] = cmd_type('stat', do_stat,    POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['mstat'] = cmd_type('stat', do_mstat,    POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['ostat'] = cmd_type('stat', do_ostat,    POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['string'] = cmd_type('string', do_string, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['switch'] = cmd_type('switch', do_switch, POS_DEAD, L6, LOG_ALWAYS, 1)
cmd_table['wizinvis'] = cmd_type('wizinvis', do_invis,   POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['vnum'] = cmd_type('vnum', do_vnum, POS_DEAD, L4, LOG_NORMAL, 1)
cmd_table['mfind'] = cmd_type('mfind', do_mfind, POS_DEAD, L4, LOG_NORMAL, 1)
cmd_table['ofind'] = cmd_type('ofind', do_ofind, POS_DEAD, L4, LOG_NORMAL, 1)
cmd_table['zecho'] = cmd_type('zecho', do_zecho, POS_DEAD, L4, LOG_ALWAYS, 1)
cmd_table['clone'] = cmd_type('clone', do_clone, POS_DEAD, L5, LOG_ALWAYS, 1)
cmd_table['wiznet'] = cmd_type('wiznet', do_wiznet,  POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['immtalk'] = cmd_type('immtalk', do_immtalk, POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['imotd'] = cmd_type('imotd', do_imotd,       POS_DEAD,       IM,  LOG_NORMAL, 1)
cmd_table[':'] = cmd_type(':', do_immtalk, POS_DEAD,   IM,  LOG_NORMAL, 0)
cmd_table['smote'] = cmd_type('smote', do_smote,   POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['prefi'] = cmd_type('prefi', do_prefi,   POS_DEAD,   IM,  LOG_NORMAL, 0)
cmd_table['prefix'] = cmd_type('prefix', do_prefix,  POS_DEAD,   IM,  LOG_NORMAL, 1)
cmd_table['reload'] = cmd_type('reload', do_reload,  POS_DEAD,   ML,  LOG_NORMAL, 1)

#A little python vooodoo to make do_functions methods of char_data
for k,cmd in cmd_table.items():
    setattr(CHAR_DATA, cmd.do_fun.__name__, cmd.do_fun )


def interpret(ch, argument):
     # Strip leading spaces.
    argument = argument.lstrip()
    command = ''

    # No hiding.
    REMOVE_BIT(ch.affected_by, AFF_HIDE)

    # * Implement freeze command.
    if not IS_NPC(ch) and IS_SET(ch.act, PLR_FREEZE):
        ch.send("You're totally frozen!\n")
        return
    # * Grab the command word.
    # * Special parsing so ' can be a command,
    # *   also no spaces needed after punctuation.
    logline = argument
    if not argument[0].isalpha() and not argument[0].isdigit():
        command = argument[0]
        argument = argument[:1].lstrip()
    else:
        argument, command = read_word(argument)
    #* Look for command in command table.
    trust = ch.get_trust()
    cmd = prefix_lookup(cmd_table, command)
    if cmd != None:
        if cmd.level > trust:
            cmd = None
 
    #* Log and snoop.
    if (not IS_NPC(ch) and IS_SET(ch.act, PLR_LOG)) or LOGALL or (cmd and cmd.log == LOG_ALWAYS):
        if cmd and cmd.log != LOG_NEVER:
            log_buf = "Log %s: %s" % (ch.name, logline)
            wiznet(log_buf,ch,None,WIZ_SECURE,0,ch.get_trust())
            print (log_buf + "\n")
    if ch.desc and ch.desc.snoop_by:
        ch.desc.snoop_by.send("% ")
        ch.desc.snoop_by.send(logline)
        ch.desc.snoop_by.send("\n")
    if not cmd:
        #* Look for command in socials table.
        if not check_social(ch, command, argument):
            ch.send("Huh?\n")
        return
    #* Character not in position for command?
    if ch.position < cmd.position:
        if ch.position == POS_DEAD:
            ch.send("Lie still; you are DEAD.\n")
        elif ch.position ==  POS_MORTAL \
        or ch.position ==  POS_INCAP:
            ch.send("You are hurt far too bad for that.\n")
        elif ch.position == POS_STUNNED:
            ch.send("You are too stunned to do that.\n")
        elif ch.position == POS_SLEEPING:
            ch.send("In your dreams, or what?\n")
        elif ch.position == POS_RESTING:
            ch.send("Nah... You feel too relaxed...\n")
        elif ch.position == POS_SITTING:
            ch.send("Better stand up first.\n")
        elif ch.position == POS_FIGHTING:
            ch.send("No way!  You are still fighting!\n")
        return

    # Dispatch the command.
    cmd.do_fun(ch, argument)
    return

def check_social(ch, command, argument):
    cmd = None
    for social in social_list:
        if social.name.lower().startswith(command):
            cmd = social
    if not cmd:
        return False
    if not IS_NPC(ch) and IS_SET(ch.comm, COMM_NOEMOTE):
        ch.send("You are anti-social!\n")
        return True
    
    if ch.position == POS_DEAD:
        ch.send("Lie still; you are DEAD.\n")
        return True
    if ch.position == POS_INCAP or ch.position == POS_MORTAL:
        ch.send("You are hurt far too bad for that.\n")
        return True
    if ch.position == POS_STUNNED:
        ch.send("You are too stunned to do that.\n")
        return True
    if ch.position == POS_SLEEPING:
        #* I just know this is the path to a 12" 'if' statement.  :(
        #* But two players asked for it already!  -- Furey
            if cmd.name != "snore":
                ch.send("In your dreams, or what?\n")
                return True
    holder, arg = read_word(argument)
    victim = ch.get_char_room(arg)
    if not arg:
        act(cmd.others_no_arg, ch, None, victim, TO_ROOM)
        act(cmd.char_no_arg, ch, None, victim, TO_CHAR)
    elif not victim:
        ch.send("They aren't here.\n")
    elif victim == ch:
        act(cmd.others_auto, ch, None, victim, TO_ROOM)
        act(cmd.char_auto, ch, None, victim, TO_CHAR)
    else:
        act(cmd.others_found, ch, None, victim, TO_NOTVICT)
        act(cmd.char_found, ch, None, victim, TO_CHAR)
        act(cmd.vict_found, ch, None, victim, TO_VICT)

        if not IS_NPC(ch) and IS_NPC(victim) \
        and not IS_AFFECTED(victim, AFF_CHARM) \
        and IS_AWAKE(victim) and victim.desc == None:
            num = random.randit(0,12)
            if num in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                act(cmd.others_found, victim, None, ch, TO_NOTVICT)
                act(cmd.char_found, victim, None, ch, TO_CHAR)
                act(cmd.vict_found, victim, None, ch, TO_VICT)
                
            elif num in [9, 10, 11, 12]:
                act("$n slaps $N.", victim, None, ch, TO_NOTVICT)
                act("You slap $N.", victim, None, ch, TO_CHAR)
                act("$n slaps you.", victim, None, ch, TO_VICT)
    return True;



