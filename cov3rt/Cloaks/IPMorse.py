from logging import info, debug, DEBUG, WARNING
from os import urandom
from re import search
from scapy.layers.inet import IP, UDP
from scapy.all import Raw
from scapy.sendrecv import send, sniff
from scapy.utils import wrpcap
from time import sleep
from cov3rt.Cloaks.Cloak import Cloak

morse_code = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}


class IPMorse(Cloak):

    # Regular expression to verify IP
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    LOGLEVEL = WARNING
    # Classification, name, and description
    classification = Cloak.RESERVED_UNUSED
    name = "IP Morse Code"
    description = "A covert channel using Morse Code to transmit messages."

    def __init__(self, ip_dst="10.10.10.10", send_port = 31337, dest_port = 12345):
        self.ip_dst = ip_dst
        self.send_port = send_port
        self.dest_port = dest_port
        self.read_data = []


    def ingest(self, data):
        """Ingests and encodes data into Morse Code."""
        if isinstance(data, str):
            uppercase = data.upper()
            allowable_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890?()/.,"
            self.data = []
            for character in uppercase:
                if character in allowable_chars:
                    self.data.append(morse_code[character])
                #Space Case
                elif character == " ":
                    self.data.append(" ")
                else:
                    raise ValueError("Invalid Character Entered: {}".format(character))
            debug(self.data)

    def send_EOT(self, iface=None):
        """Sends an end-of-transmission packet to signal the end of transmission."""
        packet_string = urandom(1738)
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)  
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)

    def send_delimiter(self, iface=None):
        """Sends delimiter packet to signify end of Morse Code character. """
        packet_string = urandom(42)
        pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
    
        if self.LOGLEVEL == DEBUG:
            send(pkt, verbose=True, iface=iface)
        else:
            send(pkt, verbose=False, iface=iface)    

    def send_packet(self, dotdashorspace, iface=None):
        """Sends packets based on the evil bit."""
        if dotdashorspace == '.':
            # "." or Binary zero sends a non-evil bit packet
            pkt = IP(dst=self.ip_dst, flags=0x00) / UDP(sport=self.send_port, dport=self.dest_port)
            if self.LOGLEVEL == DEBUG:
                send(pkt, verbose=True, iface=iface)
            else:
                send(pkt, verbose=False, iface=iface)

        elif dotdashorspace == '-':
            # "-" or Binary one sends an evil bit packet
            pkt = IP(dst=self.ip_dst, flags=0x04) / UDP(sport=self.send_port, dport=self.dest_port)
            if self.LOGLEVEL == DEBUG:
                send(pkt, verbose=True, iface=iface)
            else:
                send(pkt, verbose=False, iface=iface)
        
        elif dotdashorspace == " ":
            # If the character is a space, an arbitrary payload length will be chosen
            packet_string = urandom(1337)
            pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) / Raw(packet_string)
            
            if self.LOGLEVEL == DEBUG:
                send(pkt, verbose=True, iface=iface)
            else:
                send(pkt, verbose=False, iface=iface)

    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        """Sends the entire ingested data via the send_packet method."""
        info("Sending packets...")
        # Loop over the data
        for item in self.data:
            for char in item:
                self.send_packet(char, iface)
            self.send_delimiter(iface)
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
        """Specifies the packet handler for receiving information via the IP Identifiaction Cloak."""
        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst:
                self.read_data.append(pkt.id)
                debug("Received {}".format(pkt.id))

    def recv_EOT(self, pkt):
        """Specifies the end-of-transmission packet that signals the end of transmission."""
        if pkt.haslayer(IP):
            if pkt["IP"].dst == self.ip_dst and pkt["IP"].id == self.EOT_ID:
                info("Received EOT")
                return True
        return False

    def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
        """Receives packets which use the IP Identification Morse Code Cloak."""
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
            decoded_string += chr(item)
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
            if search(self.IP_REGEX, ip_dst):
                self._ip_dst = ip_dst
            else:
                raise ValueError("Invalid IP address provided: {}".format(ip_dst))
        else:
            raise TypeError("'ip_dst' must be of type 'str'")

    # Getter for "send_port"
    @property
    def send_port(self):
        return self._send_port
  
    # Getter for "dest_port"
    @property
    def dest_port(self):
        return self._dest_port    

    # Setter for "send_port"
    @send_port.setter
    def send_port(self, send_port):
        if isinstance(send_port, int):
            if send_port > 0 and send_port < 65535:
                self._send_port = send_port
            else:
                raise ValueError("'send_port' must be between 0 and 65535")
        else:
            raise TypeError("'send_port' must be of type 'int'")
    
    # Setter for "dest_port"
    @dest_port.setter
    def dest_port(self, dest_port):
        if isinstance(dest_port, int):
            if dest_port > 0 and dest_port < 65535:
                self._dest_port = dest_port
            else:
                raise ValueError("'dest_port' must be between 0 and 65535")
        else:
            raise TypeError("'dest_port' must be of type 'int'")