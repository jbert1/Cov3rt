from logging import info, debug, DEBUG, WARNING
from os import urandom
from random import randint
from re import search
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class TCPFourCharPatsySeqNum(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "TCP Patsy 4-Char Seq Number"
    description = "A cloak based on changing the TCP sequence number\nto 4 ascii characters while using a patsy."

    def __init__(self, ip_dst="192.168.1.3", ip_patsy="192.168.1.26", patsy_port=22):
        self.ip_dst = ip_dst
        self.ip_patsy = ip_patsy
        self.patsy_port = patsy_port
        self.read_data = ""
        self.packets_recv = []

    def ingest(self, data):
        """Ingests and formats data into 32-bit binary string groups in a list."""
        if isinstance(data,str):
            # Prepare groups of four characters for sending later
            # First, convert the string into the binary equivalent of the characters in ASCII
            ordlist = [bin(ord(i))[2:].zfill(8) for i in data]
            # Combine that into a giant binary string
            datastring = "".join(ordlist)
            # Turn into an array of 32-bit groups, left-justified with zeros
            self.data = [(datastring[i:i+32].ljust(32, '0')) for i in range(0, len(datastring), 32)]
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of
        transmission."""
        # EOT packet sends to patsy w/ src of destination, don't fragment, SYN flag, no payload
        # no payload will be interpreted as pkt.load == b''
        pkt = IP(dst=self.ip_patsy, src=self.ip_dst, flags="DF") / TCP(flags=0x02, sport=21, dport=self.patsy_port) / ""
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose = False, iface=iface)

    def send_packet(self, num, iface=None):
        """Sends packets based on TCP sequence number."""
        # We will use random data in a packet to indicate that there is an active message
        payload = urandom(randint(15,100))
        # Packet w/ SYN Flag, don't fragment, payload of random bytes
        pkt = IP(dst=self.ip_patsy, src=self.ip_dst, flags="DF") / TCP(flags=0x02, seq=num, sport=randint(20,300), dport=self.patsy_port) / payload
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True, iface=iface)
        else:
            send(pkt, verbose = False, iface=iface)

    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data 
        for item in self.data:
            self.send_packet(int(item, 2), iface)
            sleep(0.1)
            # Packet delay
            if (isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                debug("Packet delay sleep for {}s".format(packetDelay))
                sleep(packetDelay)

        # End delay
        if (isinstance(endDelay, int) or isinstance(endDelay, float)):
            debug("End delay sleep for {}s".format(endDelay))
            sleep(endDelay)
        self.send_EOT(iface)
        return True

    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the TCP Patsy Cloak."""
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].src == self.ip_patsy and pkt["TCP"].ack != 1:
                # If we've already received this packet, it is a retransmit and we should ignore it
                if pkt in self.packets_recv:
                    return
                # If we have not already received it, add it to our packet array
                self.packets_recv.append(pkt)
                fourcharstring = bin((pkt["TCP"].ack - 1))[2:].zfill(32)
                fourchars = [fourcharstring[i:i+8] for i in range(0, 32, 8)]
                for item in fourchars:
                    self.read_data += chr(int(item, 2))
                info("String: {}".format(self.read_data))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].src == self.ip_patsy and pkt["TCP"].ack == 1:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the TCP Patsy Cloak."""
        info("Receiving packets...")
        self.read_data = ''
        self.packets_recv = []
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        info("String decoded: {}".format(self.read_data))
        # trim off excess \x00 if required, up to 3
        if self.read_data.endswith('\x00\x00\x00'):
            self.read_data = self.read_data[:-3]
        elif self.read_data.endswith('\x00\x00'):
            self.read_data = self.read_data[:-2]
        elif self.read_data.endswith('\x00'):
            self.read_data = self.read_data[:-1]
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
                raise ValueError("Invalid IP '{}'".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")

    # Getter for 'ip_patsy'
    @property
    def ip_patsy(self):
        return self._ip_patsy
    
    # Setter for 'ip_patsy'
    @ip_patsy.setter
    def ip_patsy(self, ip_patsy):
        # Check type
        if isinstance(ip_patsy, str):
            # Check if a valid IP
            if search(self.IP_REGEX, ip_patsy):
                self._ip_patsy = ip_patsy
            # Not a valid IP
            else:
                raise ValueError("Invalid IP '{}'".format(ip_patsy))
        else:
            raise TypeError("'ip_patsy' must be of type 'str'")

    # Getter for 'patsy_port'
    @property
    def patsy_port(self):
        return self._patsy_port

    # Setter for 'patsy_port'
    @patsy_port.setter
    def patsy_port(self, patsy_port):
        # Check type
        if isinstance(patsy_port, int):
            # Now check if valid range
            if 0 <= patsy_port <= 65535:
                self._patsy_port = patsy_port
            # Not valid port range
            else:
                raise ValueError("Invalid port number '{}'".format(patsy_port))
        else:
            raise TypeError("'patsy_port' must be of type 'int'")
