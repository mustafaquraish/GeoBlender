'''
Driver-related utilites to simplify adding drivers to objects without
the boilerplate.
'''

transform_props = {
    'scale': 'SCALE_',
    'location': 'LOC_',
    'rotation': 'ROT_',
}


def make_driver_list(obj, prop, fields):
    '''
    Form a list of drivers for the required fields on an object property.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
    fields:    Fields of prop.      (String, explained below)

    `fields` is a string containing one or more of the characters 'X', 'Y', 'Z'
    denoting which of the fields need to have a driver set.

    for example, 'XY' means the X and Y fields have a new driver created.
    '''
    driver_list = []
    for axis in fields:
        idx = "XYZ".index(axis.upper())
        driver_list.append(obj.driver_add(prop, idx))
    return driver_list


def add_driver_distance(obj, prop, fields, A, B, scale=1):
    '''
    Add a driver for an object's properties, set to the distance from A to B.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
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
        # Set the expression
        driver.driver.expression = f'{scale} * {var.name}'


def add_driver(obj, prop, fields, vars_def, expr):
    '''
    Add a driver for an object's properties, using the transform channels of
    other objects.

    TODO: Support other variable modes including `Single property`, ...
    TODO: Support other `spaces` for channels other than WORLD space

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
    fields:    Fields of prop.      (String, look at `make_driver_list`)
    vars_def:  Variable defns.      (Look Below)
    expr:      Driver Expression    (String)

    Variable definitions are a dictionary with the following format:
    { var_name: (target_object, prop, field) }
    where:
        target_obj: Blender Object
        prop: 'SCALE', 'LOC' or 'ROT'
        field: 'X', 'Y', 'Z', 'W', '-'
            - Note: if this value is `-`, then the corresponding destination
                field is used. So, for the driver for the `X` component the
                value of the `X` field will be used, etc. Useful to set the
                X-Y-Z components of the destination based on the X-Y-Z
                components of the source.

    For example, to represent `x = Cube.scale[1]`,
    { x: (Cube, 'scale', 'Y') }
    '''
    # Add the needed drivers to the object
    driver_list = make_driver_list(obj, prop.lower(), fields)

    # Set the drivers to the distance
    for driver in driver_list:
        # For each variable definition
        for var_name in vars_def:
            # Get the details of the definition
            (t_obj, t_prop, t_field) = vars_def[var_name]
            # Create a new variable and assign the name/type
            var = driver.driver.variables.new()
            var.name = var_name
            var.type = 'TRANSFORMS'
            # Get correct property string
            t_prop = transform_props[t_prop.lower()]

            # If `t_field` is '-', then pick the corresponding field
            # using the driver index.
            if t_field == '-':
                t_field = 'XYZW'[driver.array_index]

            # Set the target object and the correct data path
            transform_type = t_prop + t_field.upper()
            var.targets[0].id = t_obj
            var.targets[0].transform_type = transform_type

        # Set the expression
        driver.driver.expression = expr
