from logging import info, debug, DEBUG, WARNING
from re import search
from scapy.layers.inet6 import IPv6
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak


class IPv6Hoppers(Cloak):

    # Regular expression to verify IP
    IPv6_REGEX = "(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))"
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "IPv6 Hoppers"
    description = "A covert channel using the hop limit in IPv6 \npackets to transmit messages."

    def __init__(self, EOT_hl=64, ip_dst="ff02::1:ffad:317"):
        self.ip_dst = ip_dst
        self.EOT_hl = EOT_hl
        self.read_data = []

    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = [ord(i) + self.EOT_hl if (ord(i) + self.EOT_hl) < 255 else 64 for i in data]
            debug(self.data)

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IPv6(dst=self.ip_dst, hlim=self.EOT_hl)
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_packet(self, var_hl, iface=None):
        """Sends packets based on hop limit."""
        pkt = IPv6(dst=self.ip_dst, hlim=var_hl)
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
        """Specifies the packet handler for receiving information via the IPv6 Hoppers Cloak."""
        if pkt.haslayer(IPv6):
            if pkt["IPv6"].dst == self.ip_dst:
                self.read_data.append(pkt.hlim)
                debug("Received {}".format(pkt.hlim))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(IPv6):
            if pkt["IPv6"].dst == self.ip_dst and pkt["IPv6"].hlim == self.EOT_hl:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the IPv6 Hoppers Cloak."""
        info("Receiving packets...")
        self.read_data = []
        if max_count:
            packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        else:
            packets = sniff(timeout=timeout, iface=iface, offline=in_file, stop_filter=self.recv_EOT, prn=self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        # Decode read data
        decoded_string = ''
        # Loop over the data
        for item in self.read_data[:-1]:
            # Get the ascii character and add it to our string
            decoded_string += chr(item - self.EOT_hl)
        info("String decoded: {}".format(decoded_string))
        return decoded_string

    # Getters and Setters
    # Getter for "ip_dst"
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for "ip_dst"
    @ip_dst.setter
    def ip_dst(self, ip_dst):
        # Ensure valid type:str
        if isinstance(ip_dst, str):
            # Ensure valid IP format
            if search(self.IPv6_REGEX, ip_dst):
                self._ip_dst = ip_dst
            else:
                raise ValueError("Invalid IP address provided: {}".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")

    # Getter for "ip_src"
    @property
    def ip_src(self):
        return self._ip_src

    # Setter for "ip_src"
    @ip_src.setter
    def ip_src(self, ip_src):
        # Ensure valid type:str
        if isinstance(ip_src, str):
            # Ensure valid IP format
            if search(self.IPv6_REGEX, ip_src):
                self._ip_src = ip_src
            else:
                raise ValueError("Invalid IP address provided: {}".format(ip_src))
        else:
            raise TypeError("'ip_src' must be of type 'str'")

    # Getter for "EOT_hl"
    @property
    def EOT_hl(self):
        return self._EOT_hl

    # Setter for "EOT_hl"
    @EOT_hl.setter
    def EOT_hl(self, EOT_hl):
        if isinstance(EOT_hl, int):
            if EOT_hl >= 64 and EOT_hl <= 127:
                self._EOT_hl = EOT_hl
            else:
                raise ValueError("'EOT_hl' must be between 64 and 127")
        else:
            raise TypeError("'EOT_hl' must be of type 'int'")
