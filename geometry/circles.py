from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import lines


# --------------------------------------------------------------------------- #
#                               CONSTRUCTIONS                                 #
# --------------------------------------------------------------------------- #


def circle_from_diameter(circle, A, B):
    '''
    Given the points A, B on the diameter, forms the circle.

    circle:     Circle to align         (Blender Object)
    A, B:       Points on diameter      (Blender Objects)
    '''
    lines.midpoint(circle, A, B)
    drivers.add_driver_distance(circle, 'scale', 'XYZ', A, B, scale=0.5)


def semicircle_from_diameter(semicircle, A, B, other=False):
    '''
    Given the points A, B on the diameter, forms the semicircle.

    semicircle:     Circle to align         (Blender Object)
    A, B:           Points on diameter      (Blender Objects)
    other:          S.C. on other side?     (Boolean)
    '''
    constraints.copy_rotation(semicircle, target=A)
    core.put_in_between(semicircle, A, B)
    axis = 'X' if other else '-X'
    constraints.locked_track(semicircle, lock='Z', axis=axis, target=A)
    drivers.add_driver_distance(semicircle, 'scale', 'XYZ', A, B, scale=0.5)


def circle_from_center_point(circle, A, B):
    '''
    Given the center A and a point on the circle B, forms the circle.

    circle:     Circle to align         (Blender Object)
    A:          Center                  (Blender Object)
    B:          Other point on circle   (Blender Object)
    '''
    constraints.copy_rotation(circle, target=A)
    constraints.copy_location(circle, target=A)
    drivers.add_driver_distance(circle, 'scale', 'XYZ', A, B)


def circle_from_center_distance(circle, A, X, Y, hide_extra=True):
    '''
    Given the center A, and the radius defined by the distance between the
    2 objects X, Y, forms the circle.

    circle:     Circle to align         (Blender Object)
    A:          Center                  (Blender Object)
    X, Y:       2 objects               (Blender Objects)
    '''
    constraints.copy_rotation(circle, target=A)
    constraints.copy_location(circle, target=A)
    drivers.add_driver_distance(circle, 'scale', 'XYZ', X, Y)


def circle_from_center_radius(circle, A, radius):
    '''
    Given the center A and fixed radius, forms the circle.

    circle:     Circle to align         (Blender Object)
    A:          Center                  (Blender Object)
    radius:     radius                  (Float)
    '''
    constraints.copy_rotation(circle, target=A)
    constraints.copy_location(circle, target=A)
    objects.uniform_scale(circle, radius)


# --------------------------------------------------------------------------- #
#                               RADICAL AXIS                                  #
# --------------------------------------------------------------------------- #


def radical_intercept(obj, A, B):
    '''
    Place the given object at the intersection point of the radical axis of 2
    given circles and the line connecting their centers. It also aligns the
    'Y' axis of the object with the line AB.

    - Note that the last point is useful since lines are defined on the X axis.
    Using this function with a line gives us the radical axis.

    obj:        Source object   (Blender Object)
    A, B:       2 Circles       (Blender Objects)
    '''
    
    drivers.add_driver(
        obj=obj,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('distance', A, B),
            'r1': ('transform', A, 'scale', 'X'),
            'r2': ('transform', B, 'scale', 'X'),
            'o1': ('transform', A, 'location', '-'),
            'o2': ('transform', B, 'location', '-'),
        },
        expr='gb_rad_axis_helper(d, r1, r2, o1, o2)'
    )
    constraints.copy_rotation(obj, A)
    constraints.locked_track(obj, 'Z', 'Y', A)

def radical_axis(line, circle1, circle2):
    '''
    Place the given object at the radical axis of 2 given circles.
     
    obj:        Source object   (Blender Object)
    A, B:       2 Circles       (Blender Objects)
    '''
    point_r = objects.new_point(hide=True)
    radical_intercept(point_r, circle1, circle2)
    objects.move_origin_center(line)
    constraints.copy_location(line, point_r)
    constraints.copy_rotation(line, point_r)



# --------------------------------------------------------------------------- #
#                                 TANGENTS                                    #
# --------------------------------------------------------------------------- #


def circle_tangent_points(tan1, tan2, circle, point, hide_extra=True):
    '''
    Places (and aligns) tan1 and tan2 at two points on `circle` such that
    the tangents on the circle from these two points intersect at `point`

    tan1, tan2:     Objects to be placed    (Blender Objects)
    circle:         The circle              (Blender Object; Curve; Circle)
    point:          The point               (Blender Object)
    '''

    # General idea here:
    # - Have a circle C centered at point A
    # - Have a point at point B
    # - Let M be the midpoint of A-B
    # - Consider the circle C' centered at M, with radius len(A-B)/2
    # - The tangents from B to C touch the circle at the intersection
    #     points of the circles C' and C.
    from .intersections import circle_circle_intersection

    mid_circ = objects.new_circle(hide=hide_extra)
    mid_circ.name = "tangent circle helper"
    circle_from_diameter(mid_circ, circle, point)

    # We next compute the intersection points of the two circles
    circle_circle_intersection(tan1, tan2, mid_circ, circle, hide_extra=True)


def circle_tangent_lines(line1, line2, circle, point, hide_extra=True):
    '''
    Forms the tangent line (segments) to the circle from the given point.

    line1, line2:   Lines to make tangent  (Blender Objects; Curve; Line)
    circle:         The circle              (Blender Object; Curve; Circle)
    point:          The point               (Blender Object)
    '''

    tan1 = objects.new_point(hide=hide_extra)
    tan1.name = "tangent pt 1"
    tan2 = objects.new_point(hide=hide_extra)
    tan2.name = "tangent pt 2"

    circle_tangent_points(tan1, tan2, circle, point)
    lines.segment(line1, tan1, point)
    lines.segment(line2, tan2, point)


def circle_tangent_line(line, circle, point):
    '''
    Forms the tangent to the circle at the given point.

    NOTE: This function assumes the given point is constrained to the circle.

    line:           Line to make tangent    (Blender Objects; Curve; Line)
    circle:         The circle              (Blender Object; Curve; Circle)
    point:          The point               (Blender Object)
    '''
    objects.move_origin_center(line)
    constraints.copy_location(line, point)
    constraints.copy_rotation(line, circle)

    # Lines are along the X axis, so tracking the Y to center does the job.
    constraints.locked_track(line, lock='Z', axis='Y', target=circle)


# --------------------------------------------------------------------------- #
#                               POLAR LINES                                   #
# --------------------------------------------------------------------------- #

def polar_intersection(obj, A, circle):
    '''
    Place the given object at the intersection point of the polar axis
    of a point A relative to a circle.

    obj:        Source object   (Blender Object)
    A:          Point           (Blender Objects)
    circle:     Circle          (Blender Objects)
    '''
    drivers.add_driver(
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
    constraints.copy_rotation(obj, A)


def polar_line(line, A, circle, hide_extra=True):
    '''
    This function places a line to be the polar of the point A (active)
    relative to the circle and returns it as the line argument.

    line:       Line to place   (Blender Object)
    A:          Point           (Blender Objects)
    circle:     Circle          (Blender Objects)
    '''
    foot_polar = objects.new_point(hide=hide_extra)
    polar_intersection(foot_polar, A, circle)

    # Finally we place line to the polar line
    lines.orthogonal_line_to_points(line, foot_polar, A, circle)
