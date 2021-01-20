# from scapy.all import *
import argparse

# Argument parser
parser = argparse.ArgumentParser()

# Primary Arguments
required = parser.add_argument_group("Primary Arguments")
# Send and Receive
send_receive = required.add_mutually_exclusive_group(required = True)
send_receive.add_argument("-s", "--send", action="store_true", help="Send information via the selected cloak")
send_receive.add_argument("-r", "--receive", action="store_true", help="Receive information via the selected cloak")
# Message types
message_type = required.add_mutually_exclusive_group(required = True)
message_type.add_argument("-m", "--message", metavar="", action="store", type=str, help="Read from or print to command-line")
message_type.add_argument("-f", "--filename", metavar="", action="store", type=str, help="Read from or print to file")
# Cloak type
required.add_argument("-c", "--cloak", metavar="", type=int, action="store", help="selected covert channel implementation", required=True)

test = parser.add_argument_group("Cloak types")
test.add_argument("a", help="0 -> test")

delay_type = parser.add_argument_group("Delays")
delay_type.add_argument("-sd", "--startDelay", metavar="", type=float, action="store", help="delay before communication")
delay_type.add_argument("-ed", "--endDelay", metavar="", type=float, action="store", help="delay before end-of-transmission")
delay_type.add_argument("-dd", "--delimDelay", metavar="", type=float, action="store", help="delay between delimiters")
delay_type.add_argument("-pd", "--packetDelay", metavar="", type=float, action="store", help="delay between packets in seconds")

args = parser.parse_args()

if __name__ == "main":
    pass