'''
This file contains functions that are to be added to the driver namespace for
different operators. The functions here should be prefixed by `gb_` to avoid
clashes in the driver namespace.

All functions with names that start with 'gb_' will automatically be added into
the driver_namespace by __init__.py
'''


def gb_rad_axis_helper(d, r1, r2, o1, o2):
    '''
    Function to be used in the driver to help compute the intersection point of
    the radical axis of 2 circles and the line connecting their centers.

    d:          Distance b/w circles             (float)
    r1, r2:     Radii of circles                 (float)
    o1, o2:     X,Y or Z positions of circles    (float)

    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `o1` and `o2`
    '''
    frac = (d * d + r1 * r1 - r2 * r2) / (2 * d * d)
    return (1 - frac) * o1 + frac * o2


def gb_drive_angle_bevel(start, ax, ay, az, bx, by, bz, cx, cy, cz):
    '''
    Function to be used in the driver for Angle arcs. It controls both the
    start and end bevel factor based on whether `start` = True / False

    start:      Is this the driver for bevel_start?          (Boolean)
    rest:       X, Y, Z coordinates of the objects A, B, C   (float)

    Return:  Value for the start / end bevel factor based on `start`
    '''
    import mathutils
    import math

    v1 = mathutils.Vector((bx - ax, by - ay, bz - az))
    v2 = mathutils.Vector((cx - ax, cy - ay, cz - az))
    frac = v1.dot(v2) / (v1.length * v2.length)
    angle = math.acos(frac)
    normal = v1.cross(v2)

    # This is tricky: we need to establish some sort of 'correct' normal for
    # the plane around which everything is oriented. Arbitrarily, we assume
    # that the normal with greater Z component is 'correct'. If equal, compare
    # Y, then X.
    is_correct = (
        (normal.z < 0) or
        (normal.z == 0 and normal.y < 0) or
        (normal.z == normal.y == 0 and normal.x < 0)
    )

    if is_correct:
        # If the normal is 'correct' we need to modify bevel start
        if start:
            factor = angle / math.tau   # Start factor
        else:
            factor = 1                  # End factor
    else:
        # Otherwise, the arc's normal is flipped, so we need to bevel
        # the other way.
        if start:
            factor = 0                  # Start factor
        else:
            factor = angle / math.tau   # End factor

    return factor


def gb_polar_intersection(d, r, o1, o2):
    '''
    Function to be used in the driver to help compute the intersection point of
    the polar line of a point A relative to a circle and the line connecting the
    point with the center.

    d:      Distance b/w center of circle and point           (float)
    r:      Radii of circles                                  (float)
    o1:     X,Y or Z positions of center of circle            (float)
    o2:     X,Y or Z positions of the point A                 (float)

    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `o1` and `o2`
    '''
    frac = (r * r) / (d * d)
    return (1 - frac) * o1 + frac * o2




def gb_reflect(o1, o2):
    '''
    Function to be used in the driver to help compute the reflection of a point A
    about a line.

    o1:     X,Y or Z positions of A                           (float)
    o2:     X,Y or Z positions of the projec point            (float)

    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `o1` and `o2`
    '''
    frac = 2
    return (1 - frac) * o1 + frac * o2


def gb_inv_circle_on(d, r, o1, o2):
    '''
    Function to be used in the driver to help compute the intersection point of
    the inversion of a circle (origin on) and the axis connecting the center of 
    the circle and the origin of the inversion. 
    
    d:      power of inversion                                 (float)
    r:      radius of circle                                   (float)
    o1:     X,Y or Z positions of origin                       (float)
    o2:     X,Y or Z positions of antipodal of origin          (float)
 
    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `o1` and `o2`
    '''
    frac = (d * d) / (4 * r * r)
    return (1 - frac) * o1 + frac * o2

def gb_inversion_expres(d, r, o1, o2):
    '''
    Function to be used in the driver to help compute the intersection point of
    the inversion of a circle (origin on) and the axis connecting the center of 
    the circle and the origin of the inversion. 
    
    d:      power of inversion                                 (float)
    r:      distance of origin from point                      (float)
    o1:     X,Y or Z positions of origin                       (float)
    o2:     X,Y or Z positions of origin                       (float)
 
    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `o1` and `o2`
    '''
    frac = (d * d) / (r * r)
    return (1 - frac) * o1 + frac * o2

    

