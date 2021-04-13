from os import listdir

# This will need to be changed when used in actual cov3rt
from cov3rt import Cloaks
from cov3rt.Cloaks import Cloak 
from inspect import getmembers, isclass, ismethod, signature
from logging import basicConfig, error, warning, info
from importlib import import_module
from sys import argv, exc_info
import threading
from time import sleep

module_path = "cov3rt.Cloaks."
cloak_list = {}
basicConfig(level=20)

# This class is to test out the recv_packets function in a cloak 
class RecvThread(threading.Thread):
    
    def __init__(self, testCloak):

        threading.Thread.__init__(self)
        self.testCloak = testCloak
        self.data = ""
        self.running = True

    def run(self):

        self.exc = None
        try:
            self.data = self.testCloak.recv_packets()
            self.running = False    

        except:
            self.exc = exc_info()
            self.running = False

    def join(self):
        if self.exc:
            raise self.exc

# Get filepath to user defined cloaks folder
def get_filepath():
    filepath = Cloaks.__file__
    return filepath[:-12]

# Create a dictionary with all User Defined Cloaks
def get_cloaks():
    global cloak_list
    files = listdir(get_filepath())
    counter = 0

    for i in range(len(files)):
        filename = files[i]
        if filename not in ["__init__.py", "__pycache__","Cloak.py"] and filename[-3:] == ".py":
            cloak_list[counter] = filename
            counter += 1
    return cloak_list

# List out all user defined cloaks
def list_cloaks():
    global cloak_list
    print("User Defined Cloaks:")
    for i in cloak_list:
        print("{} -> {}".format(i,cloak_list[i]))

