from abc import ABC, abstractmethod
from logging import error, warning
from os import geteuid

# Check to make sure we have the correct privileges
if geteuid() != 0:
    warning("You must be root to send packets with cov3rt!")

# Cloak superclass
class Cloak(ABC):

    @abstractmethod
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        pass
    
    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    def send_delimiter(self):
        """Sends a delimiter to signal the end of a specified data stream."""
        pass

    @abstractmethod
    def send_packets(self):
        """Sends the entire ingested data via the send_packet method."""
        pass

    @abstractmethod
    def send_packet(self, data):
        """Sends packet(s) via a defined covert channel."""
        pass

    @abstractmethod
    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the defined covert channel."""
        pass

    def recv_packets(self):
        """Receives packets which use the Case Modulated DNS Cloak."""
        pass

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        pass

    def recv_delimiter(self, pkt):
        """Specifies the delimiter packet that signals the end of a specified data stream."""
        pass

    
    ## Getters and Setters ##
    # Getter for 'description'
    @property
    def description(self):
        return self._description
    
    # Setter for 'description'
    @description.setter
    def description(self, d):
        # Check type
        if isinstance(d, str):
            # Set the description
            self._description = d
        else:
            error("'description' must be of type 'str'")
    
    # Getter for 'name'
    @property
    def name(self):
        return self._name
    
    # Setter for 'name'
    @name.setter
    def name(self, d):
        # Check type
        if isinstance(d, str):
            # Set the name
            self._name = d
        else:
            error("'name' must be of type 'str'")
