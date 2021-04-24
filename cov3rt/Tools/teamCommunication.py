# This file is part of the cov3rt project
# Copyright (C) 2021 Justin Berthelot, Samuel Dominguez, Daniel Munger, Christopher Rice

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from threading import Thread
import curses
from cov3rt.Cloaks import UDPSizeModulation
from sys import argv
from re import search
from psutil import net_if_stats

# Cloaks
recvcloak = UDPSizeModulation()
sendcloak = UDPSizeModulation()
# Regular expression to verify IP
IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    
# Field class
class Field(object):

    # Constants
    NOTHING = 0
    CURSOR_A = 1
    CURSOR_R = 2
    FIELD = 3
    FUNCTION = 4

    BASIC = 0
    INPUT = 1
    BOARD = 2

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    TAB = 4
    ENTER = 5
    SPACE = 6
    BACKTAB = 7

    # Constructor
    def __init__(self, screen, x1, x2, y1, y2, fieldtype=0):

        # Ignore errors or display them
        self.errorhandle = True

        self.left_argtype = self.NOTHING
        self.right_argtype = self.NOTHING
        self.up_argtype = self.NOTHING
        self.down_argtype = self.NOTHING
        self.tab_argtype = self.NOTHING
        self.enter_argtype = self.NOTHING
        self.space_argtype = self.NOTHING
        self.backtab_argtype = self.NOTHING
        self.selected = False

        # Check screen type
        if str(type(screen)) == "<class '_curses.window'>":
            self.screen = screen
        else:
            print(type(screen))
            raise TypeError("'screen' must be a curses window")

        # Get max values
        self._MAX_Y, self._MAX_X = screen.getmaxyx()

        # Size of field (x)
        if (isinstance(x1, int) and isinstance(x2, int)):
            # Bound size
            if ((x1 >= 0 and x1 < self.MAX_X) and
                    (x2 >= 0 and x2 < self.MAX_X)):
                # Make sure x1 <= x2
                if x1 <= x2:
                    self.x1 = x1
                    self.x2 = x2
                else:
                    raise TypeError("'x1' must be less than 'x2'")
            else:
                raise ValueError("'x' must be between {} -> {}".format(0, self.MAX_X))
        else:
            raise TypeError("'x' must be of type 'int'")

        # Size of field (y)
        if (isinstance(y1, int) and isinstance(y2, int)):
            # Bound size
            if ((y1 >= 0 and y1 < self.MAX_Y) and
                    (y2 >= 0 and y2 < self.MAX_Y)):
                # Make sure y1 <= y2
                if y1 <= y2:
                    self.y1 = y1
                    self.y2 = y2
                else:
                    raise TypeError("'y1' must be less than 'x2'")
            else:
                raise ValueError("'y' must be between {} -> {}".format(0, self.MAX_Y))
        else:
            raise TypeError("'y' must be of type 'int'")

        # Field type
        if isinstance(fieldtype, int):
            self.fieldtype = fieldtype
        else:
            raise TypeError("'fieldtype' must be of type 'int'")

        # Basic field
        if fieldtype == self.BASIC:
            # Selected coordinates
            self.selected_x = x1
            self.selected_y = y1
        # Text Input field
        elif fieldtype == self.INPUT:
            # Selected coordinates
            self.selected_x = x1
            self.selected_y = y1
            self.cursor_x = x1
            self.cursor_y = y1
        # Special fieldtype for this specific program
        elif fieldtype == self.BOARD:
            # Initialized list
            self.board_size = 13
            self.board_data = []
            # Selected coordinates
            self.selected_x = x1
            self.selected_y = y1

    # FUNCTIONS

    # Select the current field
    def select(self):
        # Loop over y's
        for y in range(self.y1, self.y2 + 1):
            # Get the old line
            try:
                # Try ascii
                string = self.screen.instr(y, self.x1, self.x2 - self.x1 + 1).decode("ascii")
            except UnicodeDecodeError:
                # Curses hates unicode, so we have to go character by character
                string = ""
                for x in range(self.x1, self.x2 + 1):
                    try:
                        char = chr(eval("0b{}".format(str(bin(self.screen.inch(y, x)))[-14:])))
                        string += char
                    except Exception as e:
                        string += ""
            if self.fieldtype == self.INPUT:
                self.screen.addstr(y, self.x1, string, curses.A_BOLD)
                # Grab the cursor character
                char = chr(eval("0b{}".format(str(bin(self.screen.inch(y, self.cursor_x)))[-14:])))
                # Add it with the defined color
                self.screen.addstr(y, self.cursor_x, char, curses.A_UNDERLINE)
            else:
                self.screen.addstr(y, self.x1, string, curses.A_BOLD)
        self.screen.move(self.selected_y, self.selected_x)
        self.selected = True

    # Unselect the current field
    def deselect(self):
        # Loop over y's
        for y in range(self.y1, self.y2 + 1):
            if (self.fieldtype == self.BASIC or self.fieldtype == self.INPUT):
                # Get the old line
                try:
                    # Try ascii
                    string = self.screen.instr(y, self.x1, self.x2 - self.x1 + 1).decode("ascii")
                except UnicodeDecodeError:
                    # Curses hates unicode, so we have to go character by
                    #  character
                    string = ""
                    for x in range(self.x1, self.x2 + 1):
                        try:
                            char = chr(
                                eval("0b{}".format(str(bin(self.screen.inch(y, x)))[-14:])))
                            string += char
                        except Exception as e:
                            string += ""
                # Add it back with the defined color
                if self.fieldtype == self.INPUT:
                    self.screen.addstr(y, self.x1, string)
                else:
                    self.screen.addstr(y, self.x1, string)
        self.screen.move(self.selected_y, self.selected_x)
        self.selected = False

    # Set text of the field
    def settext(self, string, xstart, ystart):
        # Type checks
        if isinstance(xstart, int) and isinstance(ystart, int) and isinstance(string, str):
            # Bound size
            if xstart >= self.x1 and (len(string) + xstart) <= (self.x2 + 1) and (ystart >= self.y1 or ystart <= self.y2):
                # Add text with the defined color
                self.screen.addstr(ystart, xstart, string)
            else:
                raise ValueError("'string' length must be between {} -> {}".format(self.x1, self.x2))
        else:
            raise TypeError("TypeError")

    # Handle the board field
    def updateboard(self, string):
        if len(self.board_data) < self.board_size:
            self.board_data.append(string.ljust(95))
            self.settext(string.ljust(95), self.x1 + 1, len(self.board_data) + 1)
        else:
            self.board_data = self.board_data[1:]
            self.board_data.append(string.ljust(95))
            for b in range(len(self.board_data)):
                self.settext(self.board_data[b], self.x1 + 1, b + 2)

    # Add text to the input
    def addtext(self, char, loop=False):
        # Type check
        if isinstance(char, str):
            # Input field type
            if self.fieldtype == self.INPUT:
                # Add character
                self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_BOLD)
                self.cursor_x += 1
                # End of field
                if self.cursor_x > self.x2:
                    # Loop check
                    if loop:
                        # Go to the next line
                        self.cursor_x = self.x1
                        if (self.cursor_y + 1) <= self.y2:
                            self.cursor_y += 1
                    else:
                        # Move back one
                        self.cursor_x -= 1
                # Grab the old character
                char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
                # Add it back with the selected color
                self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_UNDERLINE)
                # Move the cursor
                self.screen.move(self.cursor_y, self.cursor_x)
        else:
            raise TypeError("TypeError")
        self.selected_x = self.cursor_x

    # Clear the text in the input
    def cleartext(self):
        self.screen.addstr(self.y1, self.x1, " " * (self.x2 - self.x1 + 1), curses.A_BOLD)

    # Return the text in the input field
    def returntext(self):
        # Get the old line
        string = self.screen.instr(self.y1, self.x1, self.x2 - self.x1 + 1).decode("utf-8").strip()
        return string

    # Simulate the press of the backspace key
    def backspacetext(self, ctrl=False):
        # Check location of cursor
        if self.cursor_x != self.x1:
            if ctrl:
                # Grab the old characters
                string = self.screen.instr(self.cursor_y, self.cursor_x, (self.x2 - self.cursor_x + 1)).decode()
                # Add the required spaces
                string += " " * (self.cursor_x - self.x1)
                # Add it back with the deselected color
                self.screen.addstr(self.cursor_y, self.x1, string)
                # Move cursor back one
                self.cursor_x = self.x1
            else:
                # Grab the old characters
                string = self.screen.instr(self.cursor_y, self.cursor_x, (self.x2 - self.cursor_x + 1)).decode() + " "
                # Add it back with the deselected color
                self.screen.addstr(self.cursor_y, self.cursor_x-1, string)
                # Move cursor back one
                self.cursor_x -= 1
            # Grab the new character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the selected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_UNDERLINE)
            self.screen.move(self.cursor_y, self.cursor_x)
            self.selected_x = self.cursor_x

    # Simulate the press of the delete key
    def deletetext(self, ctrl=False):
        if ctrl:
            # Add the required spaces
            string = " " * (self.x2 - self.cursor_x + 1)
            # Add it back with the deselected color
            self.screen.addstr(self.cursor_y, self.cursor_x, string)
        else:
            # Grab the old characters
            string = self.screen.instr(self.cursor_y, self.cursor_x + 1, (self.x2 - self.cursor_x + 1)).decode()
            # Add it back with the deselected color
            self.screen.addstr(self.cursor_y, self.cursor_x, string)
        # Grab the new character
        char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
        # Add it back with the selected color
        self.screen.addstr(self.cursor_y, self.cursor_x, char[0],  curses.A_UNDERLINE)
        self.screen.move(self.cursor_y, self.cursor_x)
        self.selected_x = self.cursor_x

    # Move the input cursor on the row
    def moveinputcursor(self, x, throwerror=False):
        # Bound size
        if ((x <= 0) and (self.cursor_x + x >= self.x1)) or ((x > 0) and (self.cursor_x + x <= self.x2)):
            # Grab the old character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the deselected color
            self.screen.addstr(self.cursor_y, self.cursor_x,
                               char[0], curses.A_BOLD)
            # Get new cursorx location
            self.cursor_x = x + self.cursor_x
            # Grab the new character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the selected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_UNDERLINE)
            # Move the cursor
            self.screen.move(self.cursor_y, self.cursor_x)
        elif (x <= 0):
            # Grab the old character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the deselected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_BOLD)
            # Get new cursorx location
            self.cursor_x = self.x1
            # Grab the new character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the selected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_UNDERLINE)
            # Move the cursor
            self.screen.move(self.cursor_y, self.cursor_x)
        elif (x > 0):
            # Grab the old character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the deselected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_BOLD)
            # Get new cursorx location
            self.cursor_x = self.x2
            # Grab the new character
            char = self.screen.instr(self.cursor_y, self.cursor_x, 1).decode()
            # Add it back with the selected color
            self.screen.addstr(self.cursor_y, self.cursor_x, char[0], curses.A_UNDERLINE)
            # Move the cursor
            self.screen.move(self.cursor_y, self.cursor_x)
        # Throw an error if we say so
        elif throwerror:
            raise ValueError("'x' must be between {} -> {}".format(self.x1 - self.cursor_x, self.x2 - self.cursor_x))
        self.selected_x = self.cursor_x

    # Execute the argument type with the direction
    def execute(self, argtype, d):
        if argtype == self.NOTHING:
            pass
        elif (argtype == self.CURSOR_A or argtype == self.CURSOR_R):
            # INPUT field type
            if self.fieldtype == self.INPUT:
                if d == self.LEFT:
                    self.cursor_x = self.leftx
                    self.cursor_y = self.lefty
                elif d == self.RIGHT:
                    self.cursor_x = self.rightx
                    self.cursor_y = self.righty
                elif d == self.UP:
                    self.cursor_x = self.upx
                    self.cursor_y = self.upy
                elif d == self.DOWN:
                    self.cursor_x = self.downx
                    self.cursor_y = self.downy
                elif d == self.TAB:
                    self.cursor_x = self.tabx
                    self.cursor_y = self.taby
                elif d == self.ENTER:
                    self.cursor_x = self.enterx
                    self.cursor_y = self.entery
                elif d == self.SPACE:
                    self.cursor_x = self.spacex
                    self.cursor_y = self.spacey
                elif d == self.BACKTAB:
                    self.cursor_x = self.backtabx
                    self.cursor_y = self.backtaby
            # Move the cursor based
            if d == self.LEFT:
                self.screen.move(self.lefty, self.leftx)
            elif d == self.RIGHT:
                self.screen.move(self.righty, self.rightx)
            elif d == self.UP:
                self.screen.move(self.upy, self.upx)
            elif d == self.DOWN:
                self.screen.move(self.downy, self.downx)
            elif d == self.TAB:
                self.screen.move(self.taby, self.tabx)
            elif d == self.ENTER:
                self.screen.move(self.entery, self.enterx)
            elif d == self.SPACE:
                self.screen.move(self.spacey, self.spacex)
            elif d == self.BACKTAB:
                self.screen.move(self.backtaby, self.backtabx)
        elif argtype == self.FIELD:
            if d == self.LEFT:
                self.deselect()
                self.leftfield.select()
                return self.leftfield
            elif d == self.RIGHT:
                self.deselect()
                self.rightfield.select()
                return self.rightfield
            elif d == self.UP:
                self.deselect()
                self.upfield.select()
                return self.upfield
            elif d == self.DOWN:
                self.deselect()
                self.downfield.select()
                return self.downfield
            elif d == self.TAB:
                self.deselect()
                self.tabfield.select()
                return self.tabfield
            elif d == self.ENTER:
                self.deselect()
                self.enterfield.select()
                return self.enterfield
            elif d == self.SPACE:
                self.deselect()
                self.spacefield.select()
                return self.spacefield
            elif d == self.BACKTAB:
                self.deselect()
                self.backtabfield.select()
                return self.backtabfield
        elif argtype == self.FUNCTION:
            if d == self.LEFT:
                return self.leftfn()
            elif d == self.RIGHT:
                return self.rightfn()
            elif d == self.UP:
                return self.upfn()
            elif d == self.DOWN:
                return self.downfn()
            elif d == self.TAB:
                return self.tabfn()
            elif d == self.ENTER:
                return self.enterfn()
            elif d == self.SPACE:
                return self.spacefn()
            elif d == self.BACKTAB:
                return self.backtabfn()
        self.screen.refresh()

    # Set absolute cursor behavior on input
    def setcursor_absolute(self, d, x, y, inline):
        # Set argument type
        if d == self.LEFT:
            self.left_argtype = self.CURSOR_A
        elif d == self.RIGHT:
            self.right_argtype = self.CURSOR_A
        elif d == self.UP:
            self.up_argtype = self.CURSOR_A
        elif d == self.DOWN:
            self.down_argtype = self.CURSOR_A
        elif d == self.TAB:
            self.tab_argtype = self.CURSOR_A
        elif d == self.ENTER:
            self.enter_argtype = self.CURSOR_A
        elif d == self.SPACE:
            self.space_argtype = self.CURSOR_A
        elif d == self.BACKTAB:
            self.backtab_argtype = self.CURSOR_A
        # Check type
        if isinstance(x, int):
            if inline:
                # Bound size
                if (x >= 0 and (x + self.x1) <= self.x2):
                    if d == self.LEFT:
                        self.leftx = x + self.x1
                    elif d == self.RIGHT:
                        self.rightx = x + self.x1
                    elif d == self.UP:
                        self.upx = x + self.x1
                    elif d == self.DOWN:
                        self.downx = x + self.x1
                    elif d == self.TAB:
                        self.tabx = x + self.x1
                    elif d == self.ENTER:
                        self.enterx = x + self.x1
                    elif d == self.SPACE:
                        self.spacex = x + self.x1
                    elif d == self.BACKTAB:
                        self.backtabx = x + self.x1
                else:
                    raise ValueError("'x' must be between {} -> {}".format(0, self.x2 - self.x1))
            else:
                # Bound size
                if (x >= 0 and x <= self.MAX_X):
                    if d == self.LEFT:
                        self.leftx = x
                    elif d == self.RIGHT:
                        self.rightx = x
                    elif d == self.UP:
                        self.upx = x
                    elif d == self.DOWN:
                        self.downx = x
                    elif d == self.TAB:
                        self.tabx = x
                    elif d == self.ENTER:
                        self.enterx = x
                    elif d == self.SPACE:
                        self.spacex = x
                    elif d == self.BACKTAB:
                        self.backtabx = x
                else:
                    raise ValueError("'x' must be between {} -> {}".format(0, self.MAX_X))
        else:
            raise TypeError("'x' must be of type 'int'")
        # Check type
        if isinstance(y, int):
            if inline:
                # Bound size
                if (y >= 0 and (y + self.y1) <= self.y2):
                    if d == self.LEFT:
                        self.lefty = y + self.y1
                    elif d == self.RIGHT:
                        self.righty = y + self.y1
                    elif d == self.UP:
                        self.upy = y + self.y1
                    elif d == self.DOWN:
                        self.downy = y + self.y1
                    elif d == self.TAB:
                        self.taby = y + self.y1
                    elif d == self.ENTER:
                        self.entery = y + self.y1
                    elif d == self.SPACE:
                        self.spacey = y + self.y1
                    elif d == self.BACKTAB:
                        self.backtaby = y + self.y1
                else:
                    raise ValueError("'y' must be between {} -> {}".format(0, self.y2 - self.y1))
            else:
                # Bound size
                if (y >= 0 and y <= self.MAX_Y):
                    if d == self.LEFT:
                        self.lefty = y
                    elif d == self.RIGHT:
                        self.righty = y
                    elif d == self.UP:
                        self.upy = y
                    elif d == self.DOWN:
                        self.downy = y
                    elif d == self.TAB:
                        self.taby = y
                    elif d == self.ENTER:
                        self.entery = y
                    elif d == self.SPACE:
                        self.spacey = y
                    elif d == self.BACKTAB:
                        self.backtaby = y
                else:
                    raise ValueError("'y' must be between {} -> {}".format(0, self.MAX_Y))
        else:
            raise TypeError("'y' must be of type 'int'")

    # Set relative cursor behavior on input
    def setcursor_relative(self, d, x, y, inline):
        # Set argument type
        if d == self.LEFT:
            self.left_argtype = self.CURSOR_R
        elif d == self.RIGHT:
            self.right_argtype = self.CURSOR_R
        elif d == self.UP:
            self.up_argtype = self.CURSOR_R
        elif d == self.DOWN:
            self.down_argtype = self.CURSOR_R
        elif d == self.TAB:
            self.tab_argtype = self.CURSOR_R
        elif d == self.ENTER:
            self.enter_argtype = self.CURSOR_R
        elif d == self.SPACE:
            self.space_argtype = self.CURSOR_R
        elif d == self.BACKTAB:
            self.backtab_argtype = self.CURSOR_R
        # Check type
        if isinstance(x, int):
            if inline:
                # Bound size
                if (x <= 0) and (self.cursor_x + x >= self.x1):
                    if d == self.LEFT:
                        self.leftx = x + self.cursor_x
                    elif d == self.RIGHT:
                        self.rightx = x + self.cursor_x
                    elif d == self.UP:
                        self.upx = x + self.cursor_x
                    elif d == self.DOWN:
                        self.downx = x + self.cursor_x
                    elif d == self.TAB:
                        self.tabx = x + self.cursor_x
                    elif d == self.ENTER:
                        self.enterx = x + self.cursor_x
                    elif d == self.SPACE:
                        self.spacex = x + self.cursor_x
                    elif d == self.BACKTAB:
                        self.backtabx = x + self.cursor_x
                elif (x > 0) and (self.cursor_x + x <= self.x2):
                    if d == self.LEFT:
                        self.leftx = x + self.cursor_x
                    elif d == self.RIGHT:
                        self.rightx = x + self.cursor_x
                    elif d == self.UP:
                        self.upx = x + self.cursor_x
                    elif d == self.DOWN:
                        self.downx = x + self.cursor_x
                    elif d == self.TAB:
                        self.tabx = x + self.cursor_x
                    elif d == self.ENTER:
                        self.enterx = x + self.cursor_x
                    elif d == self.SPACE:
                        self.spacex = x + self.cursor_x
                    elif d == self.BACKTAB:
                        self.backtabx = x + self.cursor_x
            else:
                # Bound size
                if (x <= 0) and (self.x1 + x >= 0):
                    if d == self.LEFT:
                        self.leftx = x + self.x1
                    elif d == self.RIGHT:
                        self.rightx = x + self.x1
                    elif d == self.UP:
                        self.upx = x + self.x1
                    elif d == self.DOWN:
                        self.downx = x + self.x1
                    elif d == self.TAB:
                        self.tabx = x + self.x1
                    elif d == self.ENTER:
                        self.enterx = x + self.x1
                    elif d == self.SPACE:
                        self.spacex = x + self.x1
                    elif d == self.BACKTAB:
                        self.backtabx = x + self.x1
                elif (x > 0) and (self.x2 + x <= self.MAX_X):
                    if d == self.LEFT:
                        self.leftx = x + self.x2
                    elif d == self.RIGHT:
                        self.rightx = x + self.x2
                    elif d == self.UP:
                        self.upx = x + self.x2
                    elif d == self.DOWN:
                        self.downx = x + self.x2
                    elif d == self.TAB:
                        self.tabx = x + self.x2
                    elif d == self.ENTER:
                        self.enterx = x + self.x2
                    elif d == self.SPACE:
                        self.spacex = x + self.x2
                    elif d == self.BACKTAB:
                        self.backtabx = x + self.x2
                else:
                    raise ValueError("'x' must be between {} -> {}".format(self.x1 - self.cursor_x, self.x2 - self.cursor_x))
        else:
            raise TypeError("'x' must be of type 'int'")
        # Check type
        if isinstance(y, int):
            if inline:
                # Bound size
                if (y <= 0) and (self.cursor_y + y >= self.y1):
                    if d == self.LEFT:
                        self.lefty = y + self.cursor_y
                    elif d == self.RIGHT:
                        self.righty = y + self.cursor_y
                    elif d == self.UP:
                        self.upy = y + self.cursor_y
                    elif d == self.DOWN:
                        self.downy = y + self.cursor_y
                    elif d == self.TAB:
                        self.taby = y + self.cursor_y
                    elif d == self.ENTER:
                        self.entery = y + self.cursor_y
                    elif d == self.SPACE:
                        self.spacey = y + self.cursor_y
                    elif d == self.BACKTAB:
                        self.backtaby = y + self.cursor_y
                elif (y > 0) and (self.cursor_y + y <= self.y2):
                    if d == self.LEFT:
                        self.lefty = y + self.cursor_y
                    elif d == self.RIGHT:
                        self.righty = y + self.cursor_y
                    elif d == self.UP:
                        self.upy = y + self.cursor_y
                    elif d == self.DOWN:
                        self.downy = y + self.cursor_y
                    elif d == self.TAB:
                        self.taby = y + self.cursor_y
                    elif d == self.ENTER:
                        self.entery = y + self.cursor_y
                    elif d == self.SPACE:
                        self.spacey = y + self.cursor_y
                    elif d == self.BACKTAB:
                        self.backtaby = y + self.cursor_y
                else:
                    raise ValueError("'y' must be between {} -> {}".format(self.y1 - self.cursor_y, self.y2 - self.cursor_y))
            else:
                # Bound size
                if (y <= 0) and (self.y1 + y >= 0):
                    if d == self.LEFT:
                        self.lefty = y + self.y1
                    elif d == self.RIGHT:
                        self.righty = y + self.y1
                    elif d == self.UP:
                        self.upy = y + self.y1
                    elif d == self.DOWN:
                        self.downy = y + self.y1
                    elif d == self.TAB:
                        self.taby = y + self.y1
                    elif d == self.ENTER:
                        self.entery = y + self.y1
                    elif d == self.SPACE:
                        self.spacey = y + self.y1
                    elif d == self.BACKTAB:
                        self.backtaby = y + self.y1
                elif (y > 0) and (self.y2 + y <= self.MAX_Y):
                    if d == self.LEFT:
                        self.lefty = y + self.y2
                    elif d == self.RIGHT:
                        self.righty = y + self.y2
                    elif d == self.UP:
                        self.upy = y + self.y2
                    elif d == self.DOWN:
                        self.downy = y + self.y2
                    elif d == self.TAB:
                        self.taby = y + self.y2
                    elif d == self.ENTER:
                        self.entery = y + self.y2
                    elif d == self.SPACE:
                        self.spacey = y + self.y2
                    elif d == self.BACKTAB:
                        self.backtaby = y + self.y2
                else:
                    raise ValueError("'y' must be between {} -> {}".format(0, self.MAX_Y))
        else:
            raise TypeError("'y' must be of type 'int'")

    # Set field selection behavior on input
    def setfield(self, d, field):
        # Set argument type
        if d == self.LEFT:
            self.left_argtype = self.FIELD
            self.leftfield = field
        elif d == self.RIGHT:
            self.right_argtype = self.FIELD
            self.rightfield = field
        elif d == self.UP:
            self.up_argtype = self.FIELD
            self.upfield = field
        elif d == self.DOWN:
            self.down_argtype = self.FIELD
            self.downfield = field
        elif d == self.TAB:
            self.tab_argtype = self.FIELD
            self.tabfield = field
        elif d == self.ENTER:
            self.enter_argtype = self.FIELD
            self.enterfield = field
        elif d == self.SPACE:
            self.space_argtype = self.FIELD
            self.spacefield = field
        elif d == self.BACKTAB:
            self.backtab_argtype = self.FIELD
            self.backtabfield = field

    # Set function execution behavior on input
    def setfunction(self, d, fn):
        # Set argument type
        if d == self.LEFT:
            self.left_argtype = self.FUNCTION
            self.leftfn = fn
        elif d == self.RIGHT:
            self.right_argtype = self.FUNCTION
            self.rightfn = fn
        elif d == self.UP:
            self.up_argtype = self.FUNCTION
            self.upfn = fn
        elif d == self.DOWN:
            self.down_argtype = self.FUNCTION
            self.downfn = fn
        elif d == self.TAB:
            self.tab_argtype = self.FUNCTION
            self.tabfn = fn
        elif d == self.ENTER:
            self.enter_argtype = self.FUNCTION
            self.enterfn = fn
        elif d == self.SPACE:
            self.space_argtype = self.FUNCTION
            self.spacefn = fn
        elif d == self.BACKTAB:
            self.backtab_argtype = self.FUNCTION
            self.backtabfn = fn

    class Left:
        # Execute function for left input behavior
        def execute(self):
            return self.execute(self.left_argtype, self.LEFT)
        # Set absolute cursor behavior on left input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.LEFT, x, y, inline)
        # Set relative cursor behavior on left input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.LEFT, x, y, inline)
        # Set field selection behavior on left input

        def setfield(self, field):
            self.setfield(self.LEFT, field)
        # Set function execution behavior on left input

        def setfunction(self, fn):
            self.setfunction(self.LEFT, fn)

    class Right:
        # Execute function for right input behavior
        def execute(self):
            return self.execute(self.right_argtype, self.RIGHT)
        # Set absolute cursor behavior on right input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.RIGHT, x, y, inline)
        # Set relative cursor behavior on right input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.RIGHT, x, y, inline)
        # Set field selection behavior on right input

        def setfield(self, field):
            self.setfield(self.RIGHT, field)
        # Set function execution behavior on right input

        def setfunction(self, fn):
            self.setfunction(self.RIGHT, fn)

    class Up:
        # Execute function for up input behavior
        def execute(self):
            return self.execute(self.up_argtype, self.UP)
        # Set absolute cursor behavior on up input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.UP, x, y, inline)
        # Set relative cursor behavior on up input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.UP, x, y, inline)
        # Set field selection behavior on up input

        def setfield(self, field):
            self.setfield(self.UP, field)
        # Set function execution behavior on up input

        def setfunction(self, fn):
            self.setfunction(self.UP, fn)

    class Down:
        # Execute function for down input behavior
        def execute(self):
            return self.execute(self.down_argtype, self.DOWN)
        # Set absolute cursor behavior on down input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.DOWN, x, y, inline)
        # Set relative cursor behavior on down input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.DOWN, x, y, inline)
        # Set field selection behavior on down input

        def setfield(self, field):
            self.setfield(self.DOWN, field)
        # Set function execution behavior on down input

        def setfunction(self, fn):
            self.setfunction(self.DOWN, fn)

    class Tab:
        # Execute function for tab input behavior
        def execute(self):
            return self.execute(self.tab_argtype, self.TAB)
        # Set absolute cursor behavior on tab input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.TAB, x, y, inline)
        # Set relative cursor behavior on tab input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.TAB, x, y, inline)
        # Set field selection behavior on tab input

        def setfield(self, field):
            self.setfield(self.TAB, field)
        # Set function execution behavior on tab input

        def setfunction(self, fn):
            self.setfunction(self.TAB, fn)

    class Backtab:
        # Execute function for backtab input behavior
        def execute(self):
            return self.execute(self.backtab_argtype, self.BACKTAB)
        # Set absolute cursor behavior on backtab input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.BACKTAB, x, y, inline)
        # Set relative cursor behavior on backtab input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.BACKTAB, x, y, inline)
        # Set field selection behavior on backtab input

        def setfield(self, field):
            self.setfield(self.BACKTAB, field)
        # Set function execution behavior on backtab input

        def setfunction(self, fn):
            self.setfunction(self.BACKTAB, fn)

    class Enter:
        # Execute function for enter input behavior
        def execute(self):
            return self.execute(self.enter_argtype, self.ENTER)
        # Set absolute cursor behavior on enter input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.ENTER, x, y, inline)
        # Set relative cursor behavior on enter input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.ENTER, x, y, inline)
        # Set field selection behavior on enter input

        def setfield(self, field):
            self.setfield(self.ENTER, field)
        # Set function execution behavior on enter input

        def setfunction(self, fn):
            self.setfunction(self.ENTER, fn)

    class Space:
        # Execute function for space input behavior
        def execute(self):
            return self.execute(self.space_argtype, self.SPACE)
        # Set absolute cursor behavior on space input

        def setcursor_absolute(self, x, y, inline=False):
            self.setcursor_absolute(self.SPACE, x, y, inline)
        # Set relative cursor behavior on space input

        def setcursor_relative(self, x, y, inline=False):
            self.setcursor_relative(self.SPACE, x, y, inline)
        # Set field selection behavior on space input

        def setfield(self, field):
            self.setfield(self.SPACE, field)
        # Set function execution behavior on space input

        def setfunction(self, fn):
            self.setfunction(self.SPACE, fn)

    # GETTERS AND SETTERS

    # Getter for 'MAX_X'
    @property
    def MAX_X(self):
        return self._MAX_X

    # # Setter for 'MAX_X'
    @MAX_X.setter
    def MAX_X(self, MAX_X):
        raise AttributeError("'MAX_X' cannot be updated")

    # Getter for 'MAX_Y'
    @property
    def MAX_Y(self):
        return self._MAX_Y

    # # Setter for 'MAX_Y'
    @MAX_Y.setter
    def MAX_Y(self, MAX_Y):
        raise AttributeError("'MAX_Y' cannot be updated")

    # Getter for 'x1'
    @property
    def x1(self):
        return self._x1

    # Setter for 'x1'
    @x1.setter
    def x1(self, x1):
        # Check type
        if isinstance(x1, int):
            # Bound size
            if (x1 >= 0 and x1 < self.MAX_X):
                try:
                    # Make sure x1 <= x2
                    if x1 <= self.x2:
                        self._x1 = x1
                    else:
                        raise TypeError("'x1' must be less than 'x2'")
                except AttributeError:
                    self._x1 = x1
            else:
                raise ValueError("'x' must be between {} -> {}".format(0, self.MAX_X))
        else:
            raise TypeError("'x' must be of type 'int'")

    # Getter for 'x2'
    @property
    def x2(self):
        return self._x2

    # Setter for 'x2'
    @x2.setter
    def x2(self, x2):
        # Check type
        if isinstance(x2, int):
            # Bound size
            if (x2 >= 0 and x2 < self.MAX_X):
                try:
                    # Make sure x1 <= x2
                    if x2 >= self.x1:
                        self._x2 = x2
                    else:
                        raise TypeError("'x1' must be less than 'x2'")
                except AttributeError:
                    self._x2 = x2
            else:
                raise ValueError("'x' must be between {} -> {}".format(0, self.MAX_X))
        else:
            raise TypeError("'x' must be of type 'int'")

    # Getter for 'y1'
    @property
    def y1(self):
        return self._y1

    # Setter for 'y1'
    @y1.setter
    def y1(self, y1):
        # Check type
        if isinstance(y1, int):
            # Bound size
            if (y1 >= 0 and y1 < self.MAX_Y):
                try:
                    # Make sure x1 <= x2
                    if y1 <= self.y2:
                        self._y1 = y1
                    else:
                        raise TypeError("'y1' must be less than 'y2'")
                except AttributeError:
                    self._y1 = y1
            else:
                raise ValueError("'y' must be between \{} -> {}".format(0, self.MAX_Y))
        else:
            raise TypeError("'y' must be of type 'int'")

    # Getter for 'y2'
    @property
    def y2(self):
        return self._y2

    # Setter for 'y2'
    @y2.setter
    def y2(self, y2):
        # Check type
        if isinstance(y2, int):
            # Bound size
            if (y2 >= 0 and y2 < self.MAX_Y):
                try:
                    # Make sure x1 <= x2
                    if y2 >= self.y1:
                        self._y2 = y2
                    else:
                        raise TypeError("'y1' must be less than 'y2'")
                except AttributeError:
                    self._y2 = y2
            else:
                raise ValueError("'y' must be between \{} -> {}".format(0, self.MAX_Y))
        else:
            raise TypeError("'y' must be of type 'int'")

