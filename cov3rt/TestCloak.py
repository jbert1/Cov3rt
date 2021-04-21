
from inspect import getmembers, isclass, ismethod, signature
from inspect import _empty as emptyParameter
from logging import basicConfig, error, warning, info
from importlib import import_module
from os import listdir
from sys import argv, exc_info
from threading import Thread
from time import sleep
from cov3rt import Cloaks, UserCloaks
from cov3rt.Cloaks import Cloak

cloak_list = {}

# This threading function listens for specific data from the recv_packets function
def recthread(recv_packets, checkdata):
    global TIMEOUT
    # Try to receive data
    try:
        data = recv_packets(timeout=TIMEOUT)
    except:
        print("Could not receive data in 'recv_packets' function!")
        return False
    # Blank data
    if data == "" or data is None:
        print("No data received!")
    # Incorrect data
    elif data != checkdata:
        print("Data was not properly received. Received: '{}' instead of '{}'!".format(
            ''.join([i if i.isprintable() else "?" for i in data]), checkdata))
        return False
    # Success
    else:
        print("Success!")


# Create a dictionary with all User Defined Cloaks
def get_cloaks():
    global cloak_list

    # Counter to enumerate the available cloaks
    counter = 0

    # Loop over the files in the path
    for filename in listdir(Cloaks.__file__[:-12]):
        if filename not in ["__init__.py", "__pycache__", "Cloak.py"] and filename[-3:] == ".py":
            cloak_list[counter] = (filename, "Cloaks.")
            counter += 1

    # Loop over the files in the path
    for filename in listdir(UserCloaks.__file__[:-12]):
        if filename not in ["__init__.py", "__pycache__", "Cloak.py"] and filename[-3:] == ".py":
            cloak_list[counter] = (filename, "UserCloaks.")
            counter += 1

    return cloak_list


# List out all user defined cloaks
def list_cloaks():
    global cloak_list
    print("User Defined Cloaks:")
    for i in cloak_list:
        print("  {} -> {}".format(i, cloak_list[i][0]))


