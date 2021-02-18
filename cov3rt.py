 #####################################################################
#                                                                    #
#                                   ╭───╮       │                    #
#                             ╱╲_╱╲     │      ─┼──                  #
#                  ╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │                    #
#                  │    │   │ >╲ ╱<     │ │     │                    #
#                  ╰─── ╰───╯   v   ╰───╯ ╵     ╰──                  #
#                                                                    #
#             Authors: Justin Berthelot, Daniel Munger,              #
#                      Christopher Rice, Samuel Dominguez            #
#                                                                    #
#####################################################################

import npyscreen
from sys import argv, stdin
from importlib import import_module
from inspect import getmembers, isclass, signature
from os import listdir
from os import name as OS_NAME
from logging import error, basicConfig, INFO, DEBUG
from cov3rt import Cloaks

# Sizing for forms
WINDOW_LINES = 22
WINDOW_COLUMNS = 80
# Store cloak classifications
cloaks =  {
    Cloaks.Cloak.INTER_PACKET_TIMING : [
    ],

    Cloaks.Cloak.MESSAGE_TIMING : [
    ],

    Cloaks.Cloak.RATE_THROUGHPUT_TIMING : [
    ],

    Cloaks.Cloak.ARTIFICIAL_LOSS : [
    ],

    Cloaks.Cloak.MESSAGE_ORDERING : [
    ],

    Cloaks.Cloak.RETRANSMISSION : [
    ],

    Cloaks.Cloak.FRAME_COLLISIONS : [
    ],
    
    Cloaks.Cloak.TEMPERATURE : [
    ],

    Cloaks.Cloak.SIZE_MODULATION : [
    ],

    Cloaks.Cloak.POSITION : [
    ],

    Cloaks.Cloak.NUMBER_OF_ELEMENTS : [
    ],

    Cloaks.Cloak.RANDOM_VALUE : [
    ],

    Cloaks.Cloak.CASE_MODULATION : [
    ],

    Cloaks.Cloak.LSB_MODULATION : [
    ],
    
    Cloaks.Cloak.VALUE_INFLUENCING : [
    ],

    Cloaks.Cloak.RESERVED_UNUSED : [
    ],
    
    Cloaks.Cloak.PAYLOAD_FIELD_SIZE_MODULATION : [
    ],

    Cloaks.Cloak.USER_DATA_CORRUPTION : [
    ],

    Cloaks.Cloak.MODIFY_REDUNDANCY : [
    ],

    Cloaks.Cloak.USER_DATA_VALUE_MODULATION_RESERVED_UNUSED : [
    ],
}
# Stores the classname and description of each cloak
cloak_names = []

# Main application
class App(npyscreen.NPSAppManaged):
    def onStart(self):
        # Starter form
        self.addForm("MAIN", 
            MainForm, 
            name = "Welcome to cov3rt",
            lines = WINDOW_LINES,
            columns = WINDOW_COLUMNS
        )
        # Cloak Options
        self.addForm("CloakOptions",
            CloakOptionsForm,
            name = "Cloak Selection",
            lines = WINDOW_LINES,
            columns = WINDOW_COLUMNS
        )
        # Send or Receive Options
        self.addForm("Communications",
            SendReceive,
            name = "Sender and Receiver Options",
            lines = WINDOW_LINES,
            columns = WINDOW_COLUMNS
        )

# Starter page for our interactive application
class MainForm(npyscreen.ActionForm, npyscreen.FormWithMenus):

    # Defines the elements on the page
    def create(self):
        # Start the element one line higher
        self.nextrely -= 1
        # Header with our fresh mouse logo
        self.header = self.add(npyscreen.Pager, relx = 20, color = "DANGER", editable = False, height = 5,
            values = [
                "                 ╭───╮       │",
                "           ╱╲_╱╲     │      ─┼──",
                "╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │  ",
                "│    │   │ >╲ ╱<     │ │     │  ",
                "╰─── ╰───╯   v   ╰───╯ ╵     ╰──"
            ]
        )
        # Start the next element 2 lines down
        self.nextrely += 2
        # Disclaimer for the malicious idiots
        self.disclaimer = self.add(npyscreen.Pager, height = 5, relx = 5, editable = False,
            values = [
                "This tool should only be used to enhance the effectiveness of",
                "communication policy. You should not misuse this tool to gain",
                "access into computer systems or to circumvent communication policy",
                "on networks you do not own. We are not responsible for any direct",
                "or indirect damages caused due to the improper usage of this tool."
            ]
        )
        # Start the next element 1 line down
        self.nextrely += 1
        # Classification, name, and description fields
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
                # Add the cloak name to the submenu
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
        if self.cloak_name.value != "":
            # Pass it to the Secondary form
            self.parentApp.getForm("CloakOptions").cloak = self.cloak
            self.parentApp.getForm("CloakOptions").populateScreen()
            self.parentApp.switchForm("CloakOptions")
        # No element selected
        else:
            npyscreen.notify_wait("Please select a cloak before proceeding.", "Invalid Cloak", "DANGER")

    # Runs when the user cancels the form
    def on_cancel(self):
        # Ensure the user wants to exit
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            # Send them away with a smile
            npyscreen.notify_confirm("Thank you for using cov3rt!")
            self.parentApp.setNextForm(None)

