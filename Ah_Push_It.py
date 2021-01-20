#!/usr/bin/env python
# encoding: utf-8

import npyscreen


class cov3rtApp(npyscreen.NPSAppManaged):

    def main(self):
        self.registerForm("Initial", Start_TUI)
        self.registerForm("Secondary", Second_TUI)

class Start_TUI(npyscreen.ActionForm):

    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Secondary")

    def create(self):
        self.pick_cloak = self.add(npyscreen.TitleSelectOne, values = ["Inter-Packet Timing", "Random Value", "Reserved or Unreserved", "Size Modulation", "Value Modulation"], name = "Pick a category of Cloak")
    
    def on_ok(self):
        carryover = self.parentApp.getForm("Secondary")
        carryover.pick_cloak.value = self.pick_cloak.values[self.pick_cloak.value[0]]
        self.parentApp.switchForm("Secondary")

class Second_TUI(npyscreen.Form):
    def activate(self):
        self.edit()
    
    def create(self):
        self.pick_cloak = self.add(npyscreen.TitleFixedText, name = "You chose")


if __name__ == "__main__":
    cov3rt = cov3rtApp()
    cov3rt.run()
