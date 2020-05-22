'''
This file contains functions that are to be added to the driver namespace for
different operators. The functions here should be prefixed by `gb_` to avoid
clashes in the driver namespace.
'''


def gb_rad_axis_helper(d, r1, r2, o1, o2):
    '''
    Function to be used in the driver to help compute the intersection point of
    the radical axis of 2 circles and the line connecting their centers.

    d:          Distance b/w circles             (float)
    r1, r2:     Radii of circles                 (float)
    oa, ob:     X,Y or Z positions of circles    (float)

    Return: Returns the X, Y or Z position of the intersection point when the
            corresponding X, Y and Z positions are passed in as `oa` and `ob`
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

    TOL = 10e-6

    # This is tricky: we need to establish some sort of 'correct' normal for
    # the plane around which everything is oriented. Arbitrarily, we assume
    # that the normal with greater Z component is 'correct'. If equal, compare
    # Y, then X.    (Using TOLerance for floating point comparison)
    is_correct = (
        (normal.z < -TOL) or                                     # Z<0
        (normal.z < TOL and normal.y < -TOL) or                  # Z=0, Y<0
        (normal.z < TOL and normal.y < TOL and normal.x < -TOL)  # Z,Y=0, X<0
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