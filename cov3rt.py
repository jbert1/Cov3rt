# from scapy.all import *
from sys import argv, stdin
from logging import error, warning


"""
usage: cov3rt.py [-h] [-i] [-l] (-s | -r) (-m  | -f ) -c [-sd] [-ed] [-dd]
                 [-pd]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     launch an interactive application
  -l, --list            list available cloaks

Primary Arguments:
  -s, --send            send information via the selected cloak
  -r, --receive         receive information via the selected cloak
  -m                    read from or print to command-line
  -f                    read from or print to file
  -c                  __selected covert channel implementation

Delays:
  -sd , --startDelay    delay before communication
  -ed , --endDelay      delay before end-of-transmission
  -dd , --delimDelay    delay between delimiters
  -pd , --packetDelay   delay between packets in seconds
"""


# Argument parser
# parser = argparse.ArgumentParser()

# # Optional Arguments
# parser.add_argument("-i", "--interactive", action="store_true", help="launch an interactive application")
# parser.add_argument("-l", "--list", action="store_true", help="list available cloaks")

# # Primary Arguments
# required = parser.add_argument_group("Primary Arguments")

# # Send and Receive
# send_receive = required.add_mutually_exclusive_group(required = True)
# send_receive.add_argument("-s", "--send", action="store_true", help="send information via the selected cloak")
# send_receive.add_argument("-r", "--receive", action="store_true", help="receive information via the selected cloak")
# # Message types
# message_type = required.add_mutually_exclusive_group(required = True)
# message_type.add_argument("-m", metavar='', action="store", type=str, help="read from or print to command-line")
# message_type.add_argument("-f", metavar='', action="store", type=str, help="read from or print to file")
# # Cloak type
# required.add_argument("-c", type=int, action="store", help="__selected covert channel implementation", required=True, metavar='\b') 
# # Delays
# delay_type = parser.add_argument_group("Delays")
# delay_type.add_argument("-sd", "--startDelay", metavar='', type=float, action="store", help="delay before communication")
# delay_type.add_argument("-ed", "--endDelay", metavar='', type=float, action="store", help="delay before end-of-transmission")
# delay_type.add_argument("-dd", "--delimDelay", metavar='', type=float, action="store", help="delay between delimiters")
# delay_type.add_argument("-pd", "--packetDelay", metavar='', type=float, action="store", help="delay between packets in seconds")

# args = parser.parse_args()

START_DELAY = None
END_DELAY = None
DELIMITER_DELAY = None
PACKET_DELAY = None

def print_help():
    print("Usage: xxx")

def print_list():
    print("list")

def interactive():
    print("interactive")

if __name__ == "__main__":
    # Hand written parser because argparse sucks
    if "-h" in argv:
        print_help()
    # List cloaks
    elif "-l" in argv:
        print_list()
    # Interactive application
    elif "-i" in argv:
        interactive()
    # Other arguments
    else:
        # Cloak type
        if "-c" in argv:
            # Get the index in the arglist
            index = argv.index("-c")
            # Ensure the next positional argument is correct
            try:
                # Check encoding
                if argv[index + 1].isdigit():
                    ### MAKE SURE TO ADD ERROR CHECK FOR ENCODING RANGE
                    cloak_type = argv[index + 1]
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
        
        # Optional arguments
        # Start delay
        if "-sd" in argv:
            pass

        # Send message
        if "-s" in argv:
            # Console Message
            if "-m" in argv:
                index = argv.index("-m")
                # Ensure the next positional argument is correct
                try:
                    message = argv[index + 1]
                # Missing following positional argument
                except IndexError:
                    error("Missing message!")
                    exit()
            # Filename
            elif "-f" in argv:
                index = argv.index("-f")
                # Ensure the next positional argument is correct
                try:
                    filename = argv[index + 1]
                    # Error handling for opening the file
                    try:
                        f = open(filename, "r", encoding="UTF-8")
                        message = f.read()
                        f.close()
                    # File not found
                    except FileNotFoundError:
                        error("Could not find file {}!".format(filename))
                        exit()
                    # Other file error
                    except FileExistsError:
                        error("Error in opening {}!".format(filename))
                        exit()
                # Missing following positional argument
                except IndexError:
                    error("Missing message!")
                    exit()
            # Standard input
            else:
                message = ''
                # Loop over the lines of stdin
                for line in stdin:
                    message += line
            
        # Receive message
        elif "-r" in argv:
            # Output to file
            if "-o" in argv:
                pass
        else:
            error("Please specify send/receive!")
            exit()
