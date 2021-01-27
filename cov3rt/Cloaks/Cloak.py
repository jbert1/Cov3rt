from abc import ABC, abstractmethod
from logging import error, warning

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
    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
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
