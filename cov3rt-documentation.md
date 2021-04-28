# Introduction to the cov3rt Framework
_A capstone project created by Justin Berthelot, Samuel Dominguez, Daniel Munger, and Christopher Rice at Louisiana Tech University for the Cyber Engineering Senior Design Symposium, Spring 2021_

## The Purpose of cov3rt
Despite the prevalence of covert channels in cyber attacks, no standardized tools exist for creation, management, and deployment of network covert channels. The cov3rt framework seets to provide developers, red teams, and network administrators with a python environment to integrate and deploy covert channels into their existing workflows. 

## Installation of cov3rt
The cov3rt framework is designed for **Python 3** (v3.4.1 or newer.)
The framework can be installed from PIP via
```sh
sudo pip install cov3rt
```
Because of the nature of sending network packets on reserved ports, cov3rt is required to run with administrator privileges (hence the _sudo_ installation requirement.)

The framework also uses _**npyscreen** v4.10.0_, _**scapy** v2.4.3_, and _**windows-curses** v2.2.0_ (for Windows installations only.) In normal cases, these dependencies should be automatically installed when cov3rt is installed via PIP. However, if required, these packages can also be installed separately through PIP.

***
***
***

# The Cloak Superclass (Cloak.py)
The cov3rt framework, as well as all cloak implementations, are built based on Cloak.py. All cloaks written for cov3rt inherit the Cloak superclass. This superclass contains standardized functions for interfacing with the cov3rt framework, such as the ability to ingest data and send/receive packets. Many of these functions are required in each cloak for the framework to function properly, with additional optional functions present as well. These functions are described within this documentation.
For more detailed information and implementation examples, please reference our example cloaks.