# Test user defined cloaks
def testChosenCloak(cloak_list, num):

    module_path = "cov3rt.{}".format(cloak_list[num][1])
    moduleName = cloak_list[num][0]
    module_path = module_path + moduleName[:-3]

    # Check if module is importable
    try:
        module = import_module(module_path)
    # Could not import module
    except:
        error("Could not import module '{}'! Exiting...".format(moduleName[:-3]))
        exit(0)

    # Get the classes within the module
    cls = getmembers(module, isclass)
    # Check to see if there are classes within the module
    if len(cls) < 1:
        error("No classes found within the module '{}'! Exiting...".format(moduleName[:-3]))
        exit(0)
    # Classes exist in the module
    else:
        nameCheck = False
        # Make sure name of class is the same as the name of the file
        for clsName in cls:
            # Class name is the same as the module name
            if clsName[0] == moduleName[:-3]:
                # Save the module name
                moduleName = clsName[0]
                # Save the class itself
                classvar = clsName[1]
                # Set checker var to True
                nameCheck = True
                break
        # Class not found
        if not nameCheck:
            error("Cloak class must have the same name as the file / module '{}'! Exiting...".format(moduleName[:-3]))
            exit(0)
        # Get the parameters for the class constructor
        params = signature(classvar.__init__).parameters

        # Get parameter types as well
        # Add different type to list to be use later for test instantiation
        for param in params.keys():
            # Skip the 'self' parameter
            if param != "self":
                # Default value for the parameter is empty
                if params[param] == emptyParameter:
                    error("Parameter '{}' for the constructor has no default value! Exiting...".format(param))

        # Create an instance of the class
        try:
            cloakInstance = classvar()
        except:
            error("Unable to instantiate class '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check to make sure that send_packets and recv_packets exist
        funcs = getmembers(cloakInstance, ismethod)
        ingestBool = False
        sendBool = False
        recvBool = False

        # Loop over the functions in the class
        # Counter should equal 3 if all required functions exist
        for func, _ in funcs:
            if func == "ingest":
                ingestBool = True
            elif func == "send_packets":
                sendBool = True
            elif func == "recv_packets":
                recvBool = True

        # Function check
        if not ingestBool:
            error("'ingest' function not defined in the class '{}'! Exiting...".format(moduleName))
            exit(0)
        if not sendBool:
            error("'send_packets' function not defined in the class '{}'! Exiting...".format(moduleName))
            exit(0)
        if not recvBool:
            error("'recv_packets' function not defined in the class '{}'! Exiting...".format(moduleName))
            exit(0)

        # Get standard function parameters from cloak super class
        cloakIngestParams = signature(Cloak.Cloak.ingest).parameters
        cloakSendParams = signature(Cloak.Cloak.send_packets).parameters
        cloakRecvParams = signature(Cloak.Cloak.recv_packets).parameters

        # Check parameters of ingest function compared to cloak super class
        testIngestParams = signature(classvar.ingest).parameters
        missingparameter = False
        extraparameter = False
        # Loop over missing parameters
        for p in set(cloakIngestParams).difference(testIngestParams):
            print("Parameter '{}' not in ingest function!".format(p))
            missingparameter = True

        # Missing parameters exist
        if missingparameter:
            error("Parameters were missing in the ingest function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Loop over extra parameters
        for p in set(testIngestParams).difference(cloakIngestParams):
            print("Parameter '{}' not in superclass ingest function!".format(p))
            extraparameter = True

        # Extra parameters exist
        if extraparameter:
            error("Extra parameters were included in the ingest function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check order of parameters
        if str(testIngestParams) != str(cloakIngestParams):
            error("Order inconsistent for ingest parameters for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check parameters of send_packets function compared to cloak super class
        testSendParams = signature(classvar.send_packets).parameters
        missingparameter = False
        extraparameter = False
        # Loop over missing parameters
        for p in set(cloakSendParams).difference(testSendParams):
            print("Parameter '{}' not in send_packets function!".format(p))
            missingparameter = True

        # Missing parameters exist
        if missingparameter:
            error("Parameters were missing in the send_packets function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Loop over extra parameters
        for p in set(testSendParams).difference(cloakSendParams):
            print("Parameter '{}' not in superclass ingest function!".format(p))
            extraparameter = True

        # Extra parameters exist
        if extraparameter:
            error("Extra parameters were included in the send_packets function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check order of parameters
        if str(testSendParams) != str(cloakSendParams):
            error("Order inconsistent for send_packets parameters for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check parameters of recv_packets function compared to cloak super class
        testRecvParams = signature(classvar.recv_packets).parameters
        missingparameter = False
        extraparameter = False
        # Loop over missing parameters
        for p in set(cloakRecvParams).difference(testRecvParams):
            print("Parameter '{}' not in recv_packets function!".format(p))
            missingparameter = True

        # Missing parameters exist
        if missingparameter:
            error("Parameters were missing in the recv_packets function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Loop over extra parameters
        for p in set(testRecvParams).difference(cloakRecvParams):
            print("Parameter '{}' not in superclass ingest function!".format(p))
            extraparameter = True

        # Extra parameters exist
        if extraparameter:
            error("Extra parameters were included in the recv_packets function for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Check order of parameters
        if str(testRecvParams) != str(cloakRecvParams):
            error("Order inconsistent for recv_packets parameters for '{}'! Exiting...".format(moduleName))
            exit(0)

        # Let user know the status of the test function
        print("Status: Testing ASCII communication...")

        # Test to see if ingest function works properly for ASCII characters
        try:
            # Low 'value' printable ascii character
            cloakInstance.ingest(" ")
            # High 'value' printable ascii character
            cloakInstance.ingest("~")
        except:
            error("Ingest function failed with ascii characters! Exiting...")
            exit(0)

        # Start thread to listen for packets
        recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "~"], daemon=True)
        recv.start()
        # Give the receiver time to start up
        sleep(2)

        # Checking send_packets function
        try:
            cloakInstance.send_packets()
        except:
            error("Unable to send ascii characters! Exiting...")
            exit(0)

        # Wait for thread to complete
        while(recv.is_alive()):
            sleep(0.1)

        # Let user know the status of the test function
        print("\nStatus: Testing Packet Delay...")

        # Start thread to listen for packets
        recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "~"], daemon=True)
        recv.start()
        # Give the receiver time to start up
        sleep(2)

        # Testing the packet delay parameter in send_packets
        try:
            cloakInstance.send_packets(packetDelay=0.1)
        except:
            warning("'send_packets' function failed with packet delay!")

        # Wait for thread to complete
        while(recv.is_alive()):
            sleep(0.1)

        # Let user know the status of the test function
        print("\nStatus: Testing Delimiter Delay...")

        # Start thread to listen for packets
        recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "~"], daemon=True)
        recv.start()
        # Give the receiver time to start up
        sleep(2)

        # Testing the delimiter delay parameter in send_packets
        try:
            cloakInstance.send_packets(delimitDelay=2)
        except:
            warning("send_packets did not work with a delimiter delay")

        # Wait for thread to complete
        while(recv.is_alive()):
            sleep(0.1)

        # Let user know the status of the test function
        print("\nStatus: Testing End of Transmission Delay...")

        # Start thread to listen for packets
        recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "~"], daemon=True)
        recv.start()
        # Give the receiver time to start up
        sleep(2)

        # Testing the end delay parameter in send_packets
        try:
            cloakInstance.send_packets(endDelay=2)
        except:
            warning("send_packets did not work with an end delay")

        # Wait for thread to complete
        while(recv.is_alive()):
            sleep(0.1)

        # Let user know the status of the test function
        print("\nStatus: Testing UTF-8 Encoded Data...")
        skipUTF8 = False

        # Test if ingest function works properly for UTF-8 characters
        try:
            cloakInstance.ingest("✅")
        except:
            warning("Unable to ingest UTF-8 encoded data!")
            skipUTF8 = True

        if not skipUTF8:
            # Start thread to listen for packets
            recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "✅"], daemon=True)
            recv.start()
            # Give the receiver time to start up
            sleep(2)
            # Checking send_packets function
            try:
                cloakInstance.send_packets()
            except:
                warning("send_packets function did not function properly with UTF-8 data")
            # Wait for thread to complete
            while(recv.is_alive()):
                sleep(0.1)

        # Let user know the status of the test function
        print("\nStatus: Testing Long ASCII String...")

        # "Long" string of data
        try:
            cloakInstance.ingest("The quick brown fox jumped over the lazy dog.")
        except:
            error("Ingest function failed with long ascii message! Exiting...")
            exit(0)

        # Start thread to listen for packets
        recv = Thread(target=recthread, args=[cloakInstance.recv_packets, "The quick brown fox jumped over the lazy dog."], daemon=True)
        recv.start()
        # Give the receiver time to start up
        sleep(2)

        # Checking send_packets function
        try:
            cloakInstance.send_packets()
        except:
            warning("Long run was not able to be sent")

        # Wait for thread to complete
        while(recv.is_alive()):
            sleep(0.1)

        print("\nFinished testing the '{}' cloak!".format(moduleName))


# Prints a typical help screen for usage information
def print_help():
    print("""Usage: python3 TestCloak.py [-h] [-l] -c cloak_id 
    Primary Arguments:
    -c,  --cloak          Selected covert channel implementation

    Other Arguments:
    -h,  --help           Show this help screen
    -l,  --listCloaks     List available cloaks
    -t,  --timeout        Specifify timeout for listener
                          (could cause infinite loop!)"""
          )


# Hand written parser because argparse sucks
if ("-h" in argv or "--help" in argv or "?" in argv):
    print_help()
else:
    # Timeout
    if ("-t" in argv or "--timeout" in argv):
        # Get the index in the arglist
        try:
            index = argv.index("-t")
        except:
            index = argv.index("--timeout")
        # Ensure the next positional argument is correct
        try:
            temp = argv[index + 1]
            # Check type
            if temp.isdigit():
                TIMEOUT = int(temp)
            else:
                error("Timeout value must be of type 'float'!")
                exit()
        # Missing following positional argument
        except IndexError:
            error("Missing timeout value!")
            exit()
    else:
        # Default to 10 seconds
        TIMEOUT = 10
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
