from importlib import import_module
from inspect import getmembers, isclass
from os import listdir
from cov3rt import UserCloaks as CloakLocation

# Initially set module name
module_name = ""
# Loop over the filenames within the UserCloaks folder
for filename in listdir('/'.join(CloakLocation.__file__.replace("\\", "/").split('/')[:-1])):
    # Ignore these files and accept only python files
    if filename not in ["__init__.py", "__pycache__"] and filename[-3:] == ".py":
        # Grab the module name
        module_name = filename[:-3]
        try:
            # Add the file to our locals
            locals()[module_name] = getattr(import_module("cov3rt.UserCloaks.{}".format(module_name)), module_name)
        except:
            print("Could not import {}!".format(module_name))

del filename, getmembers, import_module, isclass, listdir, module_name, CloakLocation