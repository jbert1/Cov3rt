#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from importlib import import_module
from inspect import getmembers, isclass
from logging import error
from os import listdir
from os import name as OS_NAME
from cov3rt.Cloaks import Cloak
from cov3rt import Cloaks
from inspect import signature 

### TEST CODE (Mainly kept for quick reference) ###
# class ActionFormObject(npyscreen.ActionForm, npyscreen.FormWithMenus):
#     def create(self):
#         self.add(npyscreen.TitleText, 
#             name = "TitleText1", 
#             hidden = False, 
#             begin_entry_at = 20,
#             value=str(vars(self))
#         )
#         self.nextrely += 1
#         self.add(npyscreen.TitleText, 
#             name = "TitleText2", 
#             hidden = False, 
#             begin_entry_at = 20,
#             value=str(vars(self))
#         )

#         self.menu = self.new_menu(name = "Main Menu",
#             shortcut = 'm'
#         )
#         self.menu.addItem("Item 1", self.press_1, "1")
#         self.menu.addItem("Item 2", self.press_2, "2")
#         self.menu.addItem("Close Menu", self.close_menu, "^X")
#         self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
#         self.submenu.addItem("Close Menu", self.close_menu, "^X")
        

#     def press_1(self):
#         npyscreen.notify_confirm("You pressed Item 1!", "Item 1", editw=1)
#     def press_2(self):
#         npyscreen.notify_confirm("You pressed Item 2!", "Item 2", editw=1)
#     def close_menu(self):
#         self.parentApp.setNextForm(None)

#     def on_ok(self):
#         npyscreen.notify_confirm("OK button pressed", "OK Button", wide = True, editw = 1)
#         self.parentApp.setNextForm(None)
    
#     def on_cancel(self):
#         exiting = npyscreen.notify_yes_no("Are you sure you want to cancel?", "Exit")
#         if exiting:
#             self.parentApp.setNextForm(None)

#     def afterEditing(self):
#         pass
#         # self.parentApp.setNextForm(None)

# class SplitFormObject(npyscreen.SplitForm):
    
#     def create(self):
#         t1 = self.add(npyscreen.TitleText, 
#             name = "TitleText1", 
#             hidden = False, 
#             begin_entry_at = 20,
#             value=str(vars(self))
#         )
#         self.nextrely += 1
#         t2 = self.add(npyscreen.TitleText, 
#             name = "TitleText2", 
#             hidden = False, 
#             begin_entry_at = 20,
#             value=str(vars(self))
#         )

#     def afterEditing(self):
#         # pass
#         self.parentApp.setNextForm(None)

# class App(npyscreen.NPSAppManaged):
#     def onStart(self):
#         self.addForm("MAIN", 
#             ActionFormObject, 
#             name = "npyscreen Form!"
#             # lines=10,
#             # columns=40,
#             # draw_line_at = 3
#         )


# if __name__ == "__main__":
#     app = App().run()


# This is my idea for storing cloak classifications
cloaks =  {
    Cloak.INTER_PACKET_TIMING : [
    ],

    Cloak.MESSAGE_TIMING : [
    ],

    Cloak.RATE_THROUGHPUT_TIMING : [
    ],

    Cloak.ARTIFICIAL_LOSS : [
    ],

    Cloak.MESSAGE_ORDERING : [
    ],

    Cloak.RETRANSMISSION : [
    ],

    Cloak.FRAME_COLLISIONS : [
    ],
    
    Cloak.TEMPERATURE : [
    ],

    Cloak.SIZE_MODULATION : [
    ],

    Cloak.POSITION : [
    ],

    Cloak.NUMBER_OF_ELEMENTS : [
    ],

    Cloak.RANDOM_VALUE : [
    ],

    Cloak.CASE_MODULATION : [
    ],

    Cloak.LSB_MODULATION : [
    ],
    
    Cloak.VALUE_INFLUENCING : [
    ],

    Cloak.RESERVED_UNUSED : [
    ],
    
    Cloak.PAYLOAD_FIELD_SIZE_MODULATION : [
    ],

    Cloak.USER_DATA_CORRUPTION : [
    ],

    Cloak.MODIFY_REDUNDANCY : [
    ],

    Cloak.USER_DATA_VALUE_MODULATION_RESERVED_UNUSED : [
    ],
}

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
                except:
                    pass

