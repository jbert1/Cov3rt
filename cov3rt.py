from scapy.all import *
from sys import argv, stdin
from logging import error

# Prints a typical help screen for usage information
def print_help():
    print(
"""Usage: cov3rt.py [-h] [-l] [-i] (-s | -r) -c cloak_id [Options]

Primary Arguments:
  -c, --cloak           Selected covert channel implementation
  -s, --send            Send information via the selected cloak
  -r, --receive         Receive information via the selected cloak

Send Options:
  -m, --message         Send message within the command-line
  -f, --filename        Send the contents of a file

Receive Options:
  -t, --timeout         Timeout (in seconds) for the packet handler
  -mc, --maxCount       Max number of packets for the packet handler
  -if, --iface          Interface for the packet handler
  -in, --inFile         Use a .cap or .pcap rather than live analysis
  -o, --outFile         Output packets from packet handler to a file

Delay Options:
  -pd, --packetDelay    Delay between packets
  -dd, --delimitDelay   Delay before each packet delimiter
  -ed, --endDelay       Delay before EOT packet"""
)
    
# Prints a list of available cloaks for the user to choose from
def print_list():
    print(
"""Here we will list enumerated cloaks (similar to hashcat's hash modes)"""
)

def interactive():
    print("npyscreen for the win")

# OPTIONS
PACKET_DELAY = None
DELIMITER_DELAY = None
END_DELAY = None
OUTPUT_TO_FILE = False
TIMEOUT = None
MAX_COUNT = None
INTERFACE = None
INPUT_FILE = None

if __name__ == "__main__":
    # Hand written parser because argparse sucks
    if ("-h" in argv or "--help" in argv or "?" in argv):
        print_help()
    # List cloaks
    elif ("-l" in argv or "--listCloaks" in argv):
        print_list()
    # Interactive application
    elif ("-i" in argv or "--interactive" in argv):
        interactive()
    # Other arguments
    else:
        # Cloak type
        if ("-c" in argv or "--cloak" in argv):
            # Get the index in the arglist
            try:
                index = argv.index("-c")
            except:
                index = argv.index("--cloak")
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
        if ("-pd" in argv or "--packetDelay" in argv):
            try:
                index = argv.index("-pd")
            except:
                index = argv.index("--packetDelay")
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
        if ("-dd" in argv or "--delimitDelay" in argv):
            try:
                index = argv.index("-dd")
            except:
                index = argv.index("--delimitDelay")
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
            try:
                index = argv.index("-ed")
            except:
                index = argv.index("--endDelay")
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
        if ("-s" in argv or "--send" in argv):
            # Console Message
            if ("-m" in argv or "--message" in argv):
                try:
                    index = argv.index("-m")
                except:
                    index = argv.index("--message")
                # Ensure the next positional argument is correct
                try:
                    message = argv[index + 1]
                # Missing following positional argument
                except IndexError:
                    error("Missing message!")
                    exit()
            # Filename
            elif ("-f" in argv or "--filename" in argv):
                try:
                    index = argv.index("-f")
                except:
                    index = argv.index("--filename")
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
            
            ### SEND LOGIC ###
            
        # Receive message
        elif ("-r" in argv or "--receive" in argv):
            # Output to file
            if ("-o" in argv or "--outFile" in argv):
                OUTPUT_TO_FILE = True
                try:
                    index = argv.index("-o")
                except:
                    index = argv.index("--outFile")
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
            if ("-t" in argv or "--timeout" in argv):
                try:
                    index = argv.index("-t")
                except:
                    index = argv.index("--timeout")
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
            if ("-mc" in argv or "--maxCount" in argv):
                try:
                    index = argv.index("-mc")
                except:
                    index = argv.index("--maxCount")
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
            if ("-if" in argv or "--iface" in argv):
                try:
                    index = argv.index("-if")
                except:
                    index = argv.index("--iface")
                # Ensure the next positional argument is correct
                try:
                    INTERFACE = float(argv[index + 1])
                # Missing following positional argument
                except IndexError:
                    error("Missing interface value!")
                    exit()
            # Input file
            if ("-in" in argv or "--inFile" in argv):
                try:
                    index = argv.index("-in")
                except:
                    index = argv.index("--inFile")
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

            ### RECEIVE LOGIC ###


        else:
            error("Please specify send/receive!")
            exit()
