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


def runApplication():

    from importlib import import_module
    from inspect import getmembers, isclass, signature
    from logging import basicConfig, error, DEBUG, INFO
    import npyscreen
    from os import listdir
    from sys import argv, stdin
    from psutil import net_if_stats

    # Sizing for forms
    WINDOW_LINES = 22
    WINDOW_COLUMNS = 80

    # Main application
    class App(npyscreen.NPSAppManaged):
        def onStart(self):
            # Starter form
            self.addForm("MAIN",
                         MainForm,
                         name="Welcome to cov3rt",
                         lines=WINDOW_LINES,
                         columns=WINDOW_COLUMNS)
            # Cloak Options
            self.addForm("CloakOptions",
                         CloakOptionsForm,
                         name="Cloak Options",
                         lines=WINDOW_LINES,
                         columns=WINDOW_COLUMNS)
            # Send or Receive Options
            self.addForm("Communications",
                         SendReceive,
                         name="Sender and Receiver Options",
                         lines=WINDOW_LINES,
                         columns=WINDOW_COLUMNS)

    # Starter page for our interactive application
    class MainForm(npyscreen.ActionForm, npyscreen.FormWithMenus):

        # Defines the elements on the page
        def create(self):
            # Add CTRL+C Handler
            self.add_handlers({"^C": self.exit_application})
            # Start the element one line higher
            self.nextrely -= 1
            # Header with our fresh mouse logo
            self.header = self.add(npyscreen.Pager, relx=20, color="DANGER", editable=False, height=5,
                values=[
                    "                 ╭───╮       │",
                    "           ╱╲_╱╲     │      ─┼──",
                    "╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │  ",
                    "│    │   │ ⚞╲ ╱⚟     │ │     │  ",
                    "╰─── ╰───╯   v   ╰───╯ ╵     ╰──"
                ]
            )
            # Start the next element 2 lines down
            self.nextrely += 2
            # Disclaimer for the malicious idiots
            self.disclaimer = self.add(npyscreen.Pager, height=5, relx=5, editable=False,
                values=[
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
            self.cloak_classification = self.add(npyscreen.TitleFixedText, relx=5, begin_entry_at=18, editable=False, 
                name="Classification:",
                value=""
            )
            self.cloak_name = self.add(npyscreen.TitleFixedText, relx=5, begin_entry_at=18, editable=False, 
                name="Name:",
                value=""
            )
            self.cloak_description = self.add(npyscreen.TitlePager, relx=5, begin_entry_at=18, editable=False, 
                name="Description:",
                values=[
                    "Press CTRL+X to open the menu."
                ]
            )
            # Create a menu to store cloaks
            self.menu = self.new_menu(name="Cloak Selection", shortcut='^X')
            # Loop over the cloak classifications
            for cloak_classification in cloaks:
                # Temporarily store the submenu to populate it
                submenu = self.menu.addNewSubmenu(cloak_classification)
                # Loop over each cloak
                for cloak in cloaks[cloak_classification]:
                    # Add the cloak name to the submenu
                    submenu.addItem(text=cloak.name, onSelect=self.populateScreen, arguments=[cloak])
                # Add close menu at the bottom for convenience
                submenu.addItem("Close Menu", self.close_menu, "^X")
            # Add close menu at the bottom for convenience
            self.menu.addItem("Close Menu", self.close_menu, "^X")

        # Function to exit on CTRL+C
        def exit_application(self, _):
            self.parentApp.setNextForm(None)
            self.editing = False

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
            # Add CTRL+C Handler
            self.add_handlers({"^C": self.exit_application})
            # Name and Description
            self.cloak_name = self.add(npyscreen.TitleFixedText, relx=5, begin_entry_at=18, editable=False, 
                name="Name:",
                value=""
            )
            self.cloak_description = self.add(npyscreen.TitlePager, relx=5, begin_entry_at=18, editable=False, height=2, 
                name="Description:",
                values=[
                    "Press CTRL+X to open the menu."
                ]
            )
        
        # Function to exit on CTRL+C
        def exit_application(self, _):
            self.parentApp.setNextForm(None)
            self.editing = False

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
                self.parameters.append(self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name=p,
                    value=str(self.parameter_list[p].default)
                ))
            # Start the next element 1 line down
            self.nextrely += 1
            # Add the sender / receiver SelectOne element
            self.send_or_recv = self.add(npyscreen.TitleSelectOne, relx=5, begin_entry_at=18, scroll_exit=True, height=2, 
                name="Sender/Receiver",
                values=[
                    "Sender",
                    "Receiver"
                ]
            )

        # Runs when the user completes the form
        def on_ok(self):
            # Sender / Receiver not selected
            if len(self.send_or_recv.value) == 0:
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
                            setattr(self.instance, p, str(new_val))
                        except ValueError as err:
                            npyscreen.notify_wait(str(err), title="Value Error!")
                            editing = True
                        except TypeError as err:
                            npyscreen.notify_wait(str(err), title="Type Error!")
                            editing = True
                    # Integer parameter
                    elif isinstance(self.parameter_list[p].default, int):
                        try:
                            if new_val.isdigit():
                                setattr(self.instance, p, int(new_val))
                            else:
                                npyscreen.notify_wait("Parameter '{}' must be an integer.".format(p), title="Type Error!")
                                editing = True
                        except ValueError as err:
                            npyscreen.notify_wait(str(err), title="Value Error!")
                            editing = True
                        except TypeError as err:
                            npyscreen.notify_wait(str(err), title="Type Error!")
                            editing = True
                    # Float parameter
                    elif isinstance(self.parameter_list[p].default, float):
                        try:
                            if new_val.replace('.', '', 1).isdigit():
                                setattr(self.instance, p, float(new_val))
                            else:
                                npyscreen.notify_wait("Parameter '{}' must be an integer or float.".format(p), title="Type Error!")
                                editing = True
                        except ValueError as err:
                            npyscreen.notify_wait(str(err), title="Value Error!")
                            editing = True
                        except TypeError as err:
                            npyscreen.notify_wait(str(err), title="Type Error!")
                            editing = True
                # Correct values for all parameters
                if not editing:
                    # Get the next form
                    toSor = self.parentApp.getForm("Communications")
                    # Send / Receive
                    toSor.sor = self.send_or_recv.values[
                        self.send_or_recv.value[0]]
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
    class SendReceive(npyscreen.ActionForm, npyscreen.FormWithMenus):

        # Defines the elements on the page
        def create(self):
            # Add CTRL+C Handler
            self.add_handlers({"^C": self.exit_application})
            # Cloak Name
            self.cloak_name = self.add(npyscreen.FixedText, relx=5, begin_entry_at=18, editable=False, 
                name="Cloak: "
            )
            # Start the next element 1 line down
            self.nextrely += 1
            # Interface
            self.iface = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, editable=False,
                name="Interface:",
                value="Default"
            )
            self.menu = self.new_menu(name="Interface Selection", shortcut="^X")
            # Loop over the possible network interfaces
            for netiface in sorted(list(net_if_stats().keys())):
                self.menu.addItem(text=netiface, onSelect=self.selectInterface, arguments=[netiface])
            # Add close menu at the bottom for convenience
            self.menu.addItem("Close Menu", self.close_menu, "^X")

        # Add the interface name to the on-screen element
        def selectInterface(self, interface):
            # Populate on-screen interface
            self.iface.value = interface

        # Closes the menu
        def close_menu(self):
            self.parentApp.setNextForm(None)

        # Function to exit on CTRL+C
        def exit_application(self, _):
            self.parentApp.setNextForm(None)
            self.editing = False

        # Populates the screen
        def populateScreen(self):
            # Sender options
            if (self.sor == "Sender"):
                # Packet Delay Option
                self.packetdelay = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Packet Delay:",
                    value="None"
                )
                # End Delay Option
                self.enddelay = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="End Delay:",
                    value="None"
                )
                # Delimeter Delay Option
                self.delimitdelay = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Delimit Delay:",
                    value="None"
                )

                # Start the next element 1 line down
                self.nextrely += 1    
                # Create a SelectOne type to determine message type
                self.whattosend = self.add(npyscreen.TitleSelectOne, relx=5, begin_entry_at=18, scroll_exit=True, height=2, 
                    name="Message Type:",
                    values=[
                        "File Input",
                        "Text Input"
                    ]
                )
                # Function that runs when the user selects one
                self.whattosend.when_value_edited = self.handleValueChange
                
                # Start the next element 1 line down
                self.nextrely += 1
                # Filename input option
                self.filename = self.add(npyscreen.TitleFilenameCombo, relx=5, begin_entry_at=18, label=True,
                    name="Filename:"
                )
                # Text input option
                self.inputtext = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Text Input:",
                    value=""
                )
                # After selection, clear the screen
                self.filename.when_value_edited = self.clearscreen
                # Hide both of the elements
                self.filename.hidden = True
                self.inputtext.hidden = True
            
            # Receiver options
            else:
                # Timeout
                self.timeout = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Timeout:",
                    value="None"
                )
                # Max Count
                self.maxcount = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Max Count:",
                    value="∞"
                )
                # Input File
                self.in_file = self.add(npyscreen.TitleFilenameCombo, relx=5, begin_entry_at=18, label=True,
                    name="Input File:"
                )
                # After selection, clear the screen
                self.in_file.when_value_edited = self.clearscreen
                # Output Message
                self.out_file = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Output Message:",
                    value="None"
                )
                # Output Capture
                self.out_capture = self.add(npyscreen.TitleText, relx=5, begin_entry_at=18, 
                    name="Output Capture:",
                    value="None"
                )

        # Clear npyscreen terminal
        def clearscreen(self):
            npyscreen.blank_terminal()

        # Function to handle change in SelectOne element
        def handleValueChange(self):
            # Only run if something has been selected
            if len(self.whattosend.value) != 0:
                # File input selected
                if self.whattosend.values[self.whattosend.value[0]] == "File Input":
                    # Show File Input
                    self.filename.hidden = False
                    # Hide Text Input
                    self.inputtext.hidden = True
                # Text input selected
                elif self.whattosend.values[self.whattosend.value[0]] == "Text Input":
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
                # Checks for Valid Interface
                if (self.iface.value == "Default"):
                    # Set the default value
                    self.ifaceval = None
                # Ensure the interface is not blank
                elif (self.iface.value == ""):
                    npyscreen.notify_wait("Interface must not be empty.", title="Interface Value Error")
                    editing = True
                else:
                    self.ifaceval = self.iface.value

                # Checks for Valid Packet Delay
                if self.packetdelay.value == "None":
                    # Set the default value
                    self.packetdelayval = None
                else:
                    # Ensure the timeout is a float / integer
                    if (self.packetdelay.value.replace(".", "", 1).isdigit()):
                        self.packetdelayval = float(self.packetdelay.value)
                    else:
                        npyscreen.notify_wait("Packet Delay must be an integer or float.", title="Packet Delay Value Error")
                        editing = True
                
                # Checks for Valid End Delay
                if self.enddelay.value == "None":
                    # Set the default value
                    self.enddelayval = None
                else:
                    # Ensure the timeout is a float / integer
                    if (self.enddelay.value.replace(".", "", 1).isdigit()):
                        self.enddelayval = float(self.enddelay.value)
                    else:
                        npyscreen.notify_wait("End Delay must be an integer or float.", title="End Delay Value Error")
                        editing = True
                
                # Checks for Valid Delimeter Delay
                if self.delimitdelay.value == "None":
                    # Set the default value
                    self.delimitdelayval = None
                else:
                    # Ensure the timeout is a float / integer
                    if (self.delimitdelay.value.replace(".", "", 1).isdigit()):
                        self.delimitdelayval = float(self.delimitdelay.value)
                    else:
                        npyscreen.notify_wait("End Delay must be an integer or float.", title="End Delay Value Error")
                        editing = True
                
                # Text input option
                if not self.inputtext.hidden:
                    # Empty value
                    if (self.inputtext.value == ""):
                        npyscreen.notify_wait("Message must not be empty.", title="No Message Error")
                        editing = True
                    else:
                        self.message = self.inputtext.value
                # File input option
                elif not self.filename.hidden:
                    if self.filename.value is None:
                        npyscreen.notify_wait("You must select a file.", title="No File Selected")
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
                            npyscreen.notify_wait("Input file ({}) does not exist.".format(self.filename.value), title="Input Filename Error")
                            editing = True
                        # Other file error
                        except FileExistsError:
                            npyscreen.notify_wait("Cannot read input file ({}).".format(self.filename.value), title="Input Filename Error")
                            editing = True
                else:
                    npyscreen.notify_wait("Please Pick Input File or Input Text", title="Input Not Selected")
                    editing = True
                # Correct values for all parameters
                if not (editing):
                    # Ingest the message in our cloak
                    self.cloak.ingest(self.message)
                    # Notify the user before the message is about to send
                    npyscreen.notify_wait("Sending the message...", title="Message Status")
                    # Send the message
                    self.cloak.send_packets(self.ifaceval, self.packetdelayval, self.enddelayval, self.delimitdelayval)
                    # Notify the user the message has been sent
                    npyscreen.notify_wait("Packets have been sent. Thank you for using cov3rt!", title="Message Sent Successfully")
                    self.parentApp.setNextForm(None)

            # Receiver options
            elif (self.sor == "Receiver"):
                # Timeout option
                if self.timeout.value == "None":
                    # Set the default value
                    self.timeoutval = None
                else:
                    # Ensure the timeout is a float / integer
                    if (self.timeout.value.replace(".", "", 1).isdigit()):
                        self.timeoutval = float(self.timeout.value)
                    else:
                        npyscreen.notify_wait("Timeout Value must be an integer or float.", title="Timeout Value Error")
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
                        npyscreen.notify_wait("Max Count Value must be an integer.", title="Max Count Value Error")
                        editing = True

                # Interface
                if (self.iface.value == "Default"):
                    # Set the default value
                    self.ifaceval = None
                # Ensure the interface is not blank
                elif (self.iface.value == ""):
                    npyscreen.notify_wait("Interface must not be empty.", title="Interface Value Error")
                    editing = True
                else:
                    self.ifaceval = self.iface.value

                # Input file
                if self.in_file.value is None:
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
                        npyscreen.notify_wait("Input file ({}) does not exist.".format(self.in_file.value), title="Input Filename Error")
                        editing = True
                    # Other file error
                    except FileExistsError:
                        npyscreen.notify_wait("Cannot read input file ({}).".format(self.in_file.value), title="Input Filename Error")
                        editing = True

                # Output message
                if self.out_file.value == "None":
                    # Set the default value
                    self.outfile = None
                # Ensure the output file is not blank
                elif (self.out_file.value == ""):
                    npyscreen.notify_wait("Output Capture must not be empty.", title="Output Filename Value Error")
                    editing = True
                else:
                    # Ensure we can write to the file
                    try:
                        f = open(self.out_file.value, "w")
                        f.write('')
                        f.close()
                        # Set the value
                        self.outfile = self.out_file.value
                    # Other file error
                    except FileExistsError:
                        npyscreen.notify_wait("Cannot write to output capture file ({}).".format(self.out_file.value), title="Output Filename Error")
                        editing = True

                # Output capture
                if (self.out_capture.value == "None"):
                    # Set the default value
                    self.outcapfile = None
                # Ensure the output file is not blank
                elif (self.out_capture.value == ""):
                    npyscreen.notify_wait("Output Capture must not be empty.", title="Output Filename Value Error")
                    editing = True
                else:
                    # Ensure we can write to the file
                    try:
                        f = open(self.out_capture.value, "w")
                        f.write('')
                        f.close()
                        # Set the value
                        self.outcapfile = self.out_capture.value
                    # Other file error
                    except FileExistsError:
                        npyscreen.notify_wait("Cannot write to output capture file ({}).".format(self.out_capture.value), title="Output Filename Error")
                        editing = True

                # Correct values for all parameters
                if not editing:
                    # Notify the user before the message is about to send
                    npyscreen.notify_wait("Listening for the message...", title="Message Status")
                    if (self.outfile):
                        # Save the message
                        m = self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outcapfile)
                        f = open(self.outfile, "w")
                        f.write(m)
                        f.close()
                        # Notify the user the message has been received
                        if self.outcapfile:
                            npyscreen.notify_confirm("Your message has been saved to {} and your capture has been saved to {}. Thank you for using cov3rt!".format(self.outfile, self.outcapfile), title="Message Received Successfully")
                        else:
                            npyscreen.notify_confirm("Your message has been saved to {}. Thank you for using cov3rt!".format(self.outfile), title="Message Received Successfully")
                    else:
                        self.decoded = self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outcapfile)
                        # Notify the user the message has been received
                        if self.outcapfile:
                            npyscreen.notify_confirm("Your capture has been saved to {}. Your secret message is '{}'. Thank you for using cov3rt!".format(self.outcapfile, 
                                ''.join([i 
                                    if i.isprintable() else '\n'
                                    if i == '\n' else '\t'
                                    if i == '\t' else '?'
                                    for i in self.decoded])), title="Message Received Successfully")
                        else:
                            npyscreen.notify_confirm("Your secret message is '{}'. Thank you for using cov3rt!".format(
                                ''.join([i 
                                    if i.isprintable() else '\n'
                                    if i == '\n' else '\t'
                                    if i == '\t' else '?'
                                    for i in self.decoded])), title="Message Received Successfully")
                    self.parentApp.setNextForm(None)
            else:
                npyscreen.notify_wait("You messed up somewhere. Try again.", title="What did you even do?")
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
            if filename not in ["__init__.py", "__pycache__", "Cloak.py"] and filename[-3:] == ".py":
                # Grab the module name
                module_name = package_name + '.' + filename[:-3]
                # Catch general import errors within the cloak files
                try:
                    module = import_module(module_name)
                except:
                    module = ""
                # Module exists
                if module != "":
                    # Get each class name and class in the file
                    for classname, cls in getmembers(module, isclass):
                        # Create the class import path
                        module_path = "{}.{}.{}".format(package_name, classname, classname)
                        # Try-catch for imports that don't follow the standard
                        try:
                            # Get the class object path
                            imprt = str(cls).split("'")[1]
                        except IndexError:
                            imprt = ""
                        # Compare the paths and ignore the "Cloak" import
                        if (module_path == imprt) and (classname != "Cloak"):
                            # Check for the classification
                            if cloaks.get(cls.classification, -1) != -1:
                                # Add to the classification
                                cloaks[cls.classification].append(cls)
                                # Add to the list of cloaks
                                cloak_names.append(cls)

    # Prints a typical help screen for usage information
    def print_help():
        print("""Usage: cov3rt.py [-h] [-l] [-i] (-s | -r) -c cloak_id [Options]
    Primary Arguments:
    -c,  --cloak          Selected covert channel implementation
    -s,  --send           Send information via the selected cloak
    -r,  --receive        Receive information via the selected cloak

    Send Options:
    -m,  --message        Send message within the command-line
    -f,  --filename       Send the contents of a file

    Receive Options:
    -t,  --timeout        Timeout (in seconds) for the packet handler
    -mc, --maxCount       Max number of packets for the packet handler
    -in, --inFile         Use a .cap or .pcap rather than live analysis
    -of, --outFile        Output received message to a file
    -op, --outPcap        Output packets to a capture file (pcap)

    Delays:
    -pd, --packetDelay    Delay between packets
    -dd, --delimitDelay   Delay before each packet delimiter
    -ed, --endDelay       Delay before EOT packet

    Other Arguments:
    -h,  --help           Show this help screen
    -l,  --listCloaks     List available cloaks
    -i,  --interactive    Display an interactive shell for communication
    -if, --iface          Interface for the packet handler
    -d,  --default        Use the default parameters for the cloak
    -v,  --verbose        Increase verbosity
    -vv, --veryVerbose    Further increase verbosity"""
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
    OUTPUT_PCAP = False
    OUTPUT_MESSAGE = False
    TIMEOUT = None
    MAX_COUNT = None
    INTERFACE = None
    INPUT_FILE = None
    DEFAULT = False

    # Hand written parser because argparse sucks
    if ("-h" in argv or "--help" in argv or "?" in argv):
        print_help()
    else:
        # Import Cloaks here for a quicker help screen
        from cov3rt import Cloaks
        from cov3rt import UserCloaks
        
        # Store cloak classifications
        cloaks = {classvar[1]: [] for classvar in getmembers(Cloaks.Cloak.Cloak) if isinstance(classvar[1], str) and classvar[0] != "__module__"}
        # Stores the classname and description of each cloak
        cloak_names = []

        # Add the existing cloaks to our classifications
        add_classes('/'.join(Cloaks.__file__.replace("\\", "/").split('/')[:-1]), "cov3rt.Cloaks")

        # Add user cloaks to our classifications
        add_classes('/'.join(UserCloaks.__file__.replace("\\", "/").split('/')[:-1]), "cov3rt.UserCloaks")

        # Sort the list of cloak names
        cloak_names.sort(key=nameSort)

        # Delete empty classifications
        for empty in [cloak for cloak in cloaks if len(cloaks[cloak]) == 0]:
            del cloaks[empty]

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
            if ("-ed" in argv or "--endDelay" in argv):
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
                # Interface
                if ("-if" in argv or "--iface" in argv):
                    try:
                        index = argv.index("-if")
                    except:
                        index = argv.index("--iface")
                    # Ensure the next positional argument is correct
                    try:
                        INTERFACE = argv[index + 1]
                    # Missing following positional argument
                    except IndexError:
                        error("Missing interface value!")
                        exit()
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
                PCAP_FILENAME = None
                MESSAGE_FILENAME = None
                # Output pcaps to file
                if ("-op" in argv or "--outPcap" in argv):
                    OUTPUT_PCAP = True
                    try:
                        index = argv.index("-op")
                    except:
                        index = argv.index("--outPcap")
                    # Ensure the next positional argument is correct
                    try:
                        PCAP_FILENAME = argv[index + 1]
                        # Ensure we can write to the file
                        try:
                            f = open(PCAP_FILENAME, "w")
                            f.write('')
                            f.close()
                        # Other file error
                        except FileExistsError:
                            error("Error in writing to {}!"
                                  .format(PCAP_FILENAME))
                            exit()
                    # Missing following positional argument
                    except IndexError:
                        error("Missing output packet capture filename!")
                        exit()
                # Output message to file
                if ("-of" in argv or "--outFile" in argv):
                    OUTPUT_MESSAGE = True
                    try:
                        index = argv.index("-of")
                    except:
                        index = argv.index("--outFile")
                    # Ensure the next positional argument is correct
                    try:
                        MESSAGE_FILENAME = argv[index + 1]
                        # Ensure we can write to the file
                        try:
                            f = open(MESSAGE_FILENAME, "w")
                            f.write('')
                            f.close()
                        # Other file error
                        except FileExistsError:
                            error("Error in writing to {}!"
                                  .format(MESSAGE_FILENAME))
                            exit()
                    # Missing following positional argument
                    except IndexError:
                        error("Missing output message filename!")
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
                        INTERFACE = argv[index + 1]
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

            # Send / Receive not selected
            else:
                error("Please specify send/receive!")
                exit()

            # Setup the sending mechanism
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
                            try:
                                setattr(cloak, p, str(new_val))
                            except ValueError as err:
                                error(err)
                                exit()
                            except TypeError as err:
                                error(err)
                                exit()
                        # Integer parameter
                        elif isinstance(parameters[p].default, int):
                            if new_val.isdigit():
                                try:
                                    setattr(cloak, p, int(new_val))
                                except ValueError as err:
                                    error(err)
                                    exit()
                                except TypeError as err:
                                    error(err)
                                    exit()
                            else:
                                error("{} must be of type 'int'!"
                                      .format(new_val))
                                exit()
                        # Float parameter
                        elif isinstance(parameters[p].default, float):
                            if new_val.replace('.', '', 1).isdigit():
                                try:
                                    setattr(cloak, p, float(new_val))
                                except ValueError as err:
                                    error(err)
                                    exit()
                                except TypeError as err:
                                    error(err)
                                    exit()
                            else:
                                error("{} must be of type 'float'!".format(new_val))
                                exit()
            if SENDING:
                # Ingest data
                cloak.ingest(message)
                # Send packets
                cloak.send_packets(INTERFACE, PACKET_DELAY, DELIMITER_DELAY, END_DELAY)
                print(INTERFACE)
            elif RECEIVING:
                # Receive packets
                if OUTPUT_PCAP:
                    cloak.recv_packets(TIMEOUT, MAX_COUNT, INTERFACE, INPUT_FILE, PCAP_FILENAME)
                else:
                    m = cloak.recv_packets(TIMEOUT, MAX_COUNT, INTERFACE, INPUT_FILE, PCAP_FILENAME)
                    # Output to file
                    if OUTPUT_MESSAGE:
                        f = open(MESSAGE_FILENAME, "w")
                        f.write(m)
                        f.close()
                    # Simply print message
                    else:
                        print(''.join([i 
                            if i.isprintable() else '\n'
                            if i == '\n' else '\t'
                            if i == '\t' else '?'
                            for i in m]))
