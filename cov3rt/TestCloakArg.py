from logging import error
from sys import argv

cloak_list = {}

# Prints a typical help screen for usage information
def print_help():
    print("""Usage: python3 TestCloak.py [-h] [-l] -c cloak_id 
    Primary Arguments:
    -c,  --cloak          Selected covert channel implementation

    Other Arguments:
    -h,  --help           Show this help screen
    -l,  --listCloaks     List available cloaks"""
)

# Hand written parser because argparse sucks
if ("-h" in argv or "--help" in argv or "?" in argv):
    # print_help()
    pass
else:
    # List files
    if ("-l" in argv or "--list-cloaks" in argv):
        # list_cloaks()
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
        
        # Continue with testing

    else:
        error("Please specify cloak type!")
        exit()
    