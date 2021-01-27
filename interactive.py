#!/usr/bin/env python
# encoding: utf-8

import npyscreen

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

# Classification encoding
INTER_PACKET_TIMING = ("Inter-Packet Timing", 0)
MESSAGE_TIMING = ("Message Timing", 1)
RATE_THROUGHPUT_TIMING = ("Rate/Throughput", 2)
ARTIFICIAL_LOSS = ("Artificial Loss", 3)
MESSAGE_ORDERING = ("Message (PDU) Ordering", 4)
RETRANSMISSION = ("Retransmission", 5)
FRAME_COLLISIONS = ("Frame Collisions", 6)
TEMPERATURE = ("Temperature", 7)
SIZE_MODULATION = ("Size Modulation", 8)
POSITION = ("Sequence: Position", 9)
NUMBER_OF_ELEMENTS = ("Sequence: Number of Elements", 10)
RANDOM_VALUE = ("Random Value", 11)
CASE_MODULATION = ("Value Modulation: Case", 12)
LSB_MODULATION = ("Value Modulation: LSB", 13)
VALUE_INFLUENCING = ("Value Modulation: Value Influencing", 14)
RESERVED_UNUSED = ("Reserved/Unused", 15)
PAYLOAD_FIELD_SIZE_MODULATION = ("Payload Field Size Modulation", 16)
USER_DATA_CORRUPTION = ("User-Data Corruption", 17)
MODIFY_REDUNDANCY = ("Modify Redundancy", 18)
USER_DATA_VALUE_MODULATION_RESERVED_UNUSED = ("User-Data Value Modulation & Reserved/Unused", 19) 


# This is my idea for storing cloak classifications
cloaks =  {
    "Inter-Packet Timing" : [
        "DNSTiming",
    ],

    "Message Timing" : [
    ],

    "Rate/Throughput" : [
    ],

    "Artificial Loss" : [
    ],

    "Message (PDU) Ordering" : [
    ],

    "Retransmission" : [
    ],

    "Frame Collisions" : [
    ],
    
    "Temperature" : [
    ],

    "Size Modulation" : [
        "UDPRaw",
    ],

    "Sequence: Position" : [
    ],

    "Sequence: Number of Elements" : [
    ],

    "Random Value" : [
        "IPv6Hoppers","TCP",
    ],

    "Value Modulation: Case" : [
        "DNSCaseModulation"
    ],

    "Value Modulation: LSB" : [
    ],
    
    "Value Modulation: Value Influencing" : [
    ],

    "Reserved or Unused" : [
        "IPReservedBit"
    ],
    
    "Payload Field Size Modulation" : [
    ],

    "User-Data Corruption" : [
    ],

    "Modify Redundancy" : [
    ],

    "User-Data Value Modulation & Reserved/Unused" : [
    ],
}


# Main application
class App(npyscreen.NPSAppManaged):

    def onStart(self):
        self.addForm("MAIN", 
            HomePage, 
            name = "Welcome to cov3rt",
            lines = 20,
            columns = 80
        )
        self.addForm("CloakSelection",
            Second_TUI,
            name = "Cloak Selection",
            lines = 20,
            columns = 80
        )

# Main page for our interactive application
class HomePage(npyscreen.ActionForm, npyscreen.FormWithMenus):

    # Defines the elements on the page
    def create(self):
        # Header
        self.header = self.add(npyscreen.Pager, relx = 20, color = "DANGER", editable = False, height = 6,
            values = [
                "                 ╭───╮       │",
                "           ╱╲_╱╲     │      ─┼──",
                "╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │  ",
                "│    │   │  ╲_╱      │ │     │  ",
                "╰─── ╰───╯   ╳   ╰───╯ ╵     ╰──"
            ]

        )
        self.nextrely += 2
        # List of cloaks
        self.cloak_classification = self.add(npyscreen.TitleSelectOne, scroll_exit = True, begin_entry_at = 25, max_height = 7,
            name = "Cloak Classifications:", 
            values = list(cloaks.keys())
        )
        
        self.menu = self.new_menu(name = "Cloak Selection",
            shortcut = 'm'
        )
        self.menu.addItem("Item 1", self.press_1, "1")
        self.menu.addItem("Item 2", self.press_2, "2")
        self.menu.addItem("Close Menu", self.close_menu, "^X")
        
        for cloak_name in cloaks:
            with self.menu.addNewSubmenu(cloak_name) as submenu:
                for cloak in cloaks[cloak_name]:
                    submenu.addItem(cloak.name, cloak_options_next_page(cloak))
        
        def cloak_options_next_page(self, cloak):
            pass


        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu = self.menu.addNewSubmenu("A sub menu!", 's')
        # self.submenu10 = self.menu.addNewSubmenu("A sub menu!", 's')

        self.populate(self.submenu10)

        self.submenu.addItem("Close Menu", self.close_menu, "^X")

    def populate(self, submenu):
        for 
        submenu.addItem()

    def press_1(self):
        npyscreen.notify_confirm("You pressed Item 1!", "Item 1", editw=1)
    def press_2(self):
        npyscreen.notify_confirm("You pressed Item 2!", "Item 2", editw=1)
    def close_menu(self):
        self.parentApp.setNextForm(None)

    # Runs when the user completes the form
    def on_ok(self):
        # Ensure correct number is selected
        if len(self.cloak_classification.value) == 1:
            # Pass it to the Secondary form
            self.parentApp.getForm("CloakSelection").cloak_classification.value = self.cloak_classification.values[self.cloak_classification.value[0]]
            self.parentApp.switchForm("CloakSelection")
        # No element selected
        elif len(self.cloak_classification.value) == 0:
            npyscreen.notify_wait("Please select one of the cloaks before proceeding.", "Invalid Cloak", "DANGER")
        # More than one selected (How did you even do that?)
        else:
            npyscreen.notify_wait("Please select a single cloak before proceeding.", "Invalid Cloak", "DANGER", wide = True)

    # Runs when the user cancels the form
    def on_cancel(self):
        # Exit
        self.parentApp.setNextForm(None)


class Second_TUI(npyscreen.ActionForm):
    
    # Defines the elements on the page
    def create(self):
        self.cloak_classification = self.add(npyscreen.TitleFixedText, begin_entry_at = 30, editable = False, color="LABELBOLD",
            name = "Selected Classification:"
        )
        self.nextrely += 1
        self.cloak_type = self.add(npyscreen.TitleSelectOne, scroll_exit = True, begin_entry_at = 30, max_height = 7,
            name = "Cloak Types:", 
            values = []
        )
    
    def while_editing(self):
        self.cloak_type.values = cloaks[self.cloak_classification.value] if (cloaks.get(self.cloak_classification.value, -1) != -1) else ["Could not load Cloaks!"]

    # Runs when the user finishes the form
    def afterEditing(self):
        # Exit
        self.parentApp.setNextForm(None)
    

# Main program
if __name__ == '__main__':
    app = App().run()
    print("""
                 ╭───╮       │
           ╱╲_╱╲     │      ─┼──
╭─── ╭───╮ ╲╷ ╷╱  ───┤ ╭───╮ │  
│    │   │  ╲_╱      │ │     │  
╰─── ╰───╯   ╳   ╰───╯ ╵     ╰──
""")