from scapy.sendrecv import send, sniff
from scapy.layers.inet import IP, TCP
from scapy.utils import wrpcap

from logging import info, debug, DEBUG, WARNING
from re import search
from time import sleep
from os import urandom
from random import randint

from cov3rt.Cloaks.Cloak import Cloak

class TCPPatsySeqNumber(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "TCP Patsy using Sequence Number"
    description = "A cloak based on four characters per sequence number. Sender --> SYN w/ src ip of actual dst, seq = 4 chars --> patsy --> SYN RST seq++ --> Receiver seq--, extract message"
    
    def __init__(self, ip_dst="8.8.8.8", ip_patsy = "142.250.138.101"):
        self.ip_dst = ip_dst
        self.ip_patsy = ip_patsy
        self.read_data = ""
        
    def ingest(self,data):
        """Ingests and formats data into 32-bit binary string groups in a list."""
        if isinstance(data,str):
            # Prepare groups of four characters for sending later
            # First, convert the string into the binary equivalent of the characters in ASCII
            ordlist = [bin(ord(i))[2:].zfill(8) for i in data]
            # Combine that into a giant binary string
            datastring = "".join(ordlist)
            # Turn into an array of 32-bit groups, left-justified with zeros
            self.data = [(datastring[i:i+32].ljust(32,'0')) for i in range(0, len(datastring), 32)]
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        # EOT packet sends to patsy w/ src of destination, don't fragment, SYN flag, no payload.
        pkt = IP(dst = self.ip_patsy, src = self.ip_dst, flags = "DF")/TCP(flags = 0x02)/""
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True)
        else:
            send(pkt, verbose = False)

    def send_packet(self, num):
        """Sends packets based on TCP sequence number."""
        # We will use random data in a packet to indicate that there is an active message.
        payload = urandom(randint(15,100))
        # Packet w/ SYN Flag, don't fragment, payload of random bytes.
        pkt = IP(dst = self.ip_patsy, src = self.ip_dst, flags = "DF")/TCP(flags = 0x02, seq = num)/payload
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True)
        else:
            send(pkt, verbose = False)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data 
        for item in self.data:
            self.send_packet(int(item, 2))
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

    def packet_handler(self,pkt):
        """Specifies the packet handler for receiving information via the TCP Sequence Number Cloak."""
        if pkt.haslayer(TCP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].flags != 0x06:
                self.read_data += chr(pkt["TCP"].seq)
                debug("Received a '{}'".format(chr(pkt["TCP"].seq)))
                info("String: {}".format(self.read_data))


    def recv_EOT(self,pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].flags == 0x06:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        """Receives packets which use the TCP Sequence Number Cloak."""  
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
