import npyscreen
from sys import argv, stdin
from importlib import import_module
from inspect import getmembers, isclass, signature
from os import listdir
from os import name as OS_NAME
from logging import error, basicConfig, INFO, DEBUG
from cov3rt.Cloaks import Cloak

# This is my idea for storing cloak classifications
cloaks =  {
    Cloak.Cloak.INTER_PACKET_TIMING : [
    ],

    Cloak.Cloak.MESSAGE_TIMING : [
    ],

    Cloak.Cloak.RATE_THROUGHPUT_TIMING : [
    ],

    Cloak.Cloak.ARTIFICIAL_LOSS : [
    ],

    Cloak.Cloak.MESSAGE_ORDERING : [
    ],

    Cloak.Cloak.RETRANSMISSION : [
    ],

    Cloak.Cloak.FRAME_COLLISIONS : [
    ],
    
    Cloak.Cloak.TEMPERATURE : [
    ],

    Cloak.Cloak.SIZE_MODULATION : [
    ],

    Cloak.Cloak.POSITION : [
    ],

    Cloak.Cloak.NUMBER_OF_ELEMENTS : [
    ],

    Cloak.Cloak.RANDOM_VALUE : [
    ],

    Cloak.Cloak.CASE_MODULATION : [
    ],

    Cloak.Cloak.LSB_MODULATION : [
    ],
    
    Cloak.Cloak.VALUE_INFLUENCING : [
    ],

    Cloak.Cloak.RESERVED_UNUSED : [
    ],
    
    Cloak.Cloak.PAYLOAD_FIELD_SIZE_MODULATION : [
    ],

    Cloak.Cloak.USER_DATA_CORRUPTION : [
    ],

    Cloak.Cloak.MODIFY_REDUNDANCY : [
    ],

    Cloak.Cloak.USER_DATA_VALUE_MODULATION_RESERVED_UNUSED : [
    ],
}
# Stores the classname and description of each cloak
cloak_names = []

def nameSort(item):
    return item.name

# Main application for interactive session
class App(npyscreen.NPSAppManaged):

    def onStart(self):
        self.addForm("MAIN", 
            HomePage, 
            name = "Welcome to cov3rt",
            lines = 22,
            columns = 80
        )
        self.addForm("CloakOptions",
            Second_TUI,
            name = "Cloak Selection",
            lines = 22,
            columns = 80
        )

# Main page for our interactive application
class HomePage(npyscreen.ActionForm, npyscreen.FormWithMenus):

    # Defines the elements on the page
    def create(self):
        self.nextrely -= 1
        # Header
        self.header = self.add(npyscreen.Pager, relx = 20, color = "DANGER", editable = False, height = 5,
            values = [
                "                 ╭───╮       │",
                "           ╱╲_╱╲     │      ─┼──",
                "╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │  ",
                "│    │   │  ╲_╱      │ │     │  ",
                "╰─── ╰───╯   ╳   ╰───╯ ╵     ╰──"
            ]

        )
        self.nextrely += 2
        # Disclaimer
        self.disclaimer = self.add(npyscreen.Pager, height = 5, relx = 5, editable = False,
            values = [
                "This tool should only be used to enhance the effectiveness of",
                "communication policy. You should not misuse this tool to gain",
                "access into computer systems or to circumvent communication policy",
                "on networks you do not own. We are not responsible for any direct",
                "or indirect damages caused due to the improper usage of this tool."
            ]
        )
        self.nextrely += 1
        # Classification, name, and description
        self.cloak_classification = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Classification:",
            value = ""
        )
        self.cloak_name = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Name:",
            value = ""
        )
        self.cloak_description = self.add(npyscreen.TitlePager, relx = 5, begin_entry_at = 18, editable = False,
            name = "Description:",
            values = ["Press CTRL+X to open the menu."]
        )

        # Create a menu to store cloaks
        self.menu = self.new_menu(name = "Cloak Selection",
            shortcut = '^X'
        )
        # Loop over the cloak classifications
        for cloak_classification in cloaks:
            # Temporarily store the submenu to populate it
            submenu = self.menu.addNewSubmenu(cloak_classification)
            # Loop over each cloak
            for cloak in cloaks[cloak_classification]:
                # Add it to the submenu
                submenu.addItem(
                    text = cloak.name, 
                    onSelect = self.populateScreen,
                    arguments = [cloak]
                )
            # Add close menu at the bottom for convenience
            submenu.addItem("Close Menu", self.close_menu, "^X")
        # Add close menu at the bottom for convenience
        self.menu.addItem("Close Menu", self.close_menu, "^X")

    # Closes the menu
    def close_menu(self):
        self.parentApp.setNextForm(None)

    # Populates the screen and saves the cloak type
    def populateScreen(self, cloak):
        # Save the cloak
        self.cloak = cloak
        # Populate on-screen items
        self.cloak_classification.value = cloak.classification
        self.cloak_name.value = cloak.name
        self.cloak_description.values = cloak.description.split("\n")
        
    # Runs when the user completes the form
    def on_ok(self):
        # Ensure cloak is selected
        if self.cloak_name != "":
            # Pass it to the Secondary form
            self.parentApp.getForm("CloakOptions").cloak = self.cloak
            self.parentApp.getForm("CloakOptions").populateScreen()
            self.parentApp.switchForm("CloakOptions")
        # No element selected
        else:
            npyscreen.notify_wait("Please select a cloak before proceeding.", "Invalid Cloak", "DANGER")


    # Runs when the user cancels the form
    def on_cancel(self):
        # Exit
        self.parentApp.setNextForm(None)


