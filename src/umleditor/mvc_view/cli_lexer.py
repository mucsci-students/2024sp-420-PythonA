from umleditor.mvc_model import CustomExceptions as CE

#map relating commands to the flags that can be passed to them
#NOTE: These must be synched with the command_function_map based on idx
_command_flag_map = {
    "class" : ["a","d","r"],
    "list"  : ["a","c","r","d"],
    "fld"   : ["a","d","r"],
    "mthd"  : ["a","d","r"],
    "rel"   : ["a","d"],
    "save"  : [""],
    "load"  : [""],
    "exit"  : [""],
    "quit"  : [""],
    "help"  : [""]
}

#map relating commands to the names of methods that can be called on them
#NOTE: these must be synched with command_flag_map based on idx
_command_function_map = {
    "class" : ["add_entity","delete_entity","rename_entity"],
    "list"  : ["list_everything","list_entities","list_relations","list_entity_details"],
    "fld"   : ["add_field","delete_field","rename_field"],
    "mthd"  : ["add_method","delete_method","rename_method"],
    "rel"   : ["add_relation","delete_relation"],
    "save"  : ["save"],
    "load"  : ["load"],
    "exit"  : ["quit"],
    "quit"  : ["quit"],
    "help"  : ["help_menu"]
}

def lex_input(command:list, flag:list):
    '''Finds the name of the function that should be called
    
        Args:
            command - the command that was given to the parser
            flag - the flag that was given to the parser
        
        Raises: 
            CustomExceptions.CommandNotFoundError if the command entered is
                invalid
            CustomExceptions.InvalidFlagError if the flag entered is invalid
    
        Returns:
            The name of the function that needs to be called
    '''
    #convert the params to strings
    command = str(command[0])
    flag = str(flag[0]) if len(flag) > 0 else ""

    #check if the list of keys in the commmand flag map contains the given command
    command_list = list(_command_flag_map.keys())

    valid_command = command_list.__contains__(command)
    if not valid_command:
        raise CE.CommandNotFoundError(command)
    
    #pull the list of flags for the validated command
    flag_list = _command_flag_map[command]
    
    #Make sure that the flag is a flag (preceded with -)
    #some commands are just "command arg" so this needs to be checked
    prepped_flag = ""
    valid_flag = True
    if flag.__contains__("-"):
        prepped_flag = flag.lstrip("-")
        valid_flag = flag_list.__contains__(prepped_flag)
    
    if not valid_flag:
        raise CE.InvalidFlagError(flag, command)
    
    #compiling the correct location to index into the function map
    flag_index = flag_list.index(prepped_flag)
    flags = _command_function_map.get(command)
    return flags[flag_index]
