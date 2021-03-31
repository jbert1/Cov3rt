from os import listdir
from logging import basicConfig, error, DEBUG, INFO
from sys import argv
from cov3rt import UserDefinedCloaks 

cloak_list = {}


# Get filepath to user defined cloaks folder
def get_filepath():
    filepath = UserDefinedCloaks.__file__
    return filepath[:-12]

# Create a dictionary with all User Defined Cloaks
def get_cloaks():
    global cloak_list
    files = listdir(get_filepath())
    counter = 0

    for i in range(len(files)):
        filename = files[i]
        if filename not in ["__init__.py", "__pycache__"] and filename[-3:] == ".py":
            cloak_list[counter] = filename
            counter += 1
    return cloak_list


# Hand written parser because argparse sucks
if ("-h" in argv or "--help" in argv or "?" in argv):
    # print_help()
    pass
else:
    # List files
    if ("-l" in argv or "--list-cloaks" in argv):
        pass
    # Cloak type
    elif ("-c" in argv or "--cloak" in argv):
        # Get the index in the arglist
        try:
            index = argv.index("-c")
        except:
            index = argv.index("--cloak")
        # Ensure the next positional argument is correct
        try:
            temp = argv[index + 1]
            # Check encoding
            if temp.isdigit():
                # Check range
                if 0 <= int(temp) <= len(cloak_list):
                    # Save cloak_type
                    cloak_type = cloak_list[int(temp)]
                else:
                    error("Invalid cloak type!\nUse the '-l' option to view valid cloak types.")
                    exit()
            else:
                error("Invalid cloak type!\nUse the '-l' option to view valid cloak types.")
                exit()
        # Missing following positional argument
        except IndexError:
            error("Missing cloak type argument!\nUse the '-l' option to view valid cloak types.")
            exit()
    else:
        error("Please specify cloak type!")
        exit()