from scapy.sendrecv import send, sniff
from scapy.layers.inet import IP, UDP
from scapy.all import Raw
from scapy.utils import wrpcap

from logging import error, info, debug, DEBUG, WARNING
from re import search
from time import sleep
from string import printable
from random import choice

from cov3rt.Cloaks.Cloak import Cloak

class UDPSizeModulation(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.SIZE_MODULATION
    name = "UDP Payload"
    description = "A cloak based on modulation of the UDP payload."
    
    def __init__(self, ip_dst = "192.168.1.101", send_port = 25565, dest_port = 25577):
        self.ip_dst = ip_dst
        self.send_port = send_port
        self.dest_port = dest_port
        self.read_data = ""

    def ingest(self, data):
        '''Ingests and formats data as a binary stream.'''
        if isinstance(data, str):
            self.data = [ord(i) for i in data]
            debug(self.data)
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        '''Send an end-of-transmission packet to signal end of transmission.'''
        # Create short random string of four characters for final packet
        packet_string = ""
        for i in range(4):
            packet_string += choice(printable)
        # Create packet and send
        pkt = IP(dst = self.ip_dst)/UDP(sport = self.send_port, dport = self.dest_port)/Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True)
        else:
            send(pkt, verbose = False)

    def send_packet(self, number):
        '''Sends single packet based on the number in stream.'''
        # Generate random string to go into packet based on number
        packet_string = ""
        for i in range(number):
            packet_string += choice(printable)
        # Create packet and send
        pkt = IP(dst = self.ip_dst)/UDP(sport = self.send_port, dport = self.dest_port)/Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True)
        else:
            send(pkt, verbose = False)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data 
        for item in self.data:
            self.send_packet(item)
            # Packet delay
            if (isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                debug("Packet delay sleep for {}s".format(packetDelay))
                sleep(packetDelay)

        # End delay
        if (isinstance(endDelay, int) or isinstance(endDelay, float)):
            debug("End delay sleep for {}s".format(endDelay))
            sleep(endDelay)
        self.send_EOT()
        return True

    def packet_handler(self, pkt):
        '''Specifies the packet handler for receiving info via the UDP Size Modulation cloak.'''
        if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw)):
            # Check for correct options
            if (pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port):
                length = len(pkt["Raw"].load)
                if length != 4:
                    self.read_data += chr(length)
                    debug("Received a '{}'".format(chr(length)))
                    info("String: {}".format(self.read_data))
        
    def recv_EOT(self, pkt):
        '''Specifies the EOT packet, singaling the end of transmission.'''
        if (pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw)):
            # Check for correct options
            if (pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port):
                length = len(pkt["Raw"].load)
                if length == 4:
                    info("Received EOT")
                    return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        """Receives packets which use the UDP Size Modulation Cloak."""  
        info("Receiving packets...")
        self.read_data = ''
        if max_count:
            packets = sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            packets = sniff(timeout = timeout, iface = iface, offline = in_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        info("String decoded: {}".format(self.read_data))
        return self.read_data

    ## Getters and Setters ##
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
                error("Invalid IP '{}'".format(ip_dst))
        else:
            error("'ip_dst' must be of type 'str'")
    
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
            if (1 <= send_port <= 65535):
                self._send_port = send_port
            else:
                error("'send_port' must be within valid port range (1-65535)")
        else:
            error("'send_port' must be of type 'int'")

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
            if (1 <= dest_port <= 65535):
                self._dest_port = dest_port
            else:
                error("'dest_port' must be within valid port range (1-65535)")
        else:
            error("'dest_port' must be of type 'int'")
