from scapy.all import *
from string import printable
from random import choice

IP_DST = "10.0.0.4"
S_PORT = 12345
D_PORT = 23456

# Get user input
user_input = input("Enter your secret phrase: ")

# Convert user input to an integer stream
stream = [ord(i) for i in user_input]

# Loop through the elements in the integer stream
for number in stream:
    # Create random string
    s = ""
    for i in range(number):
        s += choice(printable)
    # Create IP packet
    p = IP(dst=IP_DST)/UDP(sport=S_PORT, dport=D_PORT)/Raw(s)

    send(p, verbose=False)

# Signal end of transmission
# Create random string
s = ""
for i in range(4):
    s += choice(printable)
p1 = IP(dst=IP_DST)/UDP(sport=S_PORT, dport=D_PORT)/Raw(s)
send(p1, verbose=False)
