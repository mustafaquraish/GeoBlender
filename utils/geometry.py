import bpy
from constraints import *
from new_objects import *

def plane_at_points(context, A, B, C, size=10):
    '''
    Creates a new plane going through 3 points

    context:    Context       (Blender Context)
    A, B, C:    3 points      (Blender Objects)
    size:       Plane size    (float)
    '''
    plane = new_plane(context, size=size)
    copy_location(plane, target=A)
    damped_track(plane, track='X', target=B)
    locked_track(plane, track='Y', lock='X', target=C)
    return plane

def put_in_between(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that 
        (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Context)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)
    '''

    # Note that location of B is copied first to make influence consistent
    copy_location(obj, target=B)
    copy_location(obj, target=A, influence=influence)


