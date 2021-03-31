from os import listdir

# This will need to be changed when used in actual cov3rt
from cov3rt import Cloaks 
from inspect import getmembers, isclass
from logging import error
from importlib import import_module

module_path = "cov3rt.Cloaks."

# Get filepath to user defined cloaks folder
def get_filepath():
    filepath = Cloaks.__file__
    return filepath[:-12]

# Create a dictionary with all User Defined Cloaks
def get_cloaks():
    
    files = listdir(get_filepath())
    cloak_list = {}
    counter = 0

    for i in range(len(files)):
        filename = files[i]
        if filename not in ["__init__.py", "__pycache__","Cloak.py"] and filename[-3:] == ".py":
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
        # JUSTIN WRITE SOMETHING HERE PLEASE, THANKS... haha :)...
        error("Syntax error")
        exit(0)

    cls = getmembers(module, isclass)
    
    # Second Test 
    # Check to see if there is a cloak class
    if len(cls) < 1:
        error("No cloak class defined")
        exit(0)
    else:
        
        nameCheck = False
        
        # Third Test
        # Make sure name of class is the same as the name of the file
        for clsName in cls:
            if clsName[0] == moduleName[:-3]:
                moduleName = clsName[0]
                classInstance = clsName[1]
                nameCheck = True 
                break

        if not nameCheck:
            error("Please make sure that class name matches file name.")
            exit(0)

        else:
            
            testCloak = classInstance()
            
            # Test to see if ingest function works properly for ASCII characters
            # Test with smallest and lowest printable ASCII characters
            try:
                testCloak.ingest(" ")
                testCloak.ingest("~")

            except:
                # Yo Justin you know how to write these better than me... <-----
                error("Ingest function does not work with ASCII characters.")

            # Test if ingest function works properly for UTF-8 characters 
            try:
                testCloak.ingest("🐭 🧀")    
            except:
                # Yo justin you might have to change this... haha :)...
                error("No cheess for the packet rat :(")

            



# Test function for Sam

# Haha :)
def run():
    list_cloaks(get_cloaks())
    testChosenCloak(get_cloaks(),8)