## Requirements for Cloaks
Each cloak is classified based on the [classification structure defined by Wendzel et al](http://ih-patterns.blogspot.com/p/test.html). Each of these classifications are offered as variables in the Cloak superclass. Each cloak implementation should specify its classification, such that it can be categorized correctly within the application. This is done through a class variable in a cloak, as shown below.
```py
class CloakExample(Cloak):
    ...
    classification = cloak.RANDOM_VALUE # list of valid classes found in Cloak.py
    ...
```

Each cloak implementation should also contain a name and description variable, following certain constraints to display correctly in the application. These are implemented via a class variable named 'name' and 'description', as shown below.
```py
class CloakExample(Cloak):
    ...
    name = "Name of My Cloak" # cannot be longer than 30 characters
    description = "This is a cloak with a long description to show how\
        \nline wrapping looks." # no longer than 53 characters per new line
    ...
```
Each cloak implementation must also implement the functionality for each required function, stated below in the next section. Below is a barebones example of a Cloak compatible with the cov3rt Framework.
```py
# This is a barebone example of a cloak's minimum requirements
from scapy.sendrecv import send,sniff
from cov3rt.Cloaks.Cloak import Cloak
from scapy.utils import wrpcap

class ExampleCloak(Cloak):
    # Class vars must meet requirements detailed earlier
    classification = Cloak.XXXXXXXXXXX
    name = "NAME HERE"
    description = "DESCRIPTION HERE"
    
    def __init__(self, ..., ...):
        # variables such as destination IP, sending port, etc should be defined here
        self.var1 = var1
        ...
        
    def ingest(self, data):
        ...
        
    def send_packet(self, data, iface=None):
        ...
        
    def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
        ...
    
    def packet_handler(self, pkt):
        ...
        
    def recv_packets(self, timeout=None, max_count=None, \
        iface=None, in_file=None, out_file=None):
        ...
        
    # We also recommend getters/setters for instance variables
    # var1 Getter
    @property
    def var1(self): 
        return self._var1
    # var1 Setter
    @var1.setter
    def var1(self, var1):
        ...
        self._var1 = var1
```
***
***
***
## Required Functions within Cloak.py
These functions are the **minimum** requirements for a Cloak to be compatible with the cov3rt framework. These functions provide base functionality for the framework to use a cloak, such as the ability to ingest data and send/receive packets. Additional optional functions exist as well for ease-of-use improvements such as End-of-Transmission functionalities and delimiters.
***
#### Ingest (ingest)
```
ingest(self, data)
    self : required argument
    data : can be any type as desired, this is the data to be sent by the Cloak
```
This function takes in a _data_ argument and formats said data to be used in a meaningful way within the cloak. Data can be of any type desired, as it is up to the developer to determine how to format and ingest their data. When data (ie input text, a string, etc.) is passed to a cloak through the cov3rt framework CLI/TUI, the _ingest_ function is called to accomplish this (hence why it is required.) Ingested data is recommended to be written to an instance variable such as _self.data_.
```py
# Example ingest function, using a str input converted to a binary string
# Taken from DNSTiming.py
def ingest(self, data):
    '''Ingests data and formats it as a binary string.'''
    if isinstance(data, str): # confirming input is a string
        # for each character, convert to binary and append to self.data
        self.data = ''.join(format(ord(i), 'b').zfill(8) for i in data)
    else:
        raise TypeError("'data' must be of type 'str'") # we recommend errors like this
```
***
#### Send Packets (send_packets)
```
send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None)
    self : required argument
    iface : 'str', a valid network interface on the machine to send packets on
    packetDelay : 'int' or 'float', delay between each packet sent
    delimitDelay : 'int' or 'float', delay before sending delimiter
    endDelay : 'int' or 'float', delay before sending EOT
```
This function performs the sending functionality of the cloak by calling the _send_packet_ function as desired by the developer. For example, if a cloak sends a character per packet, _send_packets_ may iterate over _self.data_, calling _send_packet_ for each iteration. This function should return _True_ once completed.
```py
# Example send_packets function, calling send_packet for each char in items of self.data
# Taken from IPMorse.py
def send_packets(self, iface=None, packetDelay=None, delimitDelay=None, endDelay=None):
    '''Sends the entire ingested data via the send_packet method.'''
    for item in self.data:
        for char in item:
            self.send_packet(char, iface)
            if isinstance(packetDelay, int) or isinstance(packetDelay, float):
                debug("Packet delay sleep for {}s".format(packetDelay))
                sleep(packetDelay)
        if isinstance(delimitDelay, int) or isinstance(delimitDelay, float):
            debug("Delimit delay sleep for {}s".format(delimitDelay))
            sleep(delimitDelay)
        self.send_delimiter(iface)
    
    # End delay
    if isinstance(endDelay, int) or isinstance(endDelay, float):
        debug("End delay sleep for {}s".format(endDelay))
        sleep(endDelay) 
    self.send_EOT(iface)
    return True
```

#### Send Packet (send_packet)
```
send_packet(self, data, iface=None)
    self : required argument
    data : can be of any type as desired, this is the data being sent in a packet
    iface : 'str', a valid network interface on the machine to send packets on
```
This function should be defined to take in a portion (or all) of _self.data_ and then craft and send a singular packet as part of the cloak. This can be accomplished by crafting a packet with Scapy and calling Scapy's _send_ function. _send_packet_ should be called within _send_packets_ in order to create and send network traffic.
```py
# Example send_packet function, sending data through case modulation of DNS requests
# Taken from DNSCaseModulation.py
def send_packet(self, databit, iface=None):
    '''Sends packets based on case modulation encoding.'''
    # Binary zero sends a lowercase domain name
    if databit == '0':
        pkt = IP(dst=self.ip_dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=self.domain.lower())
        send(pkt, verbose=False, iface=iface)
    # Binary one sends as capital domain name
    else:
        pkt = IP(dst=self.ip_dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=self.domain.upper())
        send(pkt, verbose=False, iface=iface)
```

#### Packet Handler for Sniff Function (packet_handler)
```
packet_handler(self, pkt)
    self : required argument
    pkt : Packet object, fed into the packet_handler as part of the sniff in recv_packets
```
This function specifies the packet handler used to filter packets as they are received. The _packet_handler_ function is passed to the _sniff_ function of Scapy in order to receive and process network traffic as part of the _recv_packets_ function. The packet handler's purpose is to analyze each packet to determine if it is part of the covert channel; if a packet is determined to be part of the channel, the packet handler will extract the hidden data from the packet, writing it to a variable (ie _self.read_data_.)
```py
# Example packet_handler function, receiving packets and determining important packets
# Taken from UDPChecksum.py
def packet_handler(self, pkt):
    '''Specifies the packet handler for receiving info via the UDP Checksum Cloak.'''
    # Check for appropriate layers (all others can immediately be ignored)
    if pkt.haslayer(UDP) and pkt.haslayer(IP) and pkt.haslayer(Raw):
        # Check for appropriate options specific to our cloak
        if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port \
            and pkt["UDP"].dport == self.dest_port:
            # We want all packets except for those with 0x9999 checksum
            if pkt["UDP"].chksum != 0x9999:
                self.read_data += chr(pkt["UDP"].chksum) # ASCII character checksum
                
# Used as part of recv_packets as shown
def recv_packets(...):
    ...
    packets = sniff(..., prn = self.packet_handler, ...)
    ...
```

#### Receive Packets (recv_packets)
```
recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None)
    self : required argument
    timeout : 'int' or 'float', time before exiting
    max_count : 'int', maximum number of packets received before exiting
    iface : 'str', a valid network interface on the machine to receive packets on
    in_file : 'str', path to a .pcap input file for static analysis purposes
    out_file : 'str', path to a desired output file for saving a .pcap of received traffic
```
This function receives packets in the cloak and then decodes the covert message. Scapy's _sniff_ function should be called within _recv_packets_, with _self.packet_handler_ being passed as the packet handler argument. Once the _sniff_ function returns, the extracted information can be decoded or returned as-is (depending on your implementation.) If the data decode step occurred on-the-fly in the _packet_handler_, you may only need to return _self.read_data_ without any extra steps.
```py
# Example recv_packets function, with decoding occurring within
# Taken from DNSCaseModulation.py
def recv_packets(self, timeout=None, max_count=None, iface=None, in_file=None, out_file=None):
    '''Receives packets for the DNSCaseModulation cloak and decodes message.'''
    self.read_data = '' # used to store received information
    if max_count: # for exit after a certain number of packets received
        packets = sniff(timeout=timeout, count=max_count, iface=iface, offline=in_file, \
            stop_filter=self.recv_EOT, prn=self.packet_handler)
    else: # standard case with no limit, awaits an EOT before exit
        packets = sniff(timeout=timeout, iface=iface, offline=in_file, \
            stop_filter=self.recv_EOT, prn=self.packet_handler)
    if out_file: # writes received packets to out_file
        wrpcap(out_file, packets)
    
    # Decode the read data
    string = ''
    # Convert to ASCII characters and add to decoded string
    for i in range(0, len(self.read_data), 8):
        char = "0b{}".format(self.read_data[i:i+8])
        string += chr(int(char, 2))
    
    return string
```
***
## Optional Functions within Cloak.py
These functions are provided to give additional flexibility to Cloak implementations, but are not required. These functions are implemented similarly to the required functions above.

#### Send End-of-Transmission Packet (send_EOT)
```
send_EOT(self, iface=None)
    self : required argument
    iface : 'str', a valid network interface on the machine to send packets on
```
This function sends an End-of-Transmission packet to signal the end of a covert message stream to a receiver. The _recv_EOT_ function should also be implemented if this function is used. This function should be called at the end of the _send_packets_ function.
```py
# Example send_EOT function to send a UDP packet with random data and a 0x9999 checksum
# Taken from UDPChecksum.py
def send_EOT(self, iface=None):
    '''Sends an EOT packet (checksum 0x9999) to signal the end of transmission.'''
    packet_string = urandom(randint(25,50))
    pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port, chksum=0x9999)\
        / Raw(packet_string)
    send(pkt, verbose=False, iface=iface)
```

#### Receive End-of-Transmission Packet (recv_EOT)
```
recv_EOT(self, pkt)
    self : required argument
    pkt: Packet object, fed into the recv_EOT as part of the sniff in recv_packets
```
This function works alongside the _packet_handler_ in the _sniff_ function to receive an End-of-Transmission packet. The _send_EOT_ function should also be implemented if this function is used. To use this function, it should be called in the _sniff_ function as the _stop_filter_ argument (example shown below.) This function should return _True_ if the EOT packet is received, and _False_ in any other case.
```py
# Example recv_EOT function, watching for a UDP packet with a 0x9999 checksum
# Taken from UDPChecksum.py
def recv_EOT(self, pkt):
    '''Specifies the EOT packet and returns True if packet is received.'''
    if pkt["IP"].dst == self.ip_dst and pkt["UDP"].sport == self.send_port \
        and pkt["UDP"].dport == self.dest_port:
        if (pkt["UDP"].chksum == 0x9999):
            return True
    return False
    
# Used as part of recv_packets function as shown
def recv_packets(...):
    ...
    packets = sniff(..., stop_filter = self.recv_EOT, ...)
    ...
```

#### Send Delimiter (send_delimiter)
```
send_delimiter(self, iface=None)
    self : required argument
    iface : 'str', a valid network interface on the machine to send packets on
```
This function sends a delimiter packet of choice to signal the end of a data stream to a receiver (for example, if you wanted to delimit per line or per character.) There is no corresponding _recv_delimiter_ function built in to Cloak.py -- we found it easier for delimiters to be extracted as part of the _packet_handler_ rather than trying to force in another method of detection. However, if desired, you could create a _recv_delimiter_ function and call it within the _packet_handler_.
An example of sending and receiving delimiters is shown below.
```py
# Example send_delimiter function (note similarity to send_EOT)
# Taken from IPMorse.py
def send_delimiter(self, iface=None):
    '''Sends delimiter packet to signify end of a Morse Code Character.'''
    packet_string = urandom(42)
    pkt = IP(dst=self.ip_dst) / UDP(sport=self.send_port, dport=self.dest_port) \
        / Raw(packet_string)
    send(pkt, verbose=False, iface=iface)

# Used as part of send_packets function as shown to send delimiter packets
def send_packets(...):
    ...
    for item in self.data:
        for char in item:
            ...
        ...
        self.send_delimiter(iface) # corresponds to end of an item
    ...

# Delimiters are received in packet_handler
def packet_handler(...):
    ...
    if pkt.haslayer(Raw): # do any filtering to see if packet matches requirements
        ...
        if length == 42: # this is what our delimiters have in our case
            # perform delimiter-specific action
            self.read_data += "/"
        ...
    ...
```
***
***
***

# The cov3rt Command Line Interface
The command line application parses through provided arguments to quickly deploy cloaks in the field for one-liner commands. In addition to the traditional message and file input, the command line application can take input from stdin and can therefore be "piped" with other shell commands.

## Command Line Options

### Primary Arguments
| Option | Description |
| ----- | ----- |
| -c | Selected covert channel implementation |
| -s | Send data via the selected cloak |
| -r | Receive data via the selected cloak |

### Send Options
| Option | Description |
| ----- | ----- |
| -m | Send a string message via the selected cloak |
| -f | Send file contents via the selected cloak |

### Receive Options
| Option | Description |
| ----- | ----- |
| -t | Timeout (in seconds) for the packet handler |
| -mc | Max number of packets for the packet handler |
| -in | Static analysis of a capture file |
| -of | Output the received message to a file |
| -op | Output the received packets to a capture file |

### Delay Options
| Option | Description |
| ----- | ----- |
| -pd | Delay between packets |
| -dd | Delay before each data delimeter |
| -ed | Delay before the end-of-transmission |

### Other Options
| Option | Description |
| ----- | ----- |
| -h | Display the help screen |
| -l | List the available cloaks in the current environment |
| -i | Launch the interactive TUI |
| -if | Select the network interface for cloak communication |
| -d | Use the default parameters for the selected cloak |
| -v | Increase verbosity of cloak communication |
| -vv | Further increase verbosity of cloak communication |

***
***
***

# The cov3rt Terminal User Interface
The cov3rt application includes a Terminal User Interface (TUI) which provides a more robust user experience. This TUI serves the purpose of providing the user with a simpler interface for those that are not as comfortable with a command-line interface.

The interactive TUI contains all the functionality of the command-line interface with the exception of receiving stdin. The interactive TUI includes extra functionality to list available network interfaces when the user plans to send or receive information with a selected cloak.

***
***
***

# Example Cloak Implementations
Each cloak in this section contains a description of its function and a brief overview of how it accomplishes its function. Specifics of the code are left to the actual Python files.
These cloak examples are meant to showcase the functionality of the cov3rt Framework -- not to be used in real use cases (however, some of them possibly could be.) Many of these examples are not very robust and exist to give developers examples of how to implement their own cloaks.
***
#### DNS Case Modulation (DNSCaseModulation.py)
**Classification**: Case Modulation

| Argument | Type | Description | 
| ----- | ----- | ------ |
| ip_dst | str | Destination IP Address |
| domain | str | Domain for sending modulated message |

**Description**: This cloak sends data based on the modulation of the case of a specified domain, _self.domain_. This cloak takes an input string (ASCII) and converts it to a binary string, and then sends the data via case modulation. This is accomplished by sending a lowercase domain (ie google.com) for '0' and an uppercase domain (ie GOOGLE.COM) for '1'.
***
#### DNS Timing (DNSTiming.py)
**Classification**: Inter-Packet Timing

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| domaindelim | str | Domain for EOT delimiting |
| domaincont | str | Domain for sending timing message |
| zerotiming | int / float | Delay between packets corresponding to '0' |
| onetiming | int / float | Delay between packets corresponding to '1' |

**Description**: This cloak sends data based on the delay between DNS Requests to a specified domain, _domaincont_. This cloak takes an input string (ASCII) and converts it to a binary string, and then sends the data by sending packets with corresponding delays between (_zerotiming_ / _onetiming_.)
***
#### ICMP Echo Full Payload (ICMPEchoFullPayload.py)
**Classification**: User Data Value Modulation (Reserved/Unused)

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |

**Description**: This cloak sends data within the payload of an ICMP Echo packet. The entire contents of the covert message are dumped directly into the payload and sent in plaintext.
***
#### ICMP Echo Multi Payload (ICMPEchoMultiPayload.py)
**Classification**: User Data Value Modulation (Reserved/Unused)

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |

**Description**: This cloak sends data within the payload of ICMP Echo packets. Each packet contains a single character of the covert message in plaintext within the payload of the packet.
***
#### IP Identification (IPID.py)
**Classification**: Random Value

| Argument | Type | Description |
| ----- | ----- | ----- |
| EOT_ID | int | Identification Number designated as an EOT flag |
| ip_dst | str | Destination IP Address |

**Description**: This cloak sends data by modifying the ID field of IP packets. The ID of each packet sent is overridden to correspond to a single ASCII character from the covert message.
***
#### IP Morse Code (IPMorse.py)
**Classification**: Reserved/Unused

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| send_port | int | Outbound port of covert channel on sender's machine |
| dest_port | int | Destination port of covert channel |

**Description**: This cloak converts a message into Morse Code and modifies the Reserved Bit field of IP packets to send the message covertly. This channel sends a single dot or dash per packet in the Reserved Bit field. After each full character is transmitted, a delimiter packet with a payload length of 42 is sent. A packet with a payload length of 679 designates the end of the transmission.
***
#### IP Reserved Bit (IPReservedBit.py)
**Classification**: Reserved/Unused

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |

**Description**: This cloak sends data by modulation of the Reserved Bit of IP packets. This cloak takes an input string (ASCII) and converts it to a binary string and sends one binary character per packet.
***
#### IPv6 "Hoppers" Hop Limit (IPv6Hoppers.py)
**Classification**: Random Value

| Argument | Type | Description |
| ----- | ----- | ----- |
| EOT_hl | int | Designated Hop Limit value for EOT packets |
| ip_dst | str | Destination IPv6 Address |

**Description**: This cloak sends data by overwriting the value of the Hop Limit field of IPv6 Packets. This cloak takes an input string (ASCII) and converts it to a binary string; A packet is sent for each character, replacing the Hop Limit field with the binary equivalent of the character. 
> Note: In this channel, the EOT is determined by a packet with a Hop Limit matching that of _EOT_hl_. Therefore, it is important that EOT_hl not be equal to a character within the covert message, or else the communication could be cut short.
***
#### TCP Patsy Four-Character Sequence Number (TCPFourCharPatsySeqNum.py)
**Classification**: Random Value

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| ip_patsy | str | Middle-man IP Address for bouncing TCP packets to destination |
| patsy_port | int | Port on _ip_patsy_ for bouncing TCP packets to destination |

**Description**: This cloak sends data by altering the value of the Sequence Number (SEQ) field of TCP packets and sending them to a "patsy" or intermediary machine. To achieve this "middle-man" bounce, the sender IP address is spoofed as the destination IP address, _ip_dst_. The patsy receives unsolicited TCP packets and sends a SYN-ACK response to _ip_dst_ (thinking it was the original sender), completing our transmission. The Acknowledgement (ACK) number of of the response will be equal to our original SEQ + 1, allowing us to retrieve the covert message. Each packet sent in this method delivers four ASCII characters per packet in the SEQ field; in a case where less than four characters are left to be transmitted, the SEQ is padded with zeros. The EOT is designated by a packet with no payload (while all other packets contain a randomized payload length.)

> Note: Any random IP address cannot work as a patsy. You must determine if the patsy address (and patsy port) will return packets when sent unsolicited TCP traffic. As a proof of concept, we tested this with a Raspberry Pi with the SSH port open. This setup was able to successfully bounce packets. Please note that in its current iteration, **this patsy only works for SYN-ACK responses**. If a patsy returns SYN-RST packets, you will likely encounter random data instead of the desired message. This is due to SYN-RST packets changing the ACK number based on the length of the payload.

> **Important Note:** This channel is by no means perfected. This type of communication bouncing is prone to packet retransmissions and out-of-order arrival. A list of received packets is kept and matched against to prevent duplicate portions of the message. However, no order preservation has been implemented. This could be implemented somewhat easily (by including some sort of sequencing information in the packets) and is left to future developers if desired.
***
#### TCP One-Character Sequence Number (TCPOneCharSeqNum.py)
**Classification**: Random Value

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| send_port | int | Outbound port of covert channel on sender's machine |
| dest_port | int | Destination port of covert channel |

**Description**: This cloak sends data by altering the value of the Sequence Number (SEQ) field of TCP packets. This cloak takes an input string (ASCII) and sends one packet per character, overwriting the SEQ number with the binary equivalent of the character. The EOT is designated as a packet with the IP Flags set to 0x06.
***
#### UDP Checksum (UDPChecksum.py)
**Classification**: Value Influencing

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| send_port | int | Outbound port of covert channel on sender's machine |
| dest_port | int | Destination port of covert channel |

**Description**: This cloak sends data by overwriting the checksum value of UDP packets. This cloak takes an input string (ASCII) and iterates over the string; For each character in the string, a UDP packet is sent with its checksum value set to the binary equivalent of the character. The payload of each packet contains fluff data, with the EOT packet also containing a checksum of 0x0000 rather than a character's value (ie 0x00D3.)
***
#### UDP Flood
**Classification**: Number of Elements

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| send_port | int | Outbound port of covert channel on sender's machine |
| dest_port | int | Destination port of covert channel |

**Description**: This cloak sends data by 'flooding' a destination with a number of packets corresponding to ASCII character values. Each packet sent has a randomized payload with a length of 1024. The receiver keeps count of the number of packets sent between delimiters in order to determine the character sent. A delimiter is designated as a packet with a payload length of 512. The EOT is designated as a packet with a payload length of 4.
***
#### UDP Size Modulation
**Classification**: User Data Value Modulation (Reserved/Unused)

| Argument | Type | Description |
| ----- | ----- | ----- |
| ip_dst | str | Destination IP Address |
| send_port | int | Outbound port of covert channel on sender's machine |
| dest_port | int | Destination port of covert channel |

**Description**: This cloak sends data by modulating the size of the payload of UDP packets. This cloak takes an input string (ASCII) and iterates over the data, sending packets whose payload lengths match the decimal ASCII values of each character of the data (ie payload length of 65 for 'A'.)
***
***
***
# Example Use Case for the cov3rt Framework: Teamserver Communication Application Proof-of-Concept
The cov3rt framework goes beyond sending and receiving messages and files directly with the CLI / TUI. The framework itself can be imported and called upon to perform actions for programs, such as a covert channel based team communication server. We have created a proof-of-concept implementation of a two-way teamserver for continuous communication over a selected cloak. The user can find, use, and inspect this tool in the "Tools" section of our file structure.
