from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

from .intersections import *
from .inversion import *
from .lines import *
from .triangle_constructions import *


def circle_from_diameter(circle, A, B, hide_extra=True):
    '''
    Finds the circle with diameter AB. It first puts an empty O at the midpoint
    of AB and  then draws the circle with center O and radius equal to half AB.
    The circle has the same orientation as A.

    A, B:       2 POINTS        (Blender Objects; circle curves)
    '''

    # Place the circle obj with center at the midpoint
    copy_rotation(circle, A)
    put_in_between(circle, A, B, 0.5)
    add_driver_distance(circle, scale, 'XYZ', A, B, 0.5)


def circle_center_point(circle, center, point, hide_extra=True):
    '''
    Finds the circle with given center and passes through a given point.
    It is a  2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center, point:       2 POINTS        (Blender Objects)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)
    # damped_track(circle, axis='X', target=B)
    # Non needed for 2D constructions, because Z axis of center gives
    # the plane.

    add_driver_distance(circle, 'scale', 'XYZ', center, point)


def circle_center_radius_distance(circle, center, A, B, hide_extra=True):
    '''
    Place the circle at given center with given radius AB. It is a
    2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center, A, B:       3 POINTS        (Blender Objects)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)

    add_driver_distance(circle, 'scale', 'XYZ', A, B)


def circle_center_radius_number(circle, center, number, hide_extra=True):
    '''
    Place the circle at given center with given radius number. It is a
    2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center       1 POINTS        (Blender Objects)
    number        radius         (float)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)

    add_driver(circle, 'scale', 'XYZ', vars_def={}, expr="number")

 #############################################################################
 # Polar lines


def put_at_polar_intersection(obj, A, circle):
    '''
    Place the given object at the  intersection point of the polar axis
    of a point A relative to a circle and the line connecting A to the 
    center of the circle. 

    obj:        Source object   (Blender Object)
    A:          Point           (Blender Objects)
    circle:     Circle          (Blender Objects)
    '''
    add_driver(
        obj=obj,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('distance', A, circle),
            'r': ('transform', circle, 'scale', 'X'),
            'o1': ('transform', circle, 'location', '-'),
            'o2': ('transform', A, 'location', '-'),
        },
        expr='gb_polar_intersection(d, r, o1, o2)'
    )
    copy_rotation(obj, A)


def polar_line(line, circle, A, hide_extra=True):
    '''
    This function places a line to be the polar of the point A (active)
    relative to the circle and returns it as the line argument.
    '''
    foot_polar = new_empty(hide=hide_extra)
    put_at_polar_intersection(foot_polar, A, circle)

    # We next construct the line connecting the point and the center
    connecting_line = new_line(hide=hide_extra)
    segment(connecting_line, circle, A)

    # Finally we place line to the polar line
    orthogonal_line(line, foot_polar, connecting_line)

###############################################################################
# Tangent lines


def tangent_points_to_circle(tan1, tan2, A, C, hide_extra=True):
    # This function computes the tang points tan1 and tan2 where the tangents
    # from a point A outside a cicle C intersect C. Point A should be active.

    circle_help = new_circle()
    circle_from_diameter(circle_help, A, C, hide_extra=True)

    # We next compute the intersection points of the two circles
    circle_circle_intersection(tan1, tan2, circle_help, C, hide_extra=True)


def tangent_lines_to_circle(line1, line2, A, C, hide_extra=True):

    # This function computes the tangent lines line1 and line2
    # from a point A outside a cicle C to the circle C. Point A is active.

    tan1 = new_empty(hide=hide_extra)
    tan2 = new_empty(hide=hide_extra)

    tangent_points_to_circle(tan1, tan2, A, C)

    segment(line1, A, tan1)
    segment(line2, A, tan2)


def tangent_line_to_circle(line1, A, C, hide_extra=True):

    # This function computes the tangent line line1
    # from a point A on a cicle C to the circle C. Point A active.

    radius = new_line(hide=hide_extra)
    segment(radius, A, C)
    orthogonal_line(line1, A, radius)
