'''
This file just serves as a place to list out all the operators in the folder,
so they can be imported as required by the other files.
'''

import os

###############################################################################

# This is the list of operators that will be imported by other modules. 
operator_list = []

###############################################################################

# Form a list of all the files in the current directory
path = os.path.dirname(os.path.abspath(__file__))
files = [fname[:-3]
         for fname in os.listdir(path)
         if fname.endswith('.py') and fname != '__init__.py']


# For each file
for py in files:
    # Import the file as a module
    mod = __import__('.'.join([__name__, py]), fromlist=[py])
    # Get all the classes
    classes = [getattr(mod, x)
               for x in dir(mod)
               if isinstance(getattr(mod, x), type)]
    # Add them onto the list
    operator_list += classes