# Return the name of a key input code


def returnkeyname(keynum):
    # Printable Characters
    if keynum in range(33, 127):
        keyname = "PRINT"
    # Space
    elif keynum == 32:
        keyname = "SPACE"
    # Non-Printable Characters
    else:
        # F1
        if keynum == curses.KEY_F1:
            keyname = "F1"
        # F2
        elif keynum == curses.KEY_F2:
            keyname = "F2"
        # F3
        elif keynum == curses.KEY_F3:
            keyname = "F3"
        # F4
        elif keynum == curses.KEY_F4:
            keyname = "F4"
        # F5
        elif keynum == curses.KEY_F5:
            keyname = "F5"
        # F6
        elif keynum == curses.KEY_F6:
            keyname = "F6"
        # F7
        elif keynum == curses.KEY_F7:
            keyname = "F7"
        # F8
        elif keynum == curses.KEY_F8:
            keyname = "F8"
        # F9
        elif keynum == curses.KEY_F9:
            keyname = "F9"
        # F10
        elif keynum == curses.KEY_F10:
            keyname = "F10"
        # F11
        elif keynum == curses.KEY_F11:
            keyname = "F11"
        # F12
        elif keynum == curses.KEY_F12:
            keyname = "F12"
        # Left Arrow
        elif keynum == curses.KEY_LEFT:
            keyname = "LEFT"
        # Right Arrow
        elif keynum == curses.KEY_RIGHT:
            keyname = "RIGHT"
        # Up Arrow
        elif keynum == curses.KEY_UP:
            keyname = "UP"
        # Down Arrow
        elif keynum == curses.KEY_DOWN:
            keyname = "DOWN"
        # Backspace
        elif (keynum == curses.KEY_BACKSPACE or keynum == 8):
            keyname = "BACKSPACE"
        # Backtab
        elif keynum == curses.KEY_BTAB:
            keyname = "BACKTAB"
        # Delete
        elif keynum == curses.KEY_DC:
            keyname = "DELETE"
        # Escape
        elif keynum == 27:
            keyname = "ESCAPE"
        # End
        elif keynum == curses.KEY_END:
            keyname = "END"
        # Enter
        elif (keynum == 10 or keynum == 459):
            keyname = "ENTER"
        # Home
        elif keynum == curses.KEY_HOME:
            keyname = "HOME"
        # Insert
        elif keynum == curses.KEY_IC:
            keyname = "INSERT"
        # Page Down
        elif keynum == curses.KEY_NPAGE:
            keyname = "PAGEDOWN"
        # Page Up
        elif keynum == curses.KEY_PPAGE:
            keyname = "PAGEUP"
        # Tab
        elif keynum == 9:
            keyname = "TAB"
        # Shifted Left Arrow
        elif keynum == curses.KEY_SLEFT:
            keyname = "SHIFT_LEFT"
        # Shifted Right Arrow
        elif keynum == curses.KEY_SRIGHT:
            keyname = "SHIFT_RIGHT"
        # Shifted Up Arrow
        elif keynum == 547:
            keyname = "SHIFT_UP"
        # Shifted Down Arrow
        elif keynum == 548:
            keyname = "SHIFT_DOWN"
        # Shifted End
        elif keynum == curses.KEY_SEND:
            keyname = "SHIFT_END"
        # Shifted Home
        elif keynum == curses.KEY_SHOME:
            keyname = "SHIFT_HOME"
        # CTRL Left Arrow
        elif keynum == 443:
            keyname = "CTRL_LEFT"
        # CTRL Right Arrow
        elif keynum == 444:
            keyname = "CTRL_RIGHT"
        # CTRL Up Arrow
        elif keynum == 480:
            keyname = "CTRL_UP"
        # CTRL Down Arrow
        elif keynum == 481:
            keyname = "CTRL_DOWN"
        # CTRL Backspace
        elif keynum == 127:
            keyname = "CTRL_BACKSPACE"
        # CTRL Delete
        elif keynum == 527:
            keyname = "CTRL_DELETE"
        # CTRL End
        elif keynum == 448:
            keyname = "CTRL_END"
        # CTRL Enter
        elif keynum == 529:
            keyname = "CTRL_ENTER"
        # CTRL Home
        elif keynum == 447:
            keyname = "CTRL_HOME"
        # CTRL Tab
        elif keynum == 482:
            keyname = "CTRL_TAB"
        # CTRL A
        elif keynum == 1:
            keyname = "CTRL_A"
        # CTRL B
        elif keynum == 2:
            keyname = "CTRL_B"
        # CTRL C
        elif keynum == 3:
            keyname = "CTRL_C"
        # CTRL D
        elif keynum == 4:
            keyname = "CTRL_D"
        # CTRL E
        elif keynum == 5:
            keyname = "CTRL_E"
        # CTRL F
        elif keynum == 6:
            keyname = "CTRL_F"
        # CTRL G
        elif keynum == 7:
            keyname = "CTRL_G"
        # CTRL H
        elif keynum == 8:
            keyname = "CTRL_H"
        # CTRL I
        elif keynum == 9:
            keyname = "CTRL_I"
        # CTRL J
        elif keynum == 10:
            keyname = "CTRL_J"
        # CTRL K
        elif keynum == 11:
            keyname = "CTRL_K"
        # CTRL L
        elif keynum == 12:
            keyname = "CTRL_L"
        # CTRL M
        elif keynum == 13:
            keyname = "CTRL_M"
        # CTRL N
        elif keynum == 14:
            keyname = "CTRL_N"
        # CTRL O
        elif keynum == 15:
            keyname = "CTRL_O"
        # CTRL P
        elif keynum == 16:
            keyname = "CTRL_P"
        # CTRL Q
        elif keynum == 17:
            keyname = "CTRL_Q"
        # CTRL R
        elif keynum == 18:
            keyname = "CTRL_R"
        # CTRL S
        elif keynum == 19:
            keyname = "CTRL_S"
        # CTRL T
        elif keynum == 20:
            keyname = "CTRL_T"
        # CTRL U
        elif keynum == 21:
            keyname = "CTRL_U"
        # CTRL V
        elif keynum == 22:
            keyname = "CTRL_V"
        # CTRL W
        elif keynum == 23:
            keyname = "CTRL_W"
        # CTRL X
        elif keynum == 24:
            keyname = "CTRL_X"
        # CTRL Y
        elif keynum == 25:
            keyname = "CTRL_Y"
        # CTRL Z
        elif keynum == 26:
            keyname = "CTRL_Z"
        # ALT 0
        elif keynum == 407:
            keyname = "ALT_0"
        # ALT 1
        elif keynum == 408:
            keyname = "ALT_1"
        # ALT 2
        elif keynum == 409:
            keyname = "ALT_2"
        # ALT 3
        elif keynum == 410:
            keyname = "ALT_3"
        # ALT 4
        elif keynum == 411:
            keyname = "ALT_4"
        # ALT 5
        elif keynum == 412:
            keyname = "ALT_5"
        # ALT 6
        elif keynum == 413:
            keyname = "ALT_6"
        # ALT 7
        elif keynum == 414:
            keyname = "ALT_7"
        # ALT 8
        elif keynum == 415:
            keyname = "ALT_8"
        # ALT 9
        elif keynum == 416:
            keyname = "ALT_9"
        # ALT A
        elif keynum == 417:
            keyname = "ALT_A"
        # ALT B
        elif keynum == 418:
            keyname = "ALT_B"
        # ALT C
        elif keynum == 419:
            keyname = "ALT_C"
        # ALT D
        elif keynum == 420:
            keyname = "ALT_D"
        # ALT E
        elif keynum == 421:
            keyname = "ALT_E"
        # ALT F
        elif keynum == 422:
            keyname = "ALT_F"
        # ALT G
        elif keynum == 423:
            keyname = "ALT_G"
        # ALT H
        elif keynum == 424:
            keyname = "ALT_H"
        # ALT I
        elif keynum == 425:
            keyname = "ALT_I"
        # ALT J
        elif keynum == 426:
            keyname = "ALT_J"
        # ALT K
        elif keynum == 427:
            keyname = "ALT_K"
        # ALT L
        elif keynum == 428:
            keyname = "ALT_L"
        # ALT M
        elif keynum == 429:
            keyname = "ALT_M"
        # ALT N
        elif keynum == 430:
            keyname = "ALT_N"
        # ALT O
        elif keynum == 431:
            keyname = "ALT_O"
        # ALT P
        elif keynum == 432:
            keyname = "ALT_P"
        # ALT Q
        elif keynum == 433:
            keyname = "ALT_Q"
        # ALT R
        elif keynum == 434:
            keyname = "ALT_R"
        # ALT S
        elif keynum == 435:
            keyname = "ALT_S"
        # ALT T
        elif keynum == 436:
            keyname = "ALT_T"
        # ALT U
        elif keynum == 437:
            keyname = "ALT_U"
        # ALT V
        elif keynum == 438:
            keyname = "ALT_V"
        # ALT W
        elif keynum == 439:
            keyname = "ALT_W"
        # ALT X
        elif keynum == 440:
            keyname = "ALT_X"
        # ALT Y
        elif keynum == 441:
            keyname = "ALT_Y"
        # ALT Z
        elif keynum == 442:
            keyname = "ALT_Z"
        # Other
        else:
            keyname = "UNKNOWN"
            print(keynum)
    return keyname

