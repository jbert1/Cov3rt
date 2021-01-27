#!/usr/bin/env python
# encoding: utf-8

import importlib, inspect
from os import listdir, name
from cov3rt.Cloaks import Cloak

# Get path for cov3rt
if name == "nt":
    # Windows path
    COV3RT_PATH = "\\".join(Cloak.__file__.split("\\")[:-1])
else:
    COV3RT_PATH = "/".join(Cloak.__file__.split("/")[:-1])

b = []

def get_modules_in_package(package_name: str):
    files = listdir(package_name)
    for file in files:
        if file not in ['__init__.py', '__pycache__']:
            if file[-3:] != '.py':
                continue

            file_name = file[:-3]
            module_name = package_name + '.' + file_name
            for n, cls in inspect.getmembers(importlib.import_module(module_name), inspect.isclass):
                b.append((n , cls))
                # if cls.__module__ == module_name:
                #     yield cls

a = get_modules_in_package("cov3rt")