class Second_TUI(npyscreen.ActionForm):
    
    # Defines the elements on the page
    def create(self):

        # Classification, name, and description
        self.cloak_classification = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Classification:",
            value = ""
        )
        self.cloak_name = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Name:",
            value = ""
        )
        self.cloak_description = self.add(npyscreen.TitlePager, relx = 5, begin_entry_at = 18, editable = False,
            name = "Description:",
            values = ["Press CTRL+X to open the menu."]
        )

    # Populates the screen
    def populateScreen(self):
        # Populate on-screen items
        self.cloak_classification.value = self.cloak.classification
        self.cloak_name.value = self.cloak.name
        self.cloak_description.values = self.cloak.description.split("\n")

    # Runs when the user finishes the form
    def afterEditing(self):
        # Exit
        self.parentApp.setNextForm(None)

# Add classes from files in a folder with a defined package name
def add_classes(filepath, package_name):
    # Get all of the cloaks within the folder
    files = listdir(filepath)
    # Loop over the filenames
    for filename in files:
        # Ignore these files and accept only python files
        if (filename not in ["__init__.py", "__pycache__", "Cloak.py"]) and (filename[-3:] == ".py"):
            # Grab the module name
            module_name = package_name + '.' + filename[:-3]
            # Get each class name and class in the file
            for classname, cls in getmembers(import_module(module_name), isclass):
                # Try-catch for odd imports
                try:
                    # Create the class import path
                    module_path = "{}.{}.{}".format(package_name, classname, classname)
                    # Get the class object path
                    imprt = str(cls).split("'")[1]
                    # Compare the paths and ignore the "Cloak" import
                    if (module_path == imprt) and (classname != "Cloak"):
                        # Check for the classification
                        if cloaks.get(cls.classification, -1) != -1:
                            # Add to the classification
                            cloaks[cls.classification].append(cls)
                            # Add to the list of cloaks
                            cloak_names.append(cls)
                except:
                    pass
    # Sort the list of cloak names
    cloak_names.sort(key = nameSort)

# Prints a typical help screen for usage information
def print_help():
    print(
"""Usage: cov3rt.py [-h] [-l] [-i] (-s | -r) -c cloak_id [Options]

Primary Arguments:
  -c,  --cloak           Selected covert channel implementation
  -s,  --send            Send information via the selected cloak
  -r,  --receive         Receive information via the selected cloak

Send Options:
  -m,  --message         Send message within the command-line
  -f,  --filename        Send the contents of a file

Receive Options:
  -t,  --timeout         Timeout (in seconds) for the packet handler
  -mc, --maxCount       Max number of packets for the packet handler
  -if, --iface          Interface for the packet handler
  -in, --inFile         Use a .cap or .pcap rather than live analysis
  -o,  --outFile         Output packets from packet handler to a file

Options:
  -pd, --packetDelay    Delay between packets
  -dd, --delimitDelay   Delay before each packet delimiter
  -ed, --endDelay       Delay before EOT packet
  -d,  --default        Use the default options for the cloak
  -v,  --verbose        Increase verbosity
  -vv, --veryVerbose    Maximum verbosity"""
)

