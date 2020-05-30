from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

from .circles import *
from .intersections import *
from .inversion import *
from .triangle_constructions import *


def segment(line, A, B):
    '''
    This function returns line to the segment defined by
    the points A, B.
    '''
    copy_location(line, target=A)
    copy_rotation(line, A)
    locked_track(line, lock='Z', axis='X', target=B)

    add_driver_distance(
        obj=line,
        prop='scale',
        fields='XYZ',
        A=A,
        B=B,
        scale=1
    )


def ray(line, A, B):
    '''
    Places a full line (line) through the points A, B. Effectively, copy
    location of A, align to B and stretch the given axis a desired amount
    (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    copy_location(obj, target=A)
    copy_rotation(obj, A)
    locked_track(obj, lock='Z', axis='X', target=B)
    add_driver(line, 'scale', fields='XYZ', vars_def={}, expr="1000")


def full_line(line, A, B):
    '''
    Places a full line (line) through the points A, B. her. Effectively, move
    center at the middle point of the line, copy location of A, align to B
    and stretch the given axis a desired amount (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    move_origin_center(line, center='MEDIAN')
    copy_location(obj, target=A)
    copy_rotation(obj, A)
    locked_track(obj, lock='Z', axis='X', target=B)
    add_driver(line, 'scale', fields='XYZ', vars_def={}, expr="1000")


def midpoint(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that
        (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)
    Midpoint takes the orientation of A
    '''

    # Note that location of B is copied first to make influence consistent
    copy_location(obj, target=B)
    copy_location(obj, target=A, influence=influence)
    copy_rotation(obj, A)


###############################################################################
# Parallel lines

def parallel_line(parallel_line, A, line, hide_extra=True):
    '''
    This function places a line (parallel_line) to go through a point A and
    be parallel to a line.
    '''
    move_origin_center(parallel_line, center='MEDIAN')
    copy_location(parallel_line, A)
    copy_rotation(parallel_line, line)

###############################################################################
# Orthogonality

