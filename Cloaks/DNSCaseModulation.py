from scapy.sendrecv import send, sniff
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from logging import error
from re import search
from time import sleep

from Cloak import Cloak

class DNSCaseModulation(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
    
    # Classification, name, and description
    classification = Cloak.CASE_MODULATION
    name = "DNS Domain"
    description = "A cloak based on case modulation of a specified domain."

    def __init__(self, ip_dst = "8.8.8.8", domain = "www.google.com"):
        self.ip_dst = ip_dst
        self.domain = domain + '.'
        self.read_data = ''
    
    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = ''.join(format(ord(i), 'b').zfill(8) for i in data)
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domain.capitalize()))
        send(pkt, verbose=False)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        """Sends the entire ingested data via the send_packet method."""
        # Loop over the data 
        for item in self.data:
            self.send_packet(item)
            # Packet delay
            if (isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                sleep(packetDelay)

        # End delay
        if (isinstance(endDelay, int) or isinstance(endDelay, float)):
            sleep(endDelay)
        self.send_EOT()
        return True

    def send_packet(self, databit):
        """Sends packets based on case modulation encoding."""
        if databit == '0':
            # Binary zero sends a lowercase domain name
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domain.lower()))
            send(pkt, verbose=False)
        elif databit == '1':
            # Binary one sends an uppercase domain name
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domain.upper()))
            send(pkt, verbose=False)
            

    def packet_handler(self, pkt):
        """Specifies the packet handler for receiving information via the Case Modulated DNS Cloak."""
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == self.domain.lower().encode()):
                if pkt["DNSQR"].qname == self.domain.lower().encode():
                    self.read_data += '0'
                elif pkt["DNSQR"].qname == self.domain.upper().encode():
                    self.read_data += '1'

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            # Correct Options
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname == self.domain.capitalize().encode()):
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        """Receives packets which use the Case Modulated DNS Cloak."""
        self.read_data = ''
        if max_count:
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        # Decode read data
        string = ''
        # Loop over the data
        for i in range(0, len(self.read_data), 8):
            # Get the ascii character
            char = "0b{}".format(self.read_data[i:i + 8])
            # Add it to our string
            string = string + chr(int(char, 2))
        return string

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