# Form that shows cloak options for the selected cloak
class CloakOptionsForm(npyscreen.ActionForm):
    
    # Defines the elements on the page
    def create(self):
        # Name and Description
        self.cloak_name = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Name:",
            value = ""
        )
        self.cloak_description = self.add(npyscreen.TitlePager, relx = 5, begin_entry_at = 18, editable = False, height = 2,
            name = "Description:",
            values = ["Press CTRL+X to open the menu."]
        )

    # Populates the screen
    def populateScreen(self):
        # Populate existing on-screen items
        self.cloak_name.value = self.cloak.name
        self.cloak_description.values = self.cloak.description.split("\n")
        # Create an instance of the cloak
        self.instance = self.cloak()
        # Start the next element 1 line down
        self.nextrely += 1
        # Get the parameters for the constructor
        self.parameter_list = dict(signature(self.instance.__init__).parameters)
        self.parameters = []
        # Loop over the parameters
        for p in self.parameter_list:
            # Add the field to our list
            self.parameters.append(self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18, name = p, value = str(self.parameter_list[p].default)))
        # Start the next element 1 line down
        self.nextrely += 1
        # Add the sender / receiver SelectOne element
        self.send_or_recv = self.add(npyscreen.TitleSelectOne, relx = 5, begin_entry_at = 18, scroll_exit = True, height = 2,
            name = "Sender/Receiver",
            values = ["Sender", "Receiver"]
        )
        
    # Runs when the user completes the form
    def on_ok(self):
        # Sender / Receiver not selected
        if (len(self.send_or_recv.value) == 0):
            npyscreen.notify_wait("Please pick Sender or Receiver.", "Sender or Receiver", "DANGER")
        else:
            # Create a variable to determine if we have correct values for all parameters
            editing = False
            # Loop over the parameters
            for element in self.parameters:
                # Get the name and value
                p = element.name
                new_val = element.value
                # String parameter
                if isinstance(self.parameter_list[p].default, str):
                    try:
                        exec("self.instance.{} = '{}'".format(p, new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
                # Integer parameter
                elif isinstance(self.parameter_list[p].default, int):
                    try:
                        if new_val.isdigit():
                            exec("self.instance.{} = int({})".format(p, new_val))
                        else:
                            error("{} must be of type 'int'!".format(new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
                # Float parameter
                elif isinstance(self.parameter_list[p].default, float):
                    try:
                        if new_val.replace('.', '', 1).isdigit():
                            exec("self.instance.{} = float({})".format(p, new_val))
                        else:
                            error("{} must be of type 'float'!".format(new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
            # Correct values for all parameters
            if not editing:
                # Get the next form
                toSor = self.parentApp.getForm("Communications")
                # Send / Receive 
                toSor.sor = self.send_or_recv.values[self.send_or_recv.value[0]]
                # Instance of cloak
                toSor.cloak = self.instance
                # Name of cloak
                toSor.cloak_name.value = self.instance.name
                # Populate elements
                toSor.populateScreen()
                # Go to the next form
                self.parentApp.setNextForm("Communications")

    # Runs when the user cancels the form
    def on_cancel(self):
        # Ensure the user wants to exit
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            # Send them away with a smile
            npyscreen.notify_confirm("Thank you for using cov3rt!")
            self.parentApp.setNextForm(None)

# Form that shows send/receive options for the selected cloak
class SendReceive(npyscreen.ActionForm):
    
    # Defines the elements on the page
    def create(self):
        # Cloak Name
        self.cloak_name = self.add(npyscreen.FixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Cloak: "
        )

    # Populates the screen
    def populateScreen(self):
        # Sender options
        if (self.sor == "Sender"):
            # Start the next element 1 line down
            self.nextrely += 1
            # Create a SelectOne type to determine message type
            self.whattosend = self.add(npyscreen.TitleSelectOne, relx = 5, begin_entry_at = 18, scroll_exit = True, height = 2,
                name = "Message Type:",
                values = ["File Input", "Text Input"]
            )
            # Function that runs when the user selects one 
            self.whattosend.when_value_edited = self.handleValueChange
            # Start the next element 1 line down
            self.nextrely += 1
            # Filename input option
            self.filename = self.add(npyscreen.TitleFilenameCombo, relx = 5, begin_entry_at = 18,
                name="Filename:", label=True
            )
            # Text input option
            self.inputtext = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Text Input:", value = ""
            )
            # Hide both of the elements
            self.filename.hidden = True
            self.inputtext.hidden = True
        # Receiver options
        else:
            # Timeout
            self.timeout = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Timeout:",
                value = "None"
            )
            # Max Count
            self.maxcount = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Max Count:",
                value = "∞"
            )
            # Interface
            self.iface = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Interface:",
                value = "eth0" if OS_NAME != "nt" else "Wi-Fi"
            )
            # Input File
            self.in_file = self.add(npyscreen.TitleFilenameCombo, relx = 5, begin_entry_at = 18,
                name="Input File:", label=True
            )
            # Output File
            self.out_file = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Output File:",
                value = "None"
            )
            
    # Function to handle change in SelectOne element
    def handleValueChange(self):
        # Only run if something has been selected
        if (len(self.whattosend.value) != 0):
            # File input selected
            if(self.whattosend.values[self.whattosend.value[0]] == "File Input"):
                # Show File Input
                self.filename.hidden = False
                # Hide Text Input
                self.inputtext.hidden = True
            # Text input selected
            elif(self.whattosend.values[self.whattosend.value[0]] == "Text Input"):
                # Hide File Input
                self.filename.hidden = True
                # Show Text Input
                self.inputtext.hidden = False
            # Force the elements to update their display setting
            self.filename.display()
            self.inputtext.display()
    
    # Runs when the user completes the form
    def on_ok(self):
        # Create a variable to determine if we have correct values for all parameters
        editing = False
        # Sender options
        if (self.sor == "Sender"):
            # Text input option
            if not self.inputtext.hidden:
                # Empty value
                if (self.inputtext.value == ""):
                    npyscreen.notify_wait("Message must not be empty.", title = "No Message Error")
                    editing = True
                else:
                    self.message = self.inputtext.value
            # File input option
            if not self.filename.hidden:
                if (self.filename.value == None):
                    npyscreen.notify_wait("You must select a file.", title = "No File Selected")
                    editing = True
                else:
                    # Ensure we can read the file
                    try:
                        f = open(self.filename.value, "r")
                        # Set the text of the file as our message
                        self.message = f.read()
                        f.close()
                        
                    # File not found error
                    except FileNotFoundError:
                        npyscreen.notify_wait("Input file ({}) does not exist.".format(self.filename.value), title = "Input Filename Error")
                        editing = True
                    # Other file error
                    except FileExistsError:
                        npyscreen.notify_wait("Cannot read input file ({}).".format(self.filename.value), title = "Input Filename Error")
                        editing = True
            
            # Correct values for all parameters
            if not (editing):
                # Ingest the message in our cloak
                self.cloak.ingest(self.message)
                # Notify the user before the message is about to send
                npyscreen.notify_wait("Sending the message...", title = "Message Status")
                # Send the message
                self.cloak.send_packets()
                # Notify the user the message has been sent
                npyscreen.notify_wait("Packets have been sent. Thank you for using cov3rt!", title = "Message Sent Successfully")
                self.parentApp.setNextForm(None)

        # Receiver options
        else:
            
            # Timeout option
            if (self.timeout.value == "None"):
                # Set the default value
                self.timeoutval = None
            else:
                # Ensure the timeout is a float / integer
                if (self.timeout.value.replace(".", "", 1).isdigit()):
                    self.timeoutval = float(self.timeout.value)
                else:
                    npyscreen.notify_wait("Timeout Value must be an integer or float.", title = "Timeout Value Error")
                    editing = True

            # Max Count
            if (self.maxcount.value == "∞"):
                # Set the default value
                self.maxcountval = None
            else:
                # Ensure the max count is an integer
                if (self.maxcount.value.isdigit()):
                    self.maxcountval = int(self.maxcount.value)
                else:
                    npyscreen.notify_wait("Max Count Value must be an integer.", title = "Max Count Value Error")
                    editing = True

            # Interface
            if (self.iface.value == "eth0" or self.iface.value == "Wi-Fi"):
                # Set the default value
                self.ifaceval = "eth0" if self.iface.value == "eth0" else "Wi-Fi"
            # Ensure the interface is not blank
            elif (self.iface.value == ""):
                npyscreen.notify_wait("Interface must not be empty.", title = "Interface Value Error")
                editing = True
            else:
                self.ifaceval = self.iface.value

            # Input file
            if (self.in_file.value == None):
                # Set the default value
                self.infileval = None
            else:
                # Ensure we can read the file
                try:
                    f = open(self.in_file.value, "r")
                    f.close()
                    # Set the value 
                    self.infileval = self.in_file.value
                # File not found error
                except FileNotFoundError:
                    npyscreen.notify_wait("Input file ({}) does not exist.".format(self.in_file.value), title = "Input Filename Error")
                    editing = True
                # Other file error
                except FileExistsError:
                    npyscreen.notify_wait("Cannot read input file ({}).".format(self.in_file.value), title = "Input Filename Error")
                    editing = True

            # Output file
            if (self.out_file.value == "None"):
                # Set the default value
                self.outfileval = None
            # Ensure the output file is not blank
            elif (self.out_file.value == ""):
                npyscreen.notify_wait("Output Filename must not be empty.", title = "Output Filename Value Error")
                editing = True
            else:
                # Ensure we can write to the file
                try:
                    f = open(self.out_file.value, "w")
                    f.write('')
                    f.close()
                    # Set the value 
                    self.outfileval = self.out_file.value
                # Other file error
                except FileExistsError:
                    npyscreen.notify_wait("Cannot write to output file ({}).".format(self.out_file.value), title = "Output Filename Error")
                    editing = True

            # Correct values for all parameters
            if not (editing):
                # Notify the user before the message is about to send
                npyscreen.notify_wait("Listening for the message...", title = "Message Status")
                if (self.outfileval):
                    self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outfileval)
                    # Notify the user the message has been received
                    npyscreen.notify_wait("Your message has been saved to {}. Thank you for using cov3rt!".format(self.outfileval), title = "Message Received Successfully")
                else:
                    self.decoded_message = self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outfileval)
                    # Notify the user the message has been received
                    npyscreen.notify_wait("Your secret message is '{}'. Thank you for using cov3rt!".format(self.decoded_message), title = "Message Received Successfully")
                self.parentApp.setNextForm(None)

    # Runs when the user cancels the form
    def on_cancel(self):
        # Ensure the user wants to exit
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            # Send them away with a smile
            npyscreen.notify_confirm("Thank you for using cov3rt!")
            self.parentApp.setNextForm(None)