# Send string at given coordinates


def sendatcoor(screen, x, y, string):
    # Get max possible values of coordinates
    MAX_Y, MAX_X = screen.getmaxyx()
    # Check if coordinates are within bounds
    if (MAX_X > x and MAX_Y > y):
        # Check if string is within bounds
        if (MAX_X > (x + len(string))):
            screen.addstr(y, x, string)
        else:
            raise ValueError("'string' value extends past bounds")
    else:
        raise ValueError("Coordinates extend past bounds")
    screen.refresh()

# Create a box with the given coordinates


def createbox(screen, x1, x2, y1, y2):
    # Get max possible values of coordinates
    MAX_Y, MAX_X = screen.getmaxyx()
    # Check if coordinates are within bounds
    if (0 <= x1 and x2 < MAX_X) and \
            (0 <= y1 and y2 < MAX_Y) and \
            ((x1 != x2) and (y1 != y2)):
        # Top of modal
        screen.addstr(y1, x1, "┌{}┐".format("─" * (x2 - x1 - 1)))
        # Sides of modal
        for y in range(y1 + 1, y2):
            screen.addstr(y, x1, "│")
            screen.addstr(y, x2, "│")
        # Bottom of modal
        screen.addstr(y2, x1, "└{}┘".format("─" * (x2 - x1 - 1)))
    else:
        print("{} -> {} -> {}".format((0 >= x1 and x2 < MAX_X), (0 >= y1 and y2 < MAX_Y), ((x1 != x2) and (y1 != y2))))
    screen.refresh()

