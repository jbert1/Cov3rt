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

from abc import ABC, abstractmethod
from logging import warning

# Check priviliges based on OS
try:
    from os import geteuid
    if geteuid() != 0:
        warning("You must be root to send packets with cov3rt!")
# If this doesn't exist, assume we are OK with Windows
except ImportError:
    pass


# Cloak superclass
class Cloak(ABC):

    # Classifications
    INTER_PACKET_TIMING = "Inter-Packet Timing"
    MESSAGE_TIMING = "Message Timing"
    RATE_THROUGHPUT_TIMING = "Rate/Throughput"
    ARTIFICIAL_LOSS = "Artificial Loss"
    MESSAGE_ORDERING = "Message (PDU) Ordering"
    RETRANSMISSION = "Retransmission"
    FRAME_COLLISIONS = "Frame Collisions"
    TEMPERATURE = "Temperature"
    ARTIFICIAL_RECONNECTIONS = "Artificial Reconnections"
    SIZE_MODULATION = "Size Modulation"
    POSITION = "Sequence Position"
    NUMBER_OF_ELEMENTS = "Number of Elements"
    RANDOM_VALUE = "Random Value"
    CASE_MODULATION = "Case Modulation"
    LSB_MODULATION = "LSB Modulation"
    VALUE_INFLUENCING = "Value Influencing"
    RESERVED_UNUSED = "Reserved/Unused"
    PAYLOAD_FIELD_SIZE_MODULATION = "Payload Size Modulation"
    USER_DATA_CORRUPTION = "User-Data Corruption"
    MODIFY_REDUNDANCY = "Modify Redundancy"
    USER_DATA_VALUE_MODULATION_RESERVED_UNUSED = "User-Data Value Modulation"

    @abstractmethod
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        pass

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of
        transmission."""
        pass

    def send_delimiter(self, iface=None):
        """Sends a delimiter to signal the end of a specified data stream."""
        pass

    @abstractmethod
    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        pass

    @abstractmethod
    def send_packet(self, data, iface=None):
        """Sends packet(s) via a defined covert channel."""
        pass

    @abstractmethod
    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the defined covert channel."""
        pass

    @abstractmethod
    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the Case Modulated DNS Cloak."""
        pass

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        pass

    # Getters and Setters
    # Getter for 'description'

    @property
    def description(self):
        return self._description

    # Setter for 'description'
    @description.setter
    def description(self, d):
        # Check type
        if isinstance(d, str):
            # Loop over the lines of the description to check length
            for line in d.split("\n"):
                # Line too long
                if len(line) >= 53:
                    raise ValueError("'description' lines must be less than 53 characters long")
            # Set the description
            self._description = d
        else:
            raise TypeError("'description' must be of type 'str'")

    # Getter for 'name'
    @property
    def name(self):
        return self._name

    # Setter for 'name'
    @name.setter
    def name(self, d):
        # Check type
        if isinstance(d, str):
            # Check if the name is the correct size
            if len(d) <= 30:
                # Set the name
                self._name = d
            # Name is too long for the application menu
            else:
                raise ValueError("'name' must be less than 30 characters long")
        else:
            raise TypeError("'name' must be of type 'str'")
