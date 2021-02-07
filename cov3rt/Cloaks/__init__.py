from importlib import import_module
from inspect import getmembers, isclass
from os import listdir
from os import name as OS_NAME
from cov3rt.Cloaks import Cloak as CloakLocation
from cov3rt.Cloaks.Cloak import Cloak 

# Get path for cov3rt
if OS_NAME == "nt":
    # Windows path
    COV3RT_PATH = "\\".join(CloakLocation.__file__.split("\\")[:-1])
else:
    COV3RT_PATH = '/'.join(CloakLocation.__file__.split('/')[:-1])

# Get all of the cloaks within the folder
files = listdir(COV3RT_PATH)
# Loop over the filenames
for filename in files:
    # Ignore these files and accept only python files
    if (filename not in ["__init__.py", "__pycache__", "Cloak.py"]) and (filename[-3:] == ".py"):
        # Grab the module name
        module_name = filename[:-3]
        # Add the file to our locals
        locals()[module_name] = getattr(import_module("cov3rt.Cloaks.{}".format(module_name)), module_name)
        
del COV3RT_PATH, OS_NAME, filename, files, getmembers, import_module, isclass, listdir, module_name, CloakLocation
