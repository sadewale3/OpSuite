import pathlib
from ._base import Job
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

# https://julienharbulot.com/python-dynamical-import.html
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in iter_modules([package_dir]):

    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute):            
            globals()[attribute_name] = attribute

for j in Job.__subclasses__():
    j.shortname = f"{j.__module__.split('.')[-1]}.{j.__name__}"