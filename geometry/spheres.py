from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import planes
from . import lines
from . import triangles


def put_at_circumcenter(obj, A, B, C, hide_extra=True):
    '''
    Constrain the given object at the circumcenter of 3 points.
    obj:        Source object   (Blender Object)
    A, B, C:    3 points        (Blender Objects)
    Note: This method creates additional objects that are needed to help find
          the circumcenter. These are hidden by default.
    '''
    # Construct the perp. bisector plane of A-B
    ab_perp_plane = objects.new_plane(hide=hide_extra)
    planes.bisecting_plane_of_points(ab_perp_plane, A, B)

    # Put the object at the midpoint of A-C, and align it with the triangle.
    core.put_in_between(obj, A, C, influence=0.5)
    constraints.damped_track(obj, axis='X', target=A)
    constraints.locked_track(obj, lock='X', axis='Y', target=B)

    # Project it onto the plane from above to get the circumcenter
    constraints.project_along_axis(
        obj,
        axis='+Y',
        target=ab_perp_plane,
        opposite=True
    )

# --------------------------------------------------------------------------- #
#                               CONSTRUCTIONS                                 #
# --------------------------------------------------------------------------- #


def circumsphere(sphere, A, B, C, D, hide_extra=True):
    pr_plane = objects.new_plane(hide=hide_extra)
    pr_plane.name = 'projection plane'
    core.put_in_between(pr_plane, A, D)
    constraints.damped_track(pr_plane, axis='Z', target=A)

    center = objects.new_point(hide=hide_extra)
    center.name = 'sphere center'
    put_at_circumcenter(center, A, B, C, hide_extra=hide_extra)
    constraints.project_along_axis(
        center,
        axis='Z',
        target=pr_plane,
        opposite=True
    )

    constraints.copy_transforms(sphere, target=center, transforms='LR')
    drivers.add_driver_distance(
        obj=sphere,
        prop='scale',
        fields='XYZ',
        A=A,
        B=center
    )


def sphere_from_diameter(sphere, A, B):
    '''
    Given the points A, B on the diameter, forms the sphere.

    sphere:     sphere to align         (Blender Object)
    A, B:       Points on diameter      (Blender Objects)
    '''
    lines.midpoint(sphere, A, B)
    drivers.add_driver_distance(sphere, 'scale', 'XYZ', A, B, scale=0.5)


def sphere_from_center_point(sphere, A, B):
    '''
    Given the center A and a point on the sphere B, forms the sphere.

    sphere:     sphere to align         (Blender Object)
    A:          Center                  (Blender Object)
    B:          Other point on sphere   (Blender Object)
    '''
    constraints.copy_rotation(sphere, target=A)
    constraints.copy_location(sphere, target=A)
    drivers.add_driver_distance(sphere, 'scale', 'XYZ', A, B)


def sphere_from_center_distance(sphere, A, X, Y, hide_extra=True):
    '''
    Given the center A, and the radius defined by the distance between the
    2 objects X, Y, forms the sphere.

    sphere:     sphere to align         (Blender Object)
    A:          Center                  (Blender Object)
    X, Y:       2 objects               (Blender Objects)
    '''
    constraints.copy_rotation(sphere, target=A)
    constraints.copy_location(sphere, target=A)
    drivers.add_driver_distance(sphere, 'scale', 'XYZ', X, Y)


def sphere_from_center_radius(sphere, A, radius):
    '''
    Given the center A and fixed radius, forms the sphere.

    sphere:     sphere to align         (Blender Object)
    A:          Center                  (Blender Object)
    radius:     radius                  (Float)
    '''
    constraints.copy_rotation(sphere, target=A)
    constraints.copy_location(sphere, target=A)
    objects.uniform_scale(sphere, radius)


# --------------------------------------------------------------------------- #
#                               RADICAL AXIS                                  #
# --------------------------------------------------------------------------- #


