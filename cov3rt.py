from socket import getaddrinfo
from scapy.all import *
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


PACKET_DELAY = None
DELIMITER_DELAY = None
END_DELAY = None
OUTPUT_TO_FILE = False
TIMEOUT = None
MAX_COUNT = None
INTERFACE = None
INPUT_FILE = None


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
        # Packet delay
        if "-pd" in argv:
            index = argv.index("-pd")
            # Ensure the next positional argument is correct
            try:
                if argv[index + 1].replace('.', '', 1).isdigit():
                    PACKET_DELAY = float(argv[index + 1])
                else:
                    error("Packet delay must be of type 'float'!")
            # Missing following positional argument
            except IndexError:
                error("Missing packet delay value!")
                exit()
        # Delimiter delay
        if "-dd" in argv:
            index = argv.index("-dd")
            # Ensure the next positional argument is correct
            try:
                if argv[index + 1].replace('.', '', 1).isdigit():
                    DELIMITER_DELAY = float(argv[index + 1])
                else:
                    error("Delimiter delay must be of type 'float'!")
            # Missing following positional argument
            except IndexError:
                error("Missing delimiter delay value!")
                exit()
        # End delay
        if "-ed" in argv:
            index = argv.index("-ed")
            # Ensure the next positional argument is correct
            try:
                if argv[index + 1].replace('.', '', 1).isdigit():
                    END_DELAY = float(argv[index + 1])
                else:
                    error("End delay must be of type 'float'!")
            # Missing following positional argument
            except IndexError:
                error("Missing end delay value!")
                exit()

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
                    error("Missing filename!")
                    exit()
            # Standard input
            else:
                # Build a string based on stdin
                message = ''
                for line in stdin:
                    message += line
            
            # Send logic
            
        # Receive message
        elif "-r" in argv:
            # Output to file
            if "-o" in argv:
                OUTPUT_TO_FILE = True
                index = argv.index("-o")
                # Ensure the next positional argument is correct
                try:
                    filename = argv[index + 1]
                    # Ensure we can write to the file
                    try:
                        f = open(filename, "w")
                        f.write('')
                        f.close()
                    # Other file error
                    except FileExistsError:
                        error("Error in writing to {}!".format(filename))
                        exit()
                # Missing following positional argument
                except IndexError:
                    error("Missing output filename!")
                    exit()
            # Timeout
            if "-t" in argv:
                index = argv.index("-t")
                # Ensure the next positional argument is correct
                try:
                    if argv[index + 1].replace('.', '', 1).isdigit():
                        TIMEOUT = float(argv[index + 1])
                    else:
                        error("Timeout must be of type 'float'!")
                # Missing following positional argument
                except IndexError:
                    error("Missing timeout value!")
                    exit()
            # Max packet count
            if "-mc" in argv:
                index = argv.index("-mc")
                # Ensure the next positional argument is correct
                try:
                    if argv[index + 1].isdigit():
                        MAX_COUNT = float(argv[index + 1])
                    else:
                        error("Max packet count must be of type 'int'!")
                # Missing following positional argument
                except IndexError:
                    error("Missing max packet count value!")
                    exit()
            # Interface
            if "-iface" in argv:
                index = argv.index("-iface")
                # Ensure the next positional argument is correct
                try:
                    INTERFACE = float(argv[index + 1])
                # Missing following positional argument
                except IndexError:
                    error("Missing interface value!")
                    exit()
            # Input file
            if "-in" in argv:
                index = argv.index("-in")
                # Ensure the next positional argument is correct
                try:
                    INPUT_FILE = argv[index + 1]
                    # Ensure we can read the file
                    try:
                        f = open(INPUT_FILE, "r")
                        f.close()
                    # Other file error
                    except FileExistsError:
                        error("Error in reading {}!".format(INPUT_FILE))
                        exit()
                # Missing following positional argument
                except IndexError:
                    error("Missing input filename!")
                    exit()

            # Receive logic


        else:
            error("Please specify send/receive!")
            exit()
