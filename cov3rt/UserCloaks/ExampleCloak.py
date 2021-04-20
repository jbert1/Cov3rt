from scapy.sendrecv import send, sniff
from cov3rt.Cloaks.Cloak import Cloak


class ExampleCloak(Cloak):

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "Example User Cloak"
    description = "An example cloak."

    def __init__(self):
        pass

    def ingest(self, data):
        """Ingests and formats data."""
        pass

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pass

    def send_packet(self, databit, iface=None):
        """Sends packets based on case modulation encoding."""
        pass

    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        pass

    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the Case
        Modulated DNS Cloak."""
        pass

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of
        transmission."""
        pass

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the Case Modulated DNS Cloak."""
        pass
