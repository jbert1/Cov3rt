from os import urandom
from random import randint
from logging import info, debug, DEBUG, WARNING
from re import search
from scapy.all import Raw
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class TCPOneCharSeqNum(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "TCP One Character Seq Number"
    description = "A cloak based on changing the TCP sequence number \nASCII values."

    def __init__(self, ip_dst="8.8.8.8", send_port=25565, dest_port=25577):
        self.ip_dst = ip_dst
        self.send_port = send_port
        self.dest_port = dest_port
        self.read_data = ""

    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = [ord(i) for i in data]
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        # Generate random  string to go into packet payload
        packet_string = urandom(randint(25, 50))

        # Create packet with fluff payload and the IP flags set to 0x04
        pkt = IP(dst=self.ip_dst, flags=0x04) / TCP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, num, iface=None):
        """Sends packets based on TCP sequence number."""
        
        # Generate random string to go into packet payload
        packet_string = urandom(randint(25, 50))

        pkt = IP(dst=self.ip_dst) / TCP(sport=self.send_port, dport=self.dest_port, seq=num) / Raw(packet_string)
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
        """Specifies the packet handler for receiving information via the TCP Sequence Number Cloak."""
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["TCP"].sport == self.send_port and pkt["TCP"].dport == self.dest_port and pkt["IP"].flags != 0x04:
                self.read_data += chr(pkt["TCP"].seq)
                debug("Received a '{}'".format(chr(pkt["TCP"].seq)))
                info("String: {}".format(self.read_data))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["TCP"].sport == self.send_port and pkt["TCP"].dport == self.dest_port and pkt["IP"].flags == 0x04:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the TCP Sequence Number Cloak."""
        info("Receiving packets...")
        self.read_data = ''
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        info("String decoded: {}".format(self.read_data))
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

    # Getter for send_port
    @property
    def send_port(self):
        return self._send_port

    # Setter for send_port
    @send_port.setter
    def send_port(self, send_port):
        # Ensure valid type int
        if isinstance(send_port, int):
            # Ensure valid range
            if 1 <= send_port <= 65535:
                self._send_port = send_port
            else:
                raise ValueError("'send_port' must be within valid port range (1-65535)")
        else:
            raise TypeError("'send_port' must be of type 'int'")

    # Getter for dest_port
    @property
    def dest_port(self):
        return self._dest_port

    # Setter for dest_port
    @dest_port.setter
    def dest_port(self, dest_port):
        # Ensure valid type int
        if isinstance(dest_port, int):
            # Ensure valid range
            if 1 <= dest_port <= 65535:
                self._dest_port = dest_port
            else:
                raise ValueError("'dest_port' must be within valid port range (1-65535)")
        else:
            raise TypeError("'dest_port' must be of type 'int'")
