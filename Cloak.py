from scapy.all import send
from logging import critical, error, info, warning, debug

# Cloak superclass
class Cloak(object):

    # Constants
    STREAM_CLOAK = 0
    MODULATE_CLOAK = 1

    # Constructor
    def __init__(self, description = "An example cloak for the cov3rt framework.", cloak_type = 0):
        # Description for this cloak
        self.desc = description
        # Type of cloak (Stream or Modulation)
        self.cloak_type = cloak_type
        # Data pointer
        self.data_pointer = -1
        # Initialize data
        self.data = []
        # self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw()
    
    def ingest(self, data):
        """Ingests and formats data for the cloak to communicate."""
        self.data = data
    
    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    def send_delimiter(self):
        """Sends a delimiter to signal the end of a specified data stream."""
        pass

    # def send_next_packet(self):
    #     pass

    # # Update data
    # def update(self, data):
    #     # Create random string
    #     s = ""
    #     for i in range(data):
    #         s += choice(printable)
    #     # Update packet data
    #     self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw(s)
    
    
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