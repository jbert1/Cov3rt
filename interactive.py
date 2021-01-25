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


# This is my idea for storing cloak classifications
cloaks = {
    "Inter-Packet Timing" : [
        "DNSTiming"
    ], 
    "Random Value" : [
        "IPv6Hoppers",
        "TCP"
    ], 
    "Reserved or Unreserved" : [
        "IP"
    ], 
    "Size Modulation" : [
        "UDPRaw"
    ], 
    "Value Modulation" : [
        "DNSCaseModulation"
    ]
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
class HomePage(npyscreen.ActionForm):

    # Defines the elements on the page
    def create(self):
        # Header
        self.header1 = self.add(npyscreen.FixedText, relx = 20, color = "DANGER", editable = False,
            value = "                 ╭───╮       │"
        )
        self.header2 = self.add(npyscreen.FixedText, relx = 20, color = "DANGER", editable = False,
            value = "                     │      ─┼─╴"
        )
        self.header3 = self.add(npyscreen.FixedText, relx = 20, color = "DANGER", editable = False,
            value = "╭─── ╭───╮ ╮   ╭  ───┤ ╭───╮ │"
        )
        self.header4 = self.add(npyscreen.FixedText, relx = 20, color = "DANGER", editable = False,
            value = "│    │   │ ╰╮ ╭╯     │ │     │"
        )
        self.header5 = self.add(npyscreen.FixedText, relx = 20, color = "DANGER", editable = False,
            value = "╰─── ╰───╯  ╰─╯  ╰───╯ ╵     ╰╴"
        )
        self.nextrely += 2
        # List of cloaks
        self.cloak_classification = self.add(npyscreen.TitleSelectOne, scroll_exit = True, begin_entry_at = 25, max_height = 7,
            name = "Cloak Classifications:", 
            values = list(cloaks.keys())
        )

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
                     │      ─┼─╴  
╭─── ╭───╮ ╮   ╭  ───┤ ╭───╮ │    
│    │   │ ╰╮ ╭╯     │ │     │  
╰─── ╰───╯  ╰─╯  ╰───╯ ╵     ╰╴  
""")