def radical_intercept(obj, A, B):
    '''
    Place the given object at the intersection point of the radical axis of 2
    given spheres and the line connecting their centers. It also aligns the
    'Y' axis of the object with the line AB.

    - Note that the last point is useful since lines are defined on the X axis.
    Using this function with a line gives us the radical axis.

    obj:        Source object   (Blender Object)
    A, B:       2 spheres       (Blender Objects)
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


def radical_axis(line, sphere1, sphere2):
    '''
    Place the given object at the radical axis of 2 given spheres.

    obj:        Source object   (Blender Object)
    A, B:       2 spheres       (Blender Objects)
    '''
    point_r = objects.new_point(hide=True)
    radical_intercept(point_r, sphere1, sphere2)
    objects.move_origin_center(line)
    constraints.copy_location(line, point_r)
    constraints.copy_rotation(line, point_r)


# --------------------------------------------------------------------------- #
#                                 TANGENTS                                    #
# --------------------------------------------------------------------------- #


def sphere_tangent_points(tan1, tan2, sphere, point, hide_extra=True):
    '''
    Places (and aligns) tan1 and tan2 at two points on `sphere` such that
    the tangents on the sphere from these two points intersect at `point`

    tan1, tan2:     Objects to be placed    (Blender Objects)
    sphere:         The sphere              (Blender Object; Curve; sphere)
    point:          The point               (Blender Object)
    '''

    # General idea here:
    # - Have a sphere C centered at point A
    # - Have a point at point B
    # - Let M be the midpoint of A-B
    # - Consider the sphere C' centered at M, with radius len(A-B)/2
    # - The tangents from B to C touch the sphere at the intersection
    #     points of the spheres C' and C.
    from .intersections import sphere_sphere_intersection

    mid_circ = objects.new_sphere(hide=hide_extra)
    mid_circ.name = "tangent sphere helper"
    sphere_from_diameter(mid_circ, sphere, point)

    # We next compute the intersection points of the two spheres
    sphere_sphere_intersection(tan1, tan2, mid_circ, sphere, hide_extra=True)


def sphere_tangent_lines(line1, line2, sphere, point, hide_extra=True):
    '''
    Forms the tangent line (segments) to the sphere from the given point.

    line1, line2:   Lines to make tangent  (Blender Objects; Curve; Line)
    sphere:         The sphere              (Blender Object; Curve; sphere)
    point:          The point               (Blender Object)
    '''

    tan1 = objects.new_point(hide=hide_extra)
    tan1.name = "tangent pt 1"
    tan2 = objects.new_point(hide=hide_extra)
    tan2.name = "tangent pt 2"

    sphere_tangent_points(tan1, tan2, sphere, point)
    lines.segment(line1, tan1, point)
    lines.segment(line2, tan2, point)


def sphere_tangent_line(line, sphere, point):
    '''
    Forms the tangent to the sphere at the given point.

    NOTE: This function assumes the given point is constrained to the sphere.

    line:           Line to make tangent    (Blender Objects; Curve; Line)
    sphere:         The sphere              (Blender Object; Curve; sphere)
    point:          The point               (Blender Object)
    '''
    objects.move_origin_center(line)
    constraints.copy_location(line, point)
    constraints.copy_rotation(line, sphere)

    # Lines are along the X axis, so tracking the Y to center does the job.
    constraints.locked_track(line, lock='Z', axis='Y', target=sphere)


# --------------------------------------------------------------------------- #
#                               POLAR LINES                                   #
# --------------------------------------------------------------------------- #

def polar_intersection(obj, A, sphere):
    '''
    Place the given object at the intersection point of the polar axis
    of a point A relative to a sphere.

    obj:        Source object   (Blender Object)
    A:          Point           (Blender Objects)
    sphere:     sphere          (Blender Objects)
    '''
    drivers.add_driver(
        obj=obj,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('distance', A, sphere),
            'r': ('transform', sphere, 'scale', 'X'),
            'o1': ('transform', sphere, 'location', '-'),
            'o2': ('transform', A, 'location', '-'),
        },
        expr='gb_polar_intersection(d, r, o1, o2)'
    )
    constraints.copy_rotation(obj, A)


def polar_line(line, A, sphere, hide_extra=True):
    '''
    This function places a line to be the polar of the point A (active)
    relative to the sphere and returns it as the line argument.

    line:       Line to place   (Blender Object)
    A:          Point           (Blender Objects)
    sphere:     sphere          (Blender Objects)
    '''
    foot_polar = objects.new_point(hide=hide_extra)
    polar_intersection(foot_polar, A, sphere)

    # Finally we place line to the polar line
    lines.orthogonal_line_to_points(line, foot_polar, A, sphere)
