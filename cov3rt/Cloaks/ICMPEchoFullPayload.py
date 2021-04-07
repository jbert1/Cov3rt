from logging import info, debug, DEBUG, WARNING
from re import search
from scapy.all import Raw
from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class ICMPEchoFullPayload(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.USER_DATA_VALUE_MODULATION_RESERVED_UNUSED
    name = "ICMP Echo Full Payload"
    description = "A cloak based on putting the entire message in \nthe ICMP echo payload field."

    def __init__(self, ip_dst="8.8.8.8"):
        self.ip_dst = ip_dst
        self.read_data = ""

    def ingest(self, data):
        """Ingests and formats data as a single element."""
        if isinstance(data, str):
            self.data = [data]
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst=self.ip_dst) / ICMP(type=8) / Raw(load="\x04")
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, databit, iface=None):
        """Sends a packet with the message in the ICMP echo payload."""
        pkt = IP(dst=self.ip_dst) / ICMP(type=8) / Raw(load=self.data)
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
        """Specifies the packet handler for receiving information via the IP
        Reserved Bit Cloak."""
        if pkt.haslayer(IP) and pkt.haslayer(ICMP):
            if pkt["IP"].dst == self.ip_dst and pkt["Raw"].load != b"\x04":
                self.read_data += pkt["Raw"].load.decode("UTF-8")
                info("Received: {}".format(pkt["Raw"].load))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of
        transmission."""
        if pkt.haslayer(IP) and pkt.haslayer(ICMP):
            if pkt["IP"].dst == self.ip_dst and pkt["Raw"].load == b"\x04":
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the IP Reserved Bit Cloak."""
        info("Receiving packets...")
        self.read_data = ''
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        # Return read data
        return self.read_data

    # Getters and Setters
    # Getter for 'ip_dst'
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for 'ip_dst'
    @ip_dst.setter
    def ip_dst(self, ip_dst):
        # Check type
        if isinstance(ip_dst, str):
            # Check if a valid IP
            if search(self.IP_REGEX, ip_dst):
                self._ip_dst = ip_dst
            # Not a valid IP
            else:
                raise ValueError("Invalid IP '{}'".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")
