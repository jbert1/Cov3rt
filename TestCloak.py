from os import listdir

# This will need to be changed when used in actual cov3rt
from cov3rt import UserDefinedCloaks 
from inspect import getmembers, isclass
from logging import error
from importlib import import_module

module_path = "cov3rt.UserDefinedCloaks."

def get_filepath():
    filepath = UserDefinedCloaks.__file__
    return filepath[:-12]

def get_cloaks():
    
    files = listdir(get_filepath())
    cloak_list = {}

    for i in range(len(files)): 
        filename = files[i]
        if filename not in ["__init__.py", "__pycache__"] and filename[-3:] == ".py":
            cloak_list[i - 1] = filename
    return cloak_list

def list_cloaks(cloak_list):

    print("User Defined Cloaks:")
    for i in cloak_list:
        print("{} -> {}".format(i,cloak_list[i]))

def testChosenCloak(cloak_list, num):

    global module_path
    module = cloak_list[num]
    module_path = module_path + module[:-3] 

    try:
        import_module(module_path)
        print("Success")
    except:
        # JUSTIN WRITE SOMETHING HERE PLEASE THANKS
        error("Syntax error")

def run():
    list_cloaks(get_cloaks())
    testChosenCloak(get_cloaks(),0)
