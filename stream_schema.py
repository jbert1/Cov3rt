from scapy.all import *
from string import printable
from random import choice
from re import search

# Example cloak
class Example(object):

    ## Constants ##
    IP_REGEX = "^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9 \][0-9]?)$"
    CLOAK_TYPE = "STREAM"

    # Constructor
    def __init__(self, ip_dst = "192.168.0.1", d_port = 12345, s_port = 23456):
        # Description for this cloak
        self.desc = "This cloak encodes data by changing the size of the UDP data payload"
        self.ip_dst = ip_dst
        self.d_port = d_port
        self.s_port = s_port
        self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw()
    
    # Ingest input data
    def ingest(self, data):
        self.data = [ord(i) for i in data]
        
    # Update data
    def update(self, data):
        # Create random string
        s = ""
        for i in range(data):
            s += choice(printable)
        # Update packet data
        self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw(s)
    
    # End of Transmission
    def EOF(self):
        # Create random string
        s = ""
        for i in range(4):
            s += choice(printable)
        # Update packet data
        self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw(s)
    
    # End of Text
    def EOT(self):
        # Create random string
        s = ""
        for i in range(3):
            s += choice(printable)
        # Update packet data
        self.packet = IP(dst=self.ip_dst)/UDP(sport=self.d_port, dport=self.s_port)/Raw(s)

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
                # FIND A BETTER WAY TO ERROR HANDLE!
                raise ValueError("Invalid IP '{}'".format(ip_dst))
        else:
            # FIND A BETTER WAY TO ERROR HANDLE!
            raise TypeError("'ip_dst' must be of type 'str'")
    
    # Getter for 'd_port'
    @property
    def d_port(self):
        return self._d_port
    
    # Setter for 'd_port'
    @d_port.setter
    def d_port(self, d_port):
        # Check type
        if isinstance(d_port, int):
            self._d_port = d_port
        else:
            # FIND A BETTER WAY TO ERROR HANDLE!
            raise TypeError("'d_port' must be of type 'int'")
        
    # Getter for 's_port'
    @property
    def s_port(self):
        return self._s_port
    
    # Setter for 's_port'
    @s_port.setter
    def s_port(self, s_port):
        # Check type
        if isinstance(s_port, int):
            self._s_port = s_port
        else:
            # FIND A BETTER WAY TO ERROR HANDLE!
            raise TypeError("'s_port' must be of type 'int'")
        


# Gets the arguments for the constructor
magic = vars(Example)['__init__'].__code__.co_varnames