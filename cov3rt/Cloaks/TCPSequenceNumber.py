from scapy.sendrecv import send, sniff
from scapy.layers.inet import IP, TCP

from logging import error, info, debug, DEBUG, WARNING
from time import sleep

from cov3rt.Cloaks.Cloak import Cloak

class TCPSequenceNumber(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "TCP Sequence Number"
    description = "A cloak based on changing the TCP sequence number \nASCII values."
    
    def __init__(self, ip_dst="8.8.8.8"):
        self.ip_dst = ip_dst
        self.read_data = ""

    def ingest(self,data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data,str):
            self.data = [ord(i) for i in data]
            debug(self.data)
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst = self.ip_dst, flags = 0x06)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = False)
        else:
            send(pkt, verbose = True)

    def send_packet(self, num):
        """Sends packets based on TCP sequence number."""
        pkt = IP(dst = self.ip_dst)/TCP(seq = num)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = False)
        else:
            send(pkt, verbose = True)

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
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
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
