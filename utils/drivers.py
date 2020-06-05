'''
Driver-related utilites to simplify adding drivers to objects without
the boilerplate.
'''

transform_props = {
    'scale': 'SCALE_',
    'location': 'LOC_',
    'rotation': 'ROT_',
}


def make_driver_list(obj, prop, fields=None):
    '''
    Add drivers to the actual object for the correct properties, and return a
    list of the newly added drivers back.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
    fields:    Fields of prop.      (String, explained below)

    `fields` is a string containing one or more of the characters 'X', 'Y', 'Z'
    , 'W' denoting which of the fields need to have a driver set.

    for example, 'XY' means the X and Y fields have a new driver created.
    '''
    if fields is None:
        return [obj.driver_add(prop)]

    driver_list = []
    for axis in fields:
        idx = 'XYZW'.index(axis.upper())
        driver_list.append(obj.driver_add(prop.lower(), idx))
    return driver_list


def add_driver(obj, prop, fields=None, vars_def={}, expr="1.0"):
    '''
    Add a driver for an object's properties, using the transform channels of
    other objects.

    TODO: Support other variable types...
    TODO: Support other `spaces` for channels other than WORLD space

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
    fields:    Fields of prop.      (String, look at `make_driver_list`)
    vars_def:  Variable defns.      (Look Below)
    expr:      Driver Expression    (String)

    Variable definitions are a dictionary with the following format:
    {
        var_name: (type='transform', target_object, prop, field),
        var_name: (type='distance', object_1, object_2),
        var_name: (type='datapath', object, "data_path")
    }
    where:
        type: 'transform', 'distance', (... unsupported ...)
        object_1, object_2: 2 objects to compute distance
        target_obj: Blender Object
        prop: 'scale', 'location' or 'rotation'
        field: 'X', 'Y', 'Z', 'W', '-'
            - Note: if this value is `-`, then the corresponding destination
                field is used from the fields of the driven quantity.
                (from `driver.array_index`)

    For example, to represent `x = Cube.scale[1]`,
    {
        x: ('transform', Cube, 'scale', 'Y')
    }
    '''
    driver_list = make_driver_list(obj, prop, fields)

    for driver in driver_list:
        for var_name in vars_def:
            var = driver.driver.variables.new()
            var.name = var_name

            # Get the details of the definition
            var_type = vars_def[var_name][0]

            if var_type == 'transform':
                var.type = 'TRANSFORMS'

                (t_obj, t_prop, t_field) = vars_def[var_name][1:]
                if t_field == '-':
                    t_field = 'XYZW'[driver.array_index]

                d = {'scale': 'SCALE', 'location': 'LOC', 'rotation': 'ROT'}

                transform_type = f'{d[t_prop]}_{t_field}'
                var.targets[0].id = t_obj
                var.targets[0].transform_type = transform_type

            elif var_type == 'distance':
                var.type = 'LOC_DIFF'
                (A, B) = vars_def[var_name][1:]
                var.targets[0].id = A
                var.targets[1].id = B

            elif var_type == "datapath":
                (A, data_path) = vars_def[var_name][1:]
                var.type = 'SINGLE_PROP'
                var.targets[0].id        = A
                var.targets[0].data_path = data_path

            else:
                raise Exception("Driver variable type not in "
                                "{'transform', 'distance', 'datapath'}")

        driver.driver.expression = expr


def add_driver_distance(obj, prop, fields, A, B, scale=1):
    '''
    Add a driver for an object's properties, set to the distance from A to B,
    scaled by some factor.

    obj:       Source objects       (Blender Object)
    prop:      Driver's property    ('scale', 'location', ...)
    fields:    Fields of prop.      (String, look at `make_driver_list`)
    A, B:      The 2 Objects        (Blender Objects)
    scale:     Scaling factor       (float)
    '''
    # Add the needed drivers to the object
    driver_list = make_driver_list(obj, prop, fields)

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
