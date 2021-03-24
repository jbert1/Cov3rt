from logging import info, debug, DEBUG, WARNING
from re import search
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class DNSCaseModulation(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.CASE_MODULATION
    name = "DNS Domain"
    description = "A cloak based on case modulation of a specified \ndomain."

    def __init__(self, ip_dst="8.8.8.8", domain="www.google.com"):
        self.ip_dst = ip_dst
        self.domain = domain
        self.read_data = ''

    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = ''.join(format(ord(i), 'b').zfill(8) for i in data)
            debug(self.data)
        else:
            raise TypeError("'data' must be of type 'str'")

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst=self.ip_dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=self.domain.capitalize()))
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, databit, iface=None):
        """Sends packets based on case modulation encoding."""
        if databit == '0':
            # Binary zero sends a lowercase domain name
            pkt = IP(dst=self.ip_dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=self.domain.lower()))
            if self.LOGLEVEL == DEBUG:
                send(pkt, verbose=True, iface=iface)
            else:
                send(pkt, verbose=False, iface=iface)
        elif databit == '1':
            # Binary one sends an uppercase domain name
            pkt = IP(dst=self.ip_dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=self.domain.upper()))
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
        """Specifies the packet handler for receiving information via the Case
        Modulated DNS Cloak."""
        # Ensure this is a DNS packet
        if pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
            # Check for correct options
            if pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == "{}.".format(self.domain.lower()).encode():
                # Binary zero value
                if pkt["DNSQR"].qname == "{}.".format(self.domain.lower()).encode():
                    self.read_data += '0'
                    debug("Received a '0'")
                # Binary one value
                elif pkt["DNSQR"].qname == "{}.".format(self.domain.upper()).encode():
                    self.read_data += '1'
                    debug("Received a '1'")
                info("Binary string: {}".format(self.read_data))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of
        transmission."""
        # Ensure this is a DNS packet
        if pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
            # Correct Options
            if pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname == "{}.".format(self.domain.capitalize()).encode():
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the Case Modulated DNS Cloak."""
        info("Receiving packets...")
        self.read_data = ''
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        # Decode read data
        string = ''
        # Loop over the data
        for i in range(0, len(self.read_data), 8):
            # Get the ascii character
            char = "0b{}".format(self.read_data[i:i + 8])
            # Add it to our string
            string = string + chr(int(char, 2))
        info("String decoded: {}".format(string))
        return string

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
