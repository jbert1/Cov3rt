from scapy.sendrecv import send, sniff
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from logging import error
from re import search
from time import sleep

from Cloak import Cloak

'''Options:
IP_DST
DOMAIN_DELIM
DOMAIN_CONT
ZERO_TIMING
ONE_TIMING
'''

class DNSTiming(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"    
   
    def __init__(self, ip_dst = "8.8.8.8", domain_delim = "wikipedia.org", domain_cont = "twitter.com", zero_timing = 2, one_timing = 10):
        self.classification = Cloak.INTER_PACKET_TIMING
        self.name = "DNS"
        self.description = "A cloak based on delays between DNS requests to domains."
        self.ip_dst = ip_dst
        self.domaindelim = domain_delim + "."
        self.domaincont = domain_cont + "."
        self.zerotiming = zero_timing
        self.onetiming = one_timing
        self.read_data = []

    def ingest(self, data):
        '''Ingests and formats data as a binary stream.'''
        if isinstance(data, str):
            self.data = ''.join(format(ord(i), 'b').zfill(8) for i in data)
        else:
            error("'data' must be of type 'str'")

    def send_EOT(self):
        '''Send an end-of-transmission packet to signal end of transmission.'''
        pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaindelim.capitalize()))
        send(pkt, verbose = False)

    def send_packet(self, databit):
        '''Sends single packet with corresponding delay based on databit (0/1).'''
        if databit == '0':
            sleep(self.zerotiming)
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))
            send(pkt, verbose = False)
        elif databit == '1':
            sleep(self.onetiming)
            pkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))
            send(pkt, verbose = False)

    def send_packets(self, packetDelay = None, delimitDelay = None, endDelay = None):
        """Sends the entire ingested data via the send_packet method."""
        print("Sending data:")
        print(self.data)

        # Send an initial packet in order to start a baseline for delays.
        initpkt = IP(dst=self.ip_dst)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname = self.domaincont.capitalize()))
        send(initpkt, verbose=False)
        
        # Sends actual data.
        for item in self.data:
            self.send_packet(item)
            # Packet delay
            if (isinstance(packetDelay, int) or isinstance(packetDelay, float)):
                sleep(packetDelay)
        
        # End delay
        if (isinstance(endDelay, int) or isinstance(endDelay, float)):
            sleep(endDelay)
        # Sends EOT to confirm end of transmission.
        self.send_EOT()
        return True

    def packet_handler(self, pkt):
        '''Specifies the packet handler for receiving info via the DNS Timing Cloak.'''
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == self.domaindelim.lower().encode()):
                self.read_data.append(pkt)
            elif (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname.lower() == self.domaincont.lower().encode()):
                self.read_data.append(pkt)
        
    def recv_EOT(self, pkt):
        '''Specifies the EOT packet, singaling the end of transmission.'''
        if (pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt.haslayer(DNS) and pkt.haslayer(DNSQR)):
            # Correct Options
            if (pkt["IP"].dst == self.ip_dst and pkt["DNS"].rd == 1 and pkt["DNSQR"].qname == self.domaindelim.capitalize().encode()):
                return True
        return False

    def recv_packets(self, timeout = None, max_count = None, iface = None, in_file = None, out_file = None):
        '''Receives packets which use the DNS Timing Cloak.'''
        self.read_data = []
        print("Sniffing beginning...")
        if max_count:
            sniff(timeout = timeout, count = max_count, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        else:
            sniff(timeout = timeout, iface = iface, offline = in_file, store = out_file, stop_filter = self.recv_EOT, prn = self.packet_handler)
        # Decode the data collected, based on timings between packets
        print("Sniffing has ended, EOT received")
        string = ''
        current_time = None
        prev_time = None
        pktdif = 0
        
        # Loop over our data, ignoring last packet as it does not contain "data"
        for item in self.read_data[:-1]:
            # Set the prev_time to the last updated current_time (as it is now one behind)
            prev_time = current_time
            # Now, replace current_time with data from packet
            current_time = item.time
            # Compare difference, unless this is the first packet
            if prev_time == None:
                print("First packet ignored")
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

        print("Data has been reconverted to binary, output is")
        print(string)
        # Once our string has been populated, we can recreate the original data by reconverting
        output_string = ""
        # Loop over the data
        for i in range(0, len(string), 8):
            # Get the ascii character
            char = "0b{}".format(string[i:i + 8])
            # Add it to our string
            output_string = output_string + chr(int(char, 2))

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
        if (isinstance(zerotiming, float) or isinstance(zerotiming, int)):
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
        if (isinstance(onetiming, float) or isinstance(onetiming, int)):
            self._onetiming = onetiming
        else:
            error("'onetiming' must be of type 'float' or 'int'")