# Sorting function for our cloaks
def nameSort(item):
    return item.name

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
  -o,  --outFile         Output packets from packet handler to a file"""

# For a later day:
# Options:
#   -pd, --packetDelay    Delay between packets
#   -dd, --delimitDelay   Delay before each packet delimiter
#   -ed, --endDelay       Delay before EOT packet
#   -d,  --default        Use the default options for the cloak
#   -v,  --verbose        Increase verbosity
#   -vv, --veryVerbose    Maximum verbosity"""
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
    # Hand written parser because argparse sucks
    if ("-h" in argv or "--help" in argv or "?" in argv):
        print_help()
    else:
        # Get path for cov3rt
        if OS_NAME == "nt":
            # Windows path
            COV3RT_PATH = "\\".join(Cloaks.__file__.split("\\")[:-1])
        else:
            COV3RT_PATH = '/'.join(Cloaks.__file__.split('/')[:-1])

        # Add the existing cloaks to our classifications
        add_classes(COV3RT_PATH, "cov3rt.Cloaks")
        # Delete empty classifications
        for empty in [cloak for cloak in cloaks if len(cloaks[cloak]) == 0]: del cloaks[empty]

        # List cloaks
        if ("-l" in argv or "--listCloaks" in argv):
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
            # Send / Receive not selected
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
                        elif isinstance(parameters[p].default, float):
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