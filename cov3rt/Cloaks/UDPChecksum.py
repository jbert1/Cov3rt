from logging import info, debug, DEBUG, WARNING
from os import urandom
from random import randint
from re import search
from scapy.all import Raw
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class UDPChecksum(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.VALUE_INFLUENCING
    name = "UDP Checksum"
    description = "A cloak based on replacement of the UDP Checksum with\nuser data."

    def __init__(self, ip_dst="192.168.1.101", send_port=25565, dest_port=25577):
        self.ip_dst = ip_dst
        self.send_port = send_port
        self.dest_port = dest_port
        self.read_data = ""

    def ingest(self, data):
        '''Ingests and formats data as a binary stream.'''
        if isinstance(data, str):
            self.data = []
            for i in data:
                ordval = ord(i)
                # If the value is within acceptable range (checksum 0x9999, dec 39321)
                if ordval < 39321:
                    self.data.append(ordval)
                # Otherwise, replace the invalid with an @ (chr 64)
                else:
                    self.data.append('64')
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        '''Send an end-of-transmission packet (checksum 0x9999) to signal end of transmission.'''
        # Generate random string to go into packet payload
        packet_string = urandom(randint(25, 50))

        # Create packet with fluff payload and checksum of all 0
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port, chksum=0x9999) / Raw(packet_string)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, userdata, iface=None):
        '''Sends single packet with checksum based on user data.'''
        # Generate random string to go into packet payload
        packet_string = urandom(randint(25, 50))

        # Create packet with fluff payload and checksum of userdata
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port, chksum=int(userdata)) / Raw(packet_string)
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
        '''Specifies the packet handler for receiving info via the UDP Checksum cloak.'''
        if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
            # Check for correct options
            if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port:
                if pkt["UDP"].chksum != 0x9999:
                    self.read_data += chr(pkt["UDP"].chksum)
                    debug("Received a {}".format(chr(pkt["UDP"].chksum)))
                    info("String: {}".format(self.read_data))

    def recv_EOT(self, pkt):
        '''Specifies the EOT packet, singaling the end of transmission. Checksum of 0x9999 for this channel.'''
        if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
            # Check for correct options
            if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port and pkt["UDP"].dport == self.dest_port:
                if (pkt["UDP"].chksum == 0x9999):
                    return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the UDP Checksum Cloak."""
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