# Prints a list of available cloaks for the user to choose from
def print_list():
    print("Available Cloaks:")
    # Loop over the cloak names sorted by the key value
    for i in range(len(cloak_names)):
        print("  {} -> {}: {}".format(i, cloak_names[i].name, cloak_names[i].description.replace("\n", "\n\t")))

# OPTIONS
SENDING = False
RECEIVING = False
PACKET_DELAY = None
DELIMITER_DELAY = None
END_DELAY = None
OUTPUT_TO_FILE = False
TIMEOUT = None
MAX_COUNT = None
INTERFACE = None
INPUT_FILE = None
DEFAULT = False

if __name__ == "__main__":
    # Get path for cov3rt
    if OS_NAME == "nt":
        # Windows path
        COV3RT_PATH = "\\".join(Cloak.__file__.split("\\")[:-1])
    else:
        COV3RT_PATH = '/'.join(Cloak.__file__.split('/')[:-1])

    # Add the existing cloaks to our classifications
    add_classes(COV3RT_PATH, "cov3rt.Cloaks")

    # Hand written parser because argparse sucks
    if ("-h" in argv or "--help" in argv or "?" in argv):
        print_help()
    # List cloaks
    elif ("-l" in argv or "--listCloaks" in argv):
        print_list()
    # Interactive application
    elif ("-i" in argv or "--interactive" in argv):
        App().run()
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
                temp = argv[index + 1]
                # Check encoding
                if temp.isdigit():
                    # Check range
                    if 0 <= int(temp) <= len(cloak_names):
                        # Save cloak_type
                        cloak_type = cloak_names[int(temp)]
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
        if ("-ed" in argv or  "--endDelay" in argv):
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
        # Default parameters
        if ("-d" in argv or "--default" in argv):
            DEFAULT = True
        # Verbosity
        if ("-v" in argv or "--verbose" in argv):
            basicConfig(level=INFO)
        # Extra verbosity
        if ("-vv" in argv or "--veryVerbose" in argv):
            basicConfig(level=DEBUG)

        # Send message
        if ("-s" in argv or "--send" in argv):
            SENDING = True
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

        # Receive message
        elif ("-r" in argv or "--receive" in argv):
            RECEIVING = True
            FILENAME = None
            # Output to file
            if ("-o" in argv or "--outFile" in argv):
                OUTPUT_TO_FILE = True
                try:
                    index = argv.index("-o")
                except:
                    index = argv.index("--outFile")
                # Ensure the next positional argument is correct
                try:
                    FILENAME = argv[index + 1]
                    # Ensure we can write to the file
                    try:
                        f = open(FILENAME, "w")
                        f.write('')
                        f.close()
                    # Other file error
                    except FileExistsError:
                        error("Error in writing to {}!".format(FILENAME))
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

        ## Setup the sending mechanism
        # Instantiate the cloak
        cloak = cloak_type()
        # Custom parameters
        if not DEFAULT:
            # Get the parameters for the constructor
            parameters = dict(signature(cloak.__init__).parameters)
            for p in parameters:
                # Ask for user input
                new_val = input("Value for {} (leave blank for default '{}'): ".format(p, parameters[p].default))
                # User entered a new value
                if new_val != "":
                    # String parameter
                    if isinstance(parameters[p].default, str):
                        exec("cloak.{} = '{}'".format(p, new_val))
                    # Integer parameter
                    elif isinstance(parameters[p].default, int):
                        if new_val.isdigit():
                            exec("cloak.{} = int({})".format(p, new_val))
                        else:
                            error("{} must be of type 'int'!".format(new_val))
                    # Float parameter
                    elif isinstance(parameters[p].default, int):
                        if new_val.replace('.', '', 1).isdigit():
                            exec("cloak.{} = float({})".format(p, new_val))
                        else:
                            error("{} must be of type 'float'!".format(new_val))
        if SENDING:
            # Ingest data
            cloak.ingest(message)
            # Send packets
            cloak.send_packets(PACKET_DELAY, DELIMITER_DELAY, END_DELAY)
        elif RECEIVING:
            # Receive packets
            if OUTPUT_TO_FILE:
                cloak.recv_packets(TIMEOUT, MAX_COUNT, INTERFACE, INPUT_FILE, FILENAME)
            else:
                print(cloak.recv_packets(TIMEOUT, MAX_COUNT, INTERFACE, INPUT_FILE, FILENAME))