# Main application
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
        self.addForm("Communications",
            Third_TUI,
            name = "Sender and Receiver Options",
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
        # Exit Choice
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            npyscreen.notify_confirm("Thank you for using cov3rt!")
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
        self.cloak_description = self.add(npyscreen.TitlePager, relx = 5, begin_entry_at = 18, editable = False, height = 2,
            name = "Description:",
            values = ["Press CTRL+X to open the menu."]
        )

    # Populates the screen
    def populateScreen(self):
        self.instance = self.cloak()
        
        self.a = []
        self.a_margin = 0
        parameters = dict(signature(self.instance.__init__).parameters)
        self.nextrely += 1

        for p in parameters:
            self.a.append(self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18, name = p, value = str(parameters[p].default)))
            self.a_margin += 1
        
        self.nextrely += 1
        
        self.send_or_recv = self.add(npyscreen.TitleSelectOne, relx = 5, begin_entry_at = 18, scroll_exit = True, height = 2,
            name = "Sender/Receiver",
            values = ["Sender", "Receiver"]
        )
        
        # Populate on-screen items
        self.cloak_classification.value = self.cloak.classification
        self.cloak_name.value = self.cloak.name
        self.cloak_description.values = self.cloak.description.split("\n")
        

    def on_ok(self):
        
        if (len(self.send_or_recv.value) == 0):
            npyscreen.notify_wait("Please pick Sender or Receiver.", "Sender or Receiver", "DANGER")
        else:
            

            #TODO: Sanitize Inputs to Fit REGEX/ Datatypes and restore keys in original dictionary
            editing = False
            for element in self.a:
                p = element.name
                new_val = element.value
                parameters = dict(signature(self.instance.__init__).parameters)
                # String parameter
                if isinstance(parameters[p].default, str):
                    try:
                        exec("self.instance.{} = '{}'".format(p, new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
                # Integer parameter
                elif isinstance(parameters[p].default, int):
                    try:
                        exec("self.instance.{} = int({})".format(p, new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
                # Float parameter
                elif isinstance(parameters[p].default, int):
                    try:
                        exec("self.instance.{} = float({})".format(p, new_val))
                    except ValueError as err:
                        npyscreen.notify_wait(str(err), title = "Value Error!")
                        editing = True
                    except TypeError as err:
                        npyscreen.notify_wait(str(err), title = "Type Error!")
                        editing = True
            
            if not (editing):
                toSor = self.parentApp.getForm("Communications")
                toSor.sor = self.send_or_recv.values[self.send_or_recv.value[0]]
                toSor.cloak = self.instance
                toSor.cloak_name.value = self.instance.name
                toSor.populateScreen()
                self.parentApp.setNextForm("Communications")

    def on_cancel(self):
        # Exit Choice
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            npyscreen.notify_confirm("Thank you for using cov3rt!")
            self.parentApp.setNextForm(None)
        


        ### On_cancel return to previous screen
        # back_choice = npyscreen.notify_yes_no("Choose a different Cloak?")
        # if back_choice:
        #     npyscreen.notify_wait("Returning to Cloak Selection", title = "Cloak Selection Cancelled")
        #     for i in self.a:
        #         i.hidden = True
        #     self.a = []
        #     self.parentApp.setNextForm("MAIN")



class Third_TUI(npyscreen.ActionForm):
    
    # Defines the elements on the page
    def create(self):

        # Classification, name, and description
        self.cloak_name = self.add(npyscreen.TitleFixedText, relx = 5, begin_entry_at = 18, editable = False,
            name = "Cloak: "
        )

    # Populates the screen
    def populateScreen(self):
        self.a = []
        self.a_margin = 0
        if (self.sor == "Sender"):
            self.nextrely += 1
            self.whattosend = self.add(npyscreen.TitleSelectOne, relx = 5, begin_entry_at = 18, scroll_exit = True, height = 2,
                name = "Message Type:",
                values = ["File Input", "Text Input"]
            )
            self.nextrely += 1
            self.filename = self.add(npyscreen.TitleFilenameCombo, relx = 5, begin_entry_at = 18,
                name="Filename:", label=True
            )
            self.inputtext = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Text Input:", value = ""
            )
            self.filename.hidden = True
            self.inputtext.hidden = True
        else:
            self.timeout = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Timeout:",
                value = "None"
            )
            self.maxcount = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Max Count:",
                value = "∞"
            )
            self.iface = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Interface:",
                value = "eth0" if OS_NAME != "nt" else "Wi-Fi"
            )
            self.in_file = self.add(npyscreen.TitleFilenameCombo, relx = 5, begin_entry_at = 18,
                name="Filename:", label=True
            )
            self.out_file = self.add(npyscreen.TitleText, relx = 5, begin_entry_at = 18,
                name = "Output File:",
                value = "None"
            )
            
            
    def selectFilename(self):
        self.filename.hidden = False
        self.inputtext.hidden = True
    
    def selectText(self):
        self.inputtext.hidden = False
        self.filename.hidden = True

    def on_ok(self):
        editing = False
        
        if (self.sor == "Sender"):
            
            
            if not (editing):
                pass
        
        
        else:
            
            # Timeout
            if (self.timeout.value == "None"):
                self.timeoutval = None
            else:
                if (self.timeout.value.replace(".", "", 1).isdigit()):
                    self.timeoutval = float(self.timeout.value)
                else:
                    npyscreen.notify_wait("Timeout Value must be an integer or float.", title = "Timeout Value Error")
                    editing = True
            
            # Max Count
            if (self.maxcount.value == "∞"):
                self.maxcountval = None
            else:
                if (self.maxcount.value.isdigit()):
                    self.maxcountval = int(self.maxcount.value)
                else:
                    npyscreen.notify_wait("Max Count Value must be an integer.", title = "Max Count Value Error")
                    editing = True
            
            # Interface
            if (self.iface.value == "eth0" or self.iface.value == "Wi-Fi"):
                self.ifaceval = "eth0" if self.iface.value == "eth0" else "Wi-Fi"
            elif (self.iface.value == ""):
                npyscreen.notify_wait("Interface must not be empty.", title = "Interface Value Error")
                editing = True
            else:
                self.ifaceval = self.iface.value
            
            # Input file
            if (self.in_file.value == None):
                self.infileval = None
            else:
                # Ensure we can read the file
                try:
                    f = open(self.in_file.value, "r")
                    f.close()
                    self.infileval = self.in_file.value
                # Other file error
                except FileNotFoundError:
                    npyscreen.notify_wait("Input file ({}) does not exist.".format(self.in_file.value), title = "Input Filename Error")
                    editing = True
                # Other file error
                except FileExistsError:
                    npyscreen.notify_wait("Cannot read input file ({}).".format(self.in_file.value), title = "Input Filename Error")
                    editing = True
                

            # Output file
            if (self.out_file.value == "None"):
                self.outfileval = None
            elif (self.out_file.value == ""):
                npyscreen.notify_wait("Output Filename must not be empty.", title = "Output Filename Value Error")
                editing = True
            else:
                # Ensure we can write to the file
                try:
                    f = open(self.out_file.value, "w")
                    f.write('')
                    f.close()
                    self.outfileval = self.out_file.value
                # Other file error
                except FileExistsError:
                    npyscreen.notify_wait("Cannot write to output file ({}).".format(self.out_file.value), title = "Output Filename Error")
                    editing = True



            if not (editing):
                if (self.outfileval):
                    self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outfileval)
                else:
                    print(self.cloak.recv_packets(self.timeoutval, self.maxcountval, self.ifaceval, self.infileval, self.outfileval))
                

        self.parentApp.setNextForm(None)

    def on_cancel(self):
        # Exit Choice
        exit_choice = npyscreen.notify_yes_no("Are you sure you want to exit cov3rt?")
        if exit_choice:
            npyscreen.notify_confirm("Thank you for using cov3rt!")
            self.parentApp.setNextForm(None)
        
        
        ### On_cancel return to previous screen
        # back_choice = npyscreen.notify_yes_no("Choose a different Cloak?")
        # if back_choice:
        #     npyscreen.notify_wait("Returning to Cloak Selection", title = "Cloak Selection Cancelled")
        #     for i in self.a:
        #         i.hidden = True
        #     self.a = []
        #     self.parentApp.setNextForm("MAIN")

    # Runs when the user finishes the form
    def afterEditing(self):
        #Exit
        # self.parentApp.setNextForm(None)
        pass
    


# Main program
if __name__ == '__main__':

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
    app = App().run()
    