from logging import info, debug, DEBUG, WARNING
from os import urandom
from re import search
from scapy.all import Raw
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class UDPFlood(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.NUMBER_OF_ELEMENTS
    name = "UDP Number of Elements"
    description = "A cloak that sends a number of packets equal to the\nASCII integer value of the selected character."

    def __init__(self, ip_dst="192.168.1.101", send_port=25565, dest_port=25577):
        self.ip_dst = ip_dst
        self.send_port = send_port
        self.dest_port = dest_port
        self.read_data = [0]
        self.charnum = 0

    def ingest(self, data):
        '''Ingests and formats data as a binary stream.'''
        if isinstance(data, str):
            self.data = [ord(i) for i in data]
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        '''Send an end-of-transmission packet to signal end of transmission.'''
        # Create short random string of four characters for final packet
        packet_string = urandom(4)
        # Create packet and send
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_delimiter(self, iface=None):
        """Sends a delimiter to signal the end of a specified data stream."""
        # Generate random string to go into packet based on number
        packet_string = urandom(512)
        # Create packet and send
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, number, packetDelay, iface=None):
        '''Sends packets based on the given number.'''
        for i in range(0, number):
            # Generate random string to go into packet based on number
            packet_string = urandom(1024)
            # Create packet and send
            pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
            if self.LOGLEVEL == DEBUG:
                send(pkt, verbose=True, iface=iface)
            else:
                send(pkt, verbose=False, iface=iface)
            # Packet delay
            if isinstance(packetDelay, int) or isinstance(packetDelay, float):
                debug("Packet delay sleep for {}s".format(packetDelay))
                sleep(packetDelay)

    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data
        for item in self.data:
            self.send_packet(item, packetDelay, iface)
            # Delimiter delay
            if isinstance(delimitDelay, int) or isinstance(delimitDelay, float):
                debug("Delimit delay sleep for {}s".format(delimitDelay))
                sleep(delimitDelay)
            self.send_delimiter(iface)

        # End delay
        if isinstance(endDelay, int) or isinstance(endDelay, float):
            debug("End delay sleep for {}s".format(endDelay))
            sleep(endDelay)
        self.send_EOT(iface)
        return True

    def packet_handler(self, pkt):
        '''Specifies the packet handler for receiving info via the UDP Size Modulation cloak.'''
        if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
            # Check for correct options
            if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port:
                length = len(pkt["Raw"].load)
                # Data received
                if length == 1024:
                    self.read_data[self.charnum] += 1
                # Delimiter received
                elif length == 512:
                    self.read_data[self.charnum] = chr(self.read_data[self.charnum])
                    debug("Received a '{}'".format(self.read_data[self.charnum]))
                    self.charnum += 1
                    self.read_data.append(0)

    def recv_EOT(self, pkt):
        '''Specifies the EOT packet, signaling the end of transmission.'''
        if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
            # Check for correct options
            if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port:
                length = len(pkt["Raw"].load)
                if length == 4:
                    removedelement = self.read_data.pop(self.charnum)
                    info("Received EOT")
                    return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the UDP Size Modulation Cloak."""
        info("Receiving packets...")
        self.read_data = [0]
        self.charnum = 0
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        self.read_data = "".join([str(i) for i in self.read_data])
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
