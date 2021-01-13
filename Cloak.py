from scapy.all import send
from logging import critical, error, info, warning, debug

# Cloak superclass
class Cloak(object):

    # Constructor
    def __init__(self, description = "An example cloak for the cov3rt framework."):
        # Description for this cloak
        self.desc = description
        # Initialize data
        self.data = []
    
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        self.data = data
    
    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    def send_delimiter(self):
        """Sends a delimiter to signal the end of a specified data stream."""
        pass

    def send_packets(self):
        """Sends the entire ingested data via the send_packet method."""
        pass

    def send_packet(self):
        """Sends packet(s) via a defined covert channel."""
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

    # Getter for 'cloak_type'
    @property
    def cloak_type(self):
        return self._cloak_type
    
    # Setter for 'cloak_type'
    @cloak_type.setter
    def cloak_type(self, cloak):
        # Check type
        if isinstance(cloak, int):
            # Set the cloak_type
            if (cloak == self.STREAM_CLOAK or cloak == self.MODULATE_CLOAK):
                self._cloak_type = cloak
            else:
                error("Cloak type must be STREAM_CLOAK or MODULATE_CLOAK!")
        else:
            error("Cloak type must be STREAM_CLOAK or MODULATE_CLOAK!")