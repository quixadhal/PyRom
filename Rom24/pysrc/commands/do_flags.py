import game_utils
import merc

__author__ = 'venom'

#int flag_lookup args( ( const char *name, const struct flag_type *flag_table) );


def do_flag(ch, argument):
    action_type = ''
    if '+' in argument:
        action_type = 'add'
    elif '-' in argument:
        action_type = 'rem'
    elif '=' in argument:
        action_type = 'equals'

    victim = None
    
    argument, arg1 = game_utils.read_word(argument)
    argument, arg2 = game_utils.read_word(argument)
    argument, arg3 = game_utils.read_word(argument)
    argument, arg4 = game_utils.read_word(argument)
    
    if not arg1 or arg2 or arg3:
        ch.send("Syntax:\n")
        ch.send("  flag mob  <name> <field> <flags>\n")
        ch.send("  flag char <name> <field> <flags>\n")
        ch.send("  mob  flags: act,aff,off,imm,res,vuln,form,part\n")
        ch.send("  char flags: plr,comm,aff,imm,res,vuln,\n")
        ch.send("  +: add flag, -: remove flag, = set equal to\n")
        ch.send("  otherwise flag toggles the flags listed.\n")
        return

    if not arg2:
        ch.send("What do you wish to set flags on?\n")
        return

    if not arg3:
        ch.send("You need to specify a flag to set.\n")
        return

    if not arg4:
        ch.send("Which flags do you wish to change?\n")
        return

    if arg1 in ('mob', 'npc', 'character', 'char'):
        victim = ch.get_char_world(arg2)

    else:
        ch.send('You cannot find them')
        return

    if arg3.startswith('act'):
        if not victim.is_npc():
            ch.send("Use plr for PCs.\n")
            return


	    flag = &victim->act
	    flag_table = act_flags
	

	else if (!str_prefix(arg3,"plr"))
	
	    if (IS_NPC(victim))
	    
		ch.send("Use act for NPCs.\n")
		return
	    

	    flag = &victim->act
	    flag_table = plr_flags
	

 	else if (!str_prefix(arg3,"aff"))
	
	    flag = &victim->affected_by
	    flag_table = affect_flags
	

  	else if (!str_prefix(arg3,"immunity"))
	
	    flag = &victim->imm_flags
	    flag_table = imm_flags
	

	else if (!str_prefix(arg3,"resist"))
	
	    flag = &victim->res_flags
	    flag_table = imm_flags
	

	else if (!str_prefix(arg3,"vuln"))
	
	    flag = &victim->vuln_flags
	    flag_table = imm_flags
	

	else if (!str_prefix(arg3,"form"))
	
	    if (!IS_NPC(victim))
	    
	 	ch.send("Form can't be set on PCs.\n")
		return
	    

	    flag = &victim->form
	    flag_table = form_flags
	

	else if (!str_prefix(arg3,"parts"))
	
	    if (!IS_NPC(victim))
	    
		ch.send("Parts can't be set on PCs.\n")
		return
	    

	    flag = &victim->parts
	    flag_table = part_flags
	

	else if (!str_prefix(arg3,"comm"))
	
	    if (IS_NPC(victim))
	    
		ch.send("Comm can't be set on NPCs.\n")
		return
	    

	    flag = &victim->comm
	    flag_table = comm_flags
	

	else
	
	    ch.send("That's not an acceptable flag.\n")
	    return
	

	old = *flag
	victim->zone = NULL

	if (type != '=')
	    new = old

        /* mark the words */
        for ( )
        
	    argument = one_argument(argument,word)

	    if (word[0] == '\0')
		break

	    pos = flag_lookup(word,flag_table)
	    if (pos == 0)
            
	    
		ch.send("That flag doesn't exist!\n")
		return
	    
	    else
		SET_BIT(marked,pos)
	

	for (pos = 0 flag_table[pos].name != NULL pos++)
	
	    if (!flag_table[pos].settable && IS_SET(old,flag_table[pos].bit))
	    
		SET_BIT(new,flag_table[pos].bit)
		continue
	    

	    if (IS_SET(marked,flag_table[pos].bit))
	    
		switch(type)
		
		    case '=':
		    case '+':
			SET_BIT(new,flag_table[pos].bit)
			break
		    case '-':
			REMOVE_BIT(new,flag_table[pos].bit)
			break
		    default:
			if (IS_SET(new,flag_table[pos].bit))
			    REMOVE_BIT(new,flag_table[pos].bit)
			else
			    SET_BIT(new,flag_table[pos].bit)
		
	    
	
	*flag = new
	return
    

