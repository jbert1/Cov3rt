from os import listdir

# This will need to be changed when used in actual cov3rt
from cov3rt import UserDefinedCloaks 
from inspect import getmembers, isclass
from logging import error
from importlib import import_module

module_path = "cov3rt.UserDefinedCloaks."

# Get filepath to user defined cloaks folder
def get_filepath():
    filepath = UserDefinedCloaks.__file__
    return filepath[:-12]

# Create a dictionary with all User Defined Cloaks
def get_cloaks():
    
    files = listdir(get_filepath())
    cloak_list = {}
    counter = 0

    for i in range(len(files)):
        filename = files[i]
        if filename not in ["__init__.py", "__pycache__"] and filename[-3:] == ".py":
            cloak_list[counter] = filename
            counter += 1
    return cloak_list

# List out all user defined cloaks
def list_cloaks(cloak_list):

    print("User Defined Cloaks:")
    for i in cloak_list:
        print("{} -> {}".format(i,cloak_list[i]))

# Test user defined cloaks
def testChosenCloak(cloak_list, num):

    global module_path
    moduleName = cloak_list[num]
    module_path = module_path + moduleName[:-3] 
    
    # First Test
    # Check if file is compileable
    try:
        module = import_module(module_path)
    
    except:
        # JUSTIN WRITE SOMETHING HERE PLEASE THANKS
        error("Syntax error")

    cls = getmembers(module, isclass)
    
    # Second Test 
    # Check to see if there is a cloak class
    if len(cls) < 1:
        error("No cloak class defined")
    else:
        
        nameCheck = 0

        # Third Test
        for clsName in cls:
            if clsName[0] == moduleName[:-3]:
                nameCheck = 1
        
        if not nameCheck:
            error("Please make sure that class name matches file name.")

        else:
            print("Success")

# Test function for Sam

# Haha :)
def run():
    list_cloaks(get_cloaks())
    testChosenCloak(get_cloaks(),1)
