import bpy

def make_driver_list(obj, prop, fields):
    '''
    Form a list of drivers for the required fields on an object property.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', 'rotation_euler', ...)
    fields:    Fields of prop.      (String, explained below)

    `fields` is a string containing one or more of the characters 'X', 'Y' and 'Z'
    denoting which of the fields need to have a driver set.

    for example, 'XY' means the X and Y fields have a new driver created for them.
    '''
    driver_list = []
    for axis in fields:
        idx = "XYZ".index(axis.upper())
        driver_list.append(obj.driver_add(prop, idx))
    return driver_list 

def add_driver_distance(obj, prop, fields, A, B):
    '''
    Add a driver for an object's properties, set to the distance from A to B.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', 'rotation_euler', ...)
    fields:    Fields of prop.      (String, look at `make_driver_list`)
    A, B:      The 2 Objects        (Blender Objects)
    '''
    # Add the needed drivers to the object
    driver_list = make_driver_list(obj, prop.lower(), fields)

    # Set the drivers to the distance
    for driver in driver_list:
        # Create a variable
        var = driver.driver.variables.new()
        var.name = 'dist'
        var.type = 'LOC_DIFF'
        # Set the two objects 
        var.targets[0].id = A
        var.targets[1].id = B 
        # Setting the type to avg. uses the single value
        driver.driver.type = 'AVERAGE'