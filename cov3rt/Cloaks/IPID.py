from logging import info, debug, DEBUG, WARNING
from re import search
from scapy.layers.inet import IP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class IPID(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING
    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "IP Identification"
    description = "A covert channel using the Identification Field in \nIP packets to transmit messages."

    def __init__(self, ip_dst="10.10.10.10"):
        self.ip_dst = ip_dst
        self.read_data = []

    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = [ord(i) if ord(i) < 65535 else 64 for i in data]
            debug(self.data)

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst=self.ip_dst, id=4)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, var_id, iface=None):
        """Sends packets based on IP Identification Field."""
        pkt = IP(dst = self.ip_dst)
        # Set the IP ID field of the packet as our falsified ID
        pkt.id = var_id
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data
        for item in self.data:
            self.send_packet(item, iface)
            # Packet delay
            if isinstance(packetDelay, int) or isinstance(packetDelay, float):
                debug("Packet delay sleep for {}s".format(packetDelay))
                sleep(packetDelay)

        # End delay
        if isinstance(endDelay, int) or isinstance(endDelay, float):
            debug("End delay sleep for {}s".format(endDelay))
            sleep(endDelay)
        self.send_EOT(iface)
        return True

    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the IP Identification Cloak."""
        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst:
                self.read_data.append(pkt.id)
                debug("Received {}".format(pkt.id))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].id == 4:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the IP Identification Cloak."""
        info("Receiving packets...")
        self.read_data = []
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        # Decode read data
        decoded_string = ''
        # Loop over the data
        for item in self.read_data[:-1]:
            # Get the ascii character and add it to our string
            decoded_string += chr(item)
        info("String decoded: {}".format(decoded_string))
        return decoded_string

    # Getters and Setters
    # Getter for "ip_dst"
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for "ip_dst"
    @ip_dst.setter
    def ip_dst(self, ip_dst):
        # Ensure valid type:str
        if isinstance(ip_dst, str):
            # Ensure valid IP format
            if search(self.IP_REGEX, ip_dst):
                self._ip_dst = ip_dst
            else:
                raise ValueError("Invalid IP address provided: {}".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")

