from scapy.all import send
from logging import critical, error, info, warning, debug
from abc import ABC, abstractmethod

# Cloak superclass
class Cloak(ABC):
    
    @abstractmethod
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        pass
    
    @abstractmethod
    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    @abstractmethod
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
    
    ## Getters and Setters ##
    # Getter for 'description'
    @property
    def description(self):
        return self._description
    
    # Setter for 'description'
    @description.setter
    @abstractmethod
    def description(self, d):
        # Check type
        if isinstance(d, str):
            # Set the description
            self._description = d
        else:
            error("'description' must be of type 'str'")

class TestCloak(Cloak):

    def __init__(self, description = "An example cloak for the cov3rt framework."):
        self.description = description
    
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        pass
    
    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    def send_delimiter(self):
        """Sends a delimiter to signal the end of a specified data stream."""
        pass

    def send_packets(self):
        """Sends the entire ingested data via the send_packet method."""
        pass

    def send_packet(self, data):
        """Sends packet(s) via a defined covert channel."""
        pass