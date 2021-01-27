#!/usr/bin/env python
# encoding: utf-8

import importlib, inspect
from os import listdir
from os import name as OS_NAME
from cov3rt.Cloaks import Cloak

# Get path for cov3rt
if OS_NAME == "nt":
    # Windows path
    COV3RT_PATH = "\\".join(Cloak.__file__.split("\\")[:-1])
else:
    COV3RT_PATH = '/'.join(Cloak.__file__.split('/')[:-1])

INTER_PACKET_TIMING = "Inter-Packet Timing"
MESSAGE_TIMING = "Message Timing"
RATE_THROUGHPUT_TIMING = "Rate/Throughput"
ARTIFICIAL_LOSS = "Artificial Loss"
MESSAGE_ORDERING = "Message (PDU) Ordering"
RETRANSMISSION = "Retransmission"
FRAME_COLLISIONS = "Frame Collisions"
TEMPERATURE = "Temperature"
SIZE_MODULATION = "Size Modulation"
POSITION = "Sequence: Position"
NUMBER_OF_ELEMENTS = "Sequence: Number of Elements"
RANDOM_VALUE = "Random Value"
CASE_MODULATION = "Value Modulation: Case"
LSB_MODULATION = "Value Modulation: LSB"
VALUE_INFLUENCING = "Value Modulation: Value Influencing"
RESERVED_UNUSED = "Reserved/Unused"
PAYLOAD_FIELD_SIZE_MODULATION = "Payload Field Size Modulation"
USER_DATA_CORRUPTION = "User-Data Corruption"
MODIFY_REDUNDANCY = "Modify Redundancy"
USER_DATA_VALUE_MODULATION_RESERVED_UNUSED = "User-Data Value Modulation & Reserved/Unused" 

cloaks =  {
    INTER_PACKET_TIMING : [
        "DNSTiming",
    ],

    MESSAGE_TIMING : [
    ],

    RATE_THROUGHPUT_TIMING : [
    ],

    ARTIFICIAL_LOSS : [
    ],

    MESSAGE_ORDERING : [
    ],

    RETRANSMISSION : [
    ],

    FRAME_COLLISIONS : [
    ],
    
    TEMPERATURE : [
    ],

    SIZE_MODULATION : [
        "UDPRaw",
    ],

    POSITION : [
    ],

    NUMBER_OF_ELEMENTS : [
    ],

    RANDOM_VALUE : [
        "IPv6Hoppers","TCP",
    ],

    CASE_MODULATION : [
        "DNSCaseModulation"
    ],

    LSB_MODULATION : [
    ],
    
    VALUE_INFLUENCING : [
    ],

    RESERVED_UNUSED : [
        "IPReservedBit"
    ],
    
    PAYLOAD_FIELD_SIZE_MODULATION : [
    ],

    USER_DATA_CORRUPTION : [
    ],

    MODIFY_REDUNDANCY : [
    ],

    USER_DATA_VALUE_MODULATION_RESERVED_UNUSED : [
    ],
}

b = []

def get_modules_in_package(filepath, package_name):
    # Get all of the cloaks within the folder
    files = listdir(filepath)
    # Loop over the filenames
    for filename in files:
        # Ignore these files and accept only python files
        if (filename not in ["__init__.py", "__pycache__", "Cloak.py"]) and (filename[-3:] == ".py"):
            # Grab the module name
            module_name = package_name + '.' + filename[:-3]
            # Get each class name and class in the file
            for classname, cls in inspect.getmembers(importlib.import_module(module_name), inspect.isclass):
                # Try-catch for odd imports
                try:
                    # Create the class import path
                    module_path = "{}.{}.{}".format(package_name, classname, classname)
                    # Get the class object path
                    imprt = str(cls).split("'")[1]
                    # Compare the paths and ignore the "Cloak" import
                    if (module_path == imprt) and (classname != "Cloak"):
                        b.append(cls)
                        print(imprt)
                        return True
                except:
                    pass
                # if cls.__module__ == module_name:
                #     yield cls

get_modules_in_package(COV3RT_PATH, "cov3rt.Cloaks")

