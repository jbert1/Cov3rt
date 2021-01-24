#!/usr/bin/env python
# encoding: utf-8

import npyscreen


class cov3rtApp(npyscreen.NPSAppManaged):

    def onStart(self):
        self.addForm("MAIN", Start_TUI, name = "Welcome to cov3rt")
        self.addForm("Secondary", Second_TUI, name = "Welcome to cov3rt")
        self.addForm("Third", Third_TUI, name = "Welcome to cov3rt")

class Start_TUI(npyscreen.ActionForm):

    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Secondary")

    def create(self):
        self.pick_cloak = self.add(npyscreen.TitleSelectOne, values = ["Inter-Packet Timing", "Random Value", "Reserved or Unreserved", "Size Modulation", "Value Modulation"], name = "Pick a category of Cloak", scroll_exit = True)
    
    def on_ok(self):
        toSecond = self.parentApp.getForm("Secondary")
        toSecond.pick_cloak.value = self.pick_cloak.values[self.pick_cloak.value[0]]
        self.parentApp.switchForm("Secondary")

class Second_TUI(npyscreen.Form):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Third")

    
    def create(self):
        self.pick_cloak = self.add(npyscreen.TitleFixedText, name = "You Chose")
    
    



if __name__ == '__main__':
    npyscreen.wrapper(cov3rtApp().run())