# Test user defined cloaks
def testChosenCloak(cloak_list, num):

    global module_path
    moduleName = cloak_list[num]
    module_path = module_path + moduleName[:-3] 
    
    # First Test
    # Check if file is compileable
    try:
        module = import_module(module_path)
    
    except:
        # JUSTIN WRITE SOMETHING HERE PLEASE, THANKS... haha :)...
        error("Syntax error")
        exit(0)

    cls = getmembers(module, isclass)
    
    # Second Test 
    # Check to see if there is a cloak class
    if len(cls) < 1:
        error("No cloak class defined")
        exit(0)
    else:
        
        nameCheck = False
        
        # Third Test
        # Make sure name of class is the same as the name of the file
        for clsName in cls:
            if clsName[0] == moduleName[:-3]:
                moduleName = clsName[0]
                classInstance = clsName[1]
                nameCheck = True 
                break

        if not nameCheck:
            warning("Please make sure that class name matches file name.")
            exit(0)

        else:
           
            # Test to see if you can instantiate an instance of the class
            try:
                testCloak = classInstance()
            
            except:
                # Relatively big error
                error("Unable to instantiate class")
                exit(0)

            # Check to make sure that send_packets and recv_packets exist
            funcs = getmembers(testCloak, ismethod)
            counter = 0
            
            for func in funcs:
                if func[0] == "ingest":
                    counter += 1
                if func[0] == "send_packets":
                    counter += 1
                if func[0] == "recv_packets":
                    counter += 1

            if counter < 3:
                error("Make sure to define the ingest, send_packets and recv_packets function.")
                exit(0)
            
            # Get standard function parameters from cloak super class
            cloakCls = getmembers(Cloak, isclass)
            cloakIngestParams = str(signature(cloakCls[1][1].ingest).parameters)
            cloakSendParams = str(signature(cloakCls[1][1].send_packets).parameters)
            cloakRecvParams = str(signature(cloakCls[1][1].recv_packets).parameters)

            # Check paramters of ingest function compared to cloak super class
            testIngestParams = str(signature(classInstance.ingest).parameters)
            if testIngestParams != cloakIngestParams:
                warning("Make sure that your ingest parameters match the cloak super class!")

            # Check parameters of send_packets function compared to cloak super class
            testSendParams = str(signature(classInstance.send_packets).parameters)             
            if testSendParams != cloakSendParams:
                warning("Make sure that your send_packets parameters match the cloak super class!")

            # Check parameters of recv_packets function compared to cloak super class
            testRecvParams = str(signature(classInstance.recv_packets).parameters)
            if testRecvParams != cloakRecvParams:
                warning("Make sure that your recv_packets parameters match the cloak super class!")

            # Test to see if ingest function works properly for ASCII characters
            # Test with smallest and lowest printable ASCII characters
            try:
                testCloak.ingest(" ")
                testCloak.ingest("~")
            except:
                # Yo Justin you know how to write these better than me... <-----
                warning("Ingest function does not work with ASCII characters.")          
            
            # Testing send and receive functions for ASCII
            recv = RecvThread(testCloak)
            recv.start()
            sleep(2)
            
            # Checking send_packets function
            try:
                testCloak.send_packets()
            except:
                error("send_packets function did not function properly")
                exit(0)

            # Waiting for recv packets function to end
            # I NEED TO ADD A TTL TO THIS PART
            while(recv.running):
                sleep(1)

            # Checking recv_packets function
            try:
                recv.join()
            except:
                error("recv_packets function did not work")
                exit(0)

            # Make sure that data sent is the same as data received
            if recv.data != "~":
                warning("The cloak was not able maintain the integrity of the data in the send/receive process")

            # Starting recv_packets thread
            # For packet delay test
            recvPack = RecvThread(testCloak)
            recvPack.start()
            sleep(2)

            # Testing the packet delay parameter in send_packets
            try:
                testCloak.send_packets(packetDelay=2)
            except:
                warning("send_packets did not work with a packet delay")

            # I NEED TO ADD A TTL TO THIS PART
            while(recvPack.running):
                sleep(1)
            
            # Checking recv_packets function with a packet delay
            try:
                recvPack.join()
            except:
                warning("recv_packets function had an error when a packet delay was used in the send_packets function")
            
            # THIS MIGHT NEED TO GO IN THE TRY STATEMENT
            if recvPack.data != "~":
                warning("Data integrity was not maintained with a packet delay")
            
            # Starting recv_packets thread
            # For delimit delay test
            recvDelim = RecvThread(testCloak)
            recvDelim.start()
            sleep(2)
            # Testing the delimiter delay parameter in send_packets
            try:
                testCloak.send_packets(delimitDelay=2)
            except:
                warning("send_packets did not work with a delimiter delay")

            # I NEED TO ADD A TTL TO THIS PART
            while(recvDelim.running):
                sleep(1)

            # Checking recv_packets function with a delimiter delay
            try:
                recvDelim.join()
            except:
                warning("recv_packets function had an error when a delimiter delay was used in the send_packets function")
            
            # THIS MIGHT NEED TO GO IN THE TRY STATEMENT
            if recvDelim.data != "~":
                warning("Data integrity was not maintained with a delimiter delay")

            # Starting recv_packets thread
            # For end delay test
            recvEnd = RecvThread(testCloak)
            recvEnd.start()
            sleep(2)
            # Testing the end delay parameter in send_packets
            try:
                testCloak.send_packets(endDelay=2)
            except:
                warning("send_packets did not work with an end delay")

            # I NEED TO ADD A TTL TO THIS PART
            while(recvEnd.running):
                sleep(1)

            # Checking recv_packets function with an end delay
            try:
                recvEnd.join()
            except:
                warning("recv_packets function had an error when an end delay was used in the send_packets function")

            # THIS MIGHT NEED TO GO IN THE TRY STATEMENT
            if recvEnd.data != "~":
                warning("Data integrity was not maintained with an end delay")

            # Test if ingest function works properly for UTF-8 characters 
            try:
                testCloak.ingest("🐭 🧀")
            except:
                # Yo justin you might have to change this... haha :)...
                info("No cheese for the packet rat :(")
            
            # Testing send and receive functions for UTF-8
            recvUTF = RecvThread(testCloak)
            recvUTF.start()
            sleep(2)

            # Checking send_packets function
            try:
                testCloak.send_packets()
            except:
                warning("send_packets function did not function properly with UTF-8 data")

            # Waiting for recv packets function to end
            # I NEED TO ADD A TTL TO THIS PART
            while(recvUTF.running):
                sleep(1)

            # Checking recv_packets function with UTF-8 data
            try:
                recvUTF.join()
            except:
                warning("recv_packets function did not work with UTF-8 data")

            # Make sure that data sent is the same as data received
            if recvUTF.data != "🐭 🧀":
                warning("The cloak was not able maintain the integrity of the data in the send/receive process with UTF-8 data")
            print(recvUTF.data)

# Prints a typical help screen for usage information
def print_help():
    print("""Usage: python3 TestCloak.py [-h] [-l] -c cloak_id 
    Primary Arguments:
    -c,  --cloak          Selected covert channel implementation

    Other Arguments:
    -h,  --help           Show this help screen
    -l,  --listCloaks     List available cloaks"""
)        

# Hand written parser because argparse sucks
if ("-h" in argv or "--help" in argv or "?" in argv):
    print_help()
else:
    # Populate the cloak list
    cloak_list = get_cloaks()
    # List files
    if ("-l" in argv or "--list-cloaks" in argv):
        list_cloaks()
    # Cloak type
    elif ("-c" in argv or "--cloak" in argv):
        # Get the index in the arglist
        try:
            index = argv.index("-c")
        except:
            index = argv.index("--cloak")
        # Ensure the next positional argument is correct
        try:
            temp = argv[index + 1]
            # Check encoding
            if temp.isdigit():
                # Check range
                if 0 <= int(temp) <= len(cloak_list):
                    # Save cloak_type
                    cloak_type = int(temp)
                else:
                    error("Invalid cloak type!\nUse the '-l' option to view valid cloak types.")
                    exit()
            else:
                error("Invalid cloak type!\nUse the '-l' option to view valid cloak types.")
                exit()
        # Missing following positional argument
        except IndexError:
            error("Missing cloak type argument!\nUse the '-l' option to view valid cloak types.")
            exit()
        
        # Test the chosen cloak
        testChosenCloak(cloak_list, cloak_type)

    else:
        error("Please specify cloak type!")
        exit()

