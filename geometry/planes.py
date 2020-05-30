from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core


def constraint_to_plane(obj, plane):
    '''
    Takes an object and constraints it to be on the plane. Uses parenting
    without inverse, and locks the Z location coordinate to 0.

    obj:        Source object             (Blender Object)
    plane:      Plane to constrain to     (Blender Objects)
    '''
    objects.set_parent(obj, plane)
    # Drive location to Z=0 to avoid changing
    drivers.add_driver(
        obj=obj,
        prop='location',
        fields='Z',
        expr="0"
    )


def align_to_plane_of(obj, A, B, C):
    '''
    Place obj at A. Then ligns the X-Y axes of the object with the 
    plane defined by the 3 given points.

    obj:        Source object (Blender Object)
    A, B, C:    3 points      (Blender Objects)
    '''
    constraints.copy_location(obj, target=A)
    constraints.damped_track(obj, axis='X', target=B)
    constraints.locked_track(obj, axis='Y', lock='X', target=C)


def make_bisecting_plane(plane, A, B):
    '''
    Makes the bisecting plane of the line segment defined by AB

    plane:   Source plane  (Blender Object)
    A, B:    2 points      (Blender Objects)
    '''
    core.put_in_between(plane, A, B)
    constraints.damped_track(plane, axis='Z', target=A)
