from scapy.sendrecv import send, sniff
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from Cloak import Cloak
from logging import error
from re import search

'''Options:
IP_DST
DOMAIN_DELIM
DOMAIN_CONT
ZERO_TIMING
ONE_TIMING
'''

class DNSTiming(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9 \][0-9]?)$"

    def __init__(self, description = "A cloak based on delays between DNS requests to domains.", name="DNS Timing", ip_dst="8.8.8.8", DOMAIN_DELIM, DOMAIN_CONT, ZERO_TIMING, ONE_TIMING):
        self.description = description
        self.name = name
        self.ip_dst = ip_dst
        self.domaindelim = DOMAIN_DELIM + "."
        self.domaincont = DOMAIN_CONT + "."
        self.zerotiming = ZERO_TIMING
        self.onetiming = ONE_TIMING
        self.read_data = ""

    def ingest(self, data):
        '''Ingests and formats data as a binary stream.'''
        if isinstance(data, str):
            self.data = ''.join(format(ord(i), 'b').zfill(8) for i in user_input)
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        '''Send an end-of-transmission packet to signal end of transmission.'''
        pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaindelim.capitalize()))
        send(pkt, verbose=False)

    def send_packet(self, databit):
        '''Sends single packet with corresponding delay based on databit (0/1).'''
        if databit == '0':
            sleep(self.zerotiming)
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))
        elif databit == '1':
            sleep(self.onetiming)
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))

    def send_packets(self):
        '''Sends ingested data via the send_packet method.'''
        # Send an initial packet in order to start a baseline for delays.
        initpkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))
        self.send_packet(initpkt)
        # Sends actual data.
        for item in self.data:
            self.send_packet(item)
        # Sends EOT to confirm end of transmission.
        self.send_EOT()
        return True

    def packet_handler(self, pkt):
        '''Specifies the packet handler for receiving info via the DNS Timing Cloak.'''
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == self.domain.lower().encode()):
                pass # Not sure what I really need for this function, as my data processing
                # for the packets is entirely handled in recv_packets()

    def recv_EOT(self, pkt):
        '''Specifies the EOT packet, singaling the end of transmission.'''
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            # Correct Options
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname == self.domaindelim.capitalize().encode()):
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None):
        '''Receives packets which use the DNS Timing Cloak.'''
        self.read_data = ""
        sniff(timeout = timeout, stop_filter = self.recv_EOT, prn = self.packet_handler)
        # Decode the data collected, based on timings between packets
        string = ''
        current_time = None
        prev_time = None
        pktdif = 0
        # Loop over our data
        for item in range(0, len(self.read_data), 8):
            # Set the prev_time to the last updated current_time (as it is now one behind)
            prev_time = current_time
            # Now, replace current_time with data from packet
            current_time = item[UDP].time
            # Compare difference, unless this is the first packet
            if prev_time == None:
                continue
            # Otherwise, this means we have a valid prev_time and can take delays
            pktdif = current_time - prev_time

            # now, we need to determine if this was a zero or one by picking which is closer
            onediff = abs(self.onetiming - pktdif)
            zerodiff = abs(self.zerotiming - pktdif)

            # Whichever number is smaller will correspond to our data
            if zerodiff < onediff:
                string = string + '0'
            else:
                string = string + '1'
        
        # Once our string has been populated, we can recreate the original data by reconverting
        output_string = ""
        # List Comp to split our input into groups of 8 for easy decoding
        split_input = [string[i:i+n] for i in range(0, len(string), 8)]
        # Iterate through groups of 8, creating output data
        for item in split_input:
            asciichar = chr(int(item,2))
            output_string += asciichar
        
        return output_string

    ## Getters and Setters ##
    # Getter for 'ip_dst'
    @property
    def ip_dst(self):
        return self._ip_dst

    # Setter for 'ip_dst'
    @ip_dst.setter
    def ip_dst(self, ip_dst):
        # Ensure valid type: str
        if isinstance(ip_dst, str):
            # Ensure valid IP format
            if search(self.IP_REGEX, ip_dst):
                self._ip_dst = ip_dst
        # Not valid cases
            else:
                error("Invalid IP address provided: {}".format(ip_dst))
        else:
            error("'ip_dst' must be of type 'str'")

    # Getter for 'zerotiming'
    @property
    def zerotiming(self):
        return self._zerotiming
    
    # Setter for 'zerotiming'
    @zerotiming.setter
    def zerotiming(self, zerotiming):
        # Ensure valid type of int/float
        if isinstance(zerotiming, float):
            self._zerotiming = zerotiming
        elif isinstance(zerotiming, int):
            self._zerotiming = zerotiming
        else:
            error("'zerotiming' must be of type 'float' or 'int'")

    # Getter for 'onetiming'
    @property
    def onetiming(self):
        return self._onetiming
    
    # Setter for 'onetiming'
    @onetiming.setter
    def onetiming(self, onetiming):
        # Ensure valid type of int/float
        if isinstance(onetiming, float):
            self._onetiming = onetiming
        elif isinstance(onetiming, int):
            self._onetiming = onetiming
        else:
            error("'onetiming' must be of type 'float' or 'int'")