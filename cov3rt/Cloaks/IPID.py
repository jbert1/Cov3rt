from scapy.sendrecv import send, sniff
from scapy.layers.inet import IP
from scapy.utils import wrpcap

from logging import info, debug, DEBUG, WARNING
from re import search
from time import sleep

from cov3rt.Cloaks.Cloak import Cloak

class IPID(Cloak):
    
    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
    LOGLEVEL = WARNING

    # Classification, name, and description
    classification = Cloak.RANDOM_VALUE
    name = "IP Identification"
    description = "A covert channel using the Identification Field in \nIP packets to transmit messages."

    def __init__(self, EOT_ID = 20, ip_dst = "10.10.10.10"):
        self.ip_dst = ip_dst
        self.EOT_ID = EOT_ID
        self.read_data = []

    def ingest(self, data):
        """Ingests and formats data as a binary stream."""
        if isinstance(data, str):
            self.data = [ord(i) for i in data]
            debug(self.data)

    def send_EOT(self):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        pkt = IP(dst = "10.10.10.10")
        pkt.id = self.EOT_ID
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose = True)
        else:
            send(pkt, verbose = False)

    def send_packet(self, var_id):
        """Sends packets based on IP Identification Field."""
        pkt = IP(dst = "10.10.10.10")
        pkt.id = var_id
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
        """Specifies the packet handler for receiving information via the IP Identifiaction Cloak."""
        if (pkt.haslayer(IP)):
            if(pkt["IP"].dst == self.ip_dst):
                self.read_data.append(pkt.id)
                debug("Received {}".format(pkt.id))


    def recv_EOT(self,pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if (pkt.haslayer(IP)): 
            if (pkt["IP"].dst == self.ip_dst and pkt["IP"].id == self.EOT_ID):  
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        """Receives packets which use the IP Identification Cloak."""
        info("Receiving packets...")
        self.read_data = []
        if max_count:
            packets = sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            packets = sniff(timeout = timeout, iface = iface, offline = in_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        if out_file:
            wrpcap(out_file, packets)
        # Decode read data
        decoded_string = ''
        # Loop over the data
        for item in self.read_data[:-1]:
            # Get the ascii character and add it to our string
            decoded_string += chr(item)
        info("String decoded: {}".format(decoded_string))
        return decoded_string

    ## Getters and Setters ##
    # Getter for "ip_dst"
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for "ip_dst"
    @ip_dst.setter
    def ip_dst(self,ip_dst):
        # Ensure valid type:str
        if isinstance(ip_dst, str):
            # Ensure valid IP format
            if search(self.IP_REGEX, ip_dst):
                self._ip_dst = ip_dst
            else:
                raise ValueError("Invalid IP address provided: {}".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")
     

    # Getter for "EOT_ID"
    @property
    def EOT_ID(self):
        return self._EOT_ID

    # Setter for "EOT_ID"
    @EOT_ID.setter
    def EOT_ID(self, EOT_ID):
        if (isinstance(EOT_ID, int)):
            if (EOT_ID > 0 and EOT_ID < 65535):
                self._EOT_ID = EOT_ID
            else:
                raise ValueError("'EOT_ID' must be between 0 and 65535")
        else:
            raise TypeError("'EOT_ID' must be of type 'int'")
