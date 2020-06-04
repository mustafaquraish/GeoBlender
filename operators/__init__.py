'''
This file just serves as a place to list out all the operators in the folder,
so they can be imported as required by the other files.
'''
from bpy.types import Operator
import os

###############################################################################

# This dictionary stores a mapping between the operator classes and their
# corresponding panel hierarchy based on the directory structure in `operators`
# directory
operators_dict = {}

###############################################################################


files = []


def file_number(f1):
    '''
    This function just serves as a way to extract the initial number in front
    of the file / folder names to help sort them.
    '''
    try:
        return int(f1.split("_")[0])
    except BaseException:
        return 0


def get_files(folder, accum=None):
    '''
    Recursive find all of the files in the given folder, and construct the
    import path for them. `accum` is the accumulated import path.
    '''
    # For all directory elements
    for item in sorted(os.listdir(folder), key=file_number):
        itempath = os.path.join(folder, item)
        new_accum = f'{accum}.{item}' if accum is not None else item
        # If this is an operator file, add it to the `files` list
        if (os.path.isfile(itempath) and item != '__init__.py' and 
            item[0] != '.'):
            files.append(new_accum[:-3])  # [:-3] to remove the .py
        # If this is a directory, recurse
        elif os.path.isdir(itempath) and item != "__pycache__":
            get_files(itempath, new_accum)


# Get the directory of this folder (`operators`) and get all files.
path = os.path.dirname(os.path.abspath(__file__))
get_files(path)

with open("t.txt", "w") as f:
    for l in files:
        f.write(l+'\n')

# For each file
for py in files:

    # Import the file as a module
    mod = __import__('.'.join([__name__, py]), fromlist=[py])
    # Construct the Panel Hierarchy based on the file path
    op_path = [' '.join(f.split('_')[1:]) for f in py.split(".")[:-1]]

    # Get all the Operator classes
    classes = [getattr(mod, x)
               for x in dir(mod)
               if isinstance(getattr(mod, x), type)
               and issubclass(getattr(mod, x), Operator)]

    # Add the mapping between the operator and the hierarchy to the dict
    for cl in classes:
        operators_dict[cl] = op_path