# Receiving function for our thread
def recthread():
    global board, recvcloak, selected_field, screen, INTERFACE
    # Loop til you die
    while True:
        # Limit responses to 95 characters
        resp = recvcloak.recv_packets(iface=INTERFACE)[:95]
        # Put the message on the board
        board.updateboard(resp)
        # Re-select the normally selected field
        selected_field.select()
        screen.refresh()

# Three arguments given
if len(argv) == 4:
    # Check receiver IP
    if search(IP_REGEX, argv[1]) and search(IP_REGEX, argv[2]) and argv[3] in net_if_stats():
        recvcloak.ip_dst = argv[1]
        sendcloak.ip_dst = argv[2]
        INTERFACE = argv[3]
        # Initialize a curses window
        screen = curses.initscr()
        screen.keypad(True)
        curses.start_color()
        curses.echo(False)

        # Create the foundation of the message window
        createbox(screen, 0, 100, 0, 21)
        createbox(screen, 1, 99, 1, 15)
        sendatcoor(screen, 3, 17, "   Name: ")
        sendatcoor(screen, 3, 19, "Message: ")

        # Initialize our fields
        board = Field(screen, 2, 97, 2, 14, 2)
        handle = Field(screen, 12, 30, 17, 17, 1)
        msg = Field(screen, 12, 84, 19, 19, 1)

        # Set our connections for key input
        handle.Down.setfield(handle, msg)
        handle.Up.setfield(handle, msg)
        handle.Tab.setfield(handle, msg)
        handle.Backtab.setfield(handle, msg)
        msg.Down.setfield(msg, handle)
        msg.Up.setfield(msg, handle)
        msg.Tab.setfield(msg, handle)
        msg.Backtab.setfield(msg, handle)
        # Set the function for 'on-enter' key input
        handle.Enter.setfunction(handle, handle.returntext)
        msg.Enter.setfunction(msg, msg.returntext)

        # Initially select the handle
        selected_field = handle
        selected_field.select()

        # Start up our thread as a daemon
        x = Thread(target=recthread, daemon=True)
        x.start()

        keynum = 0
        # Exit on CTRL+C or ESC
        while (keynum != 27 and keynum != 3):
            # Get the key that was pressed
            keynum = screen.getch()
            keyname = returnkeyname(keynum)
            # Move up to the next field
            if keyname == "UP":
                selected_field = selected_field.Up.execute(selected_field)
            # Move down to the next field
            elif keyname == "DOWN":
                selected_field = selected_field.Down.execute(selected_field)
            # Tab to the next field
            elif keyname == "TAB":
                selected_field = selected_field.Tab.execute(selected_field)
            # Backtab to the previous field
            elif keyname == "BACKTAB":
                selected_field = selected_field.Backtab.execute(selected_field)
            # Printable characters
            elif keyname == "PRINT":
                # Add text to field
                selected_field.addtext(chr(keynum))
            # Space bar input
            elif keyname == "SPACE":
                # Add text to field
                selected_field.addtext(" ")
            # Backspace input
            elif keyname == "BACKSPACE":
                # Remove one character behind the cursor
                selected_field.backspacetext(False)
            # CTRL Backspace input
            elif keyname == "CTRL_BACKSPACE":
                # Remove line behind the cursor
                selected_field.backspacetext(True)
            # Delete input
            elif keyname == "DELETE":
                # Remove one character at the cursor
                selected_field.deletetext(False)
            # CTRL Delete input
            elif keyname == "CTRL_DELETE":
                # Remove all characters after the cursor
                selected_field.deletetext(True)
            # Move the cursor to the left one character
            elif keyname == "LEFT":
                # Check if at last character
                if selected_field.cursor_x == selected_field.x1:
                    selected_field.moveinputcursor(100)
                else:
                    selected_field.moveinputcursor(-1)
            # Move the cursor to the leftmost character
            elif (keyname == "CTRL_LEFT" or keyname == "HOME"):
                selected_field.moveinputcursor(-100)
            # Move the cursor to the right one character
            elif keyname == "RIGHT":
                # Check if at last character
                if selected_field.cursor_x == selected_field.x2:
                    selected_field.moveinputcursor(-100)
                else:
                    selected_field.moveinputcursor(1)
            # Move the cursor to the rightmost character
            elif (keyname == "CTRL_RIGHT" or keyname == "END"):
                selected_field.moveinputcursor(100)
            # Ingest and send the handle and message
            elif keyname == "ENTER":
                # Tell the user we are sending
                sendatcoor(screen, 50, 17, "Sending...")
                # Get the text values of the handle and message
                strhandle = handle.Enter.execute(handle)
                strmsg = msg.Enter.execute(msg)
                # Format and ingest the data
                sendcloak.ingest("{} > {}".format(strhandle, strmsg))
                # Send the packets and EOT
                sendcloak.send_packets(iface=INTERFACE)
                # Put the message on the board
                board.updateboard("{} > {}".format(strhandle, strmsg))
                sendatcoor(screen, 50, 17, "          ")
                # Clear the message field and move the cursor back
                msg.cleartext()
                msg.moveinputcursor(-100)
            # Keep the screen refreshed
            screen.refresh()

        # Clean up on exit
        screen.keypad(False)
        curses.endwin()
        curses.echo(True)
        curses.nocbreak()
    # IP didn't match
    else:
        print("Usage: 'python teamCommunication.py <src_ip> <dst_ip> <interface>'")
else:
    # Wrong arguments
    print("Usage: 'python teamCommunication.py <src_ip> <dst_ip> <interface>'")
    print("Your arguments: {}".format(argv))