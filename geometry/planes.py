from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import lines


def constraint_to_plane(obj, plane):
    '''
    Takes an object and constraints it to be on the plane. Uses parenting
    without inverse, and locks the Z location coordinate to 0.

    obj:        Source object             (Blender Object)
    plane:      Plane to constrain to     (Blender Objects)
    '''
    objects.set_parent(obj, plane)
    # Drive location to 0 to avoid changing
    drivers.add_driver(
        obj=obj,
        prop='location',
        fields='Z',
        expr="0"
    )


def align_to_plane_of(obj, A, B, C):
    '''
    Aligns the X-Y axes of the object with the plane defined by the 3
    given points.

    obj:        Source object (Blender Object)
    A, B, C:    3 points      (Blender Objects)
    '''
    constraints.copy_location(obj, target=A)
    constraints.damped_track(obj, axis='X', target=B)
    constraints.locked_track(obj, axis='Y', lock='X', target=C)


def bisecting_plane_of_points(plane, A, B, hide_extra=True):
    '''
    Align the obj (a plane) to the perpendicular bisector plane of
    the segment AB. The Z axis of the returned obj is parallel to AB.
    The X, Y axis are not determined.

    plane:   Source plane  (Blender Object)
    A, B:    2 points      (Blender Objects)
    '''
    lines.midpoint(plane, A, B)
    constraints.damped_track(plane, axis='Z', target=A)
    plane.name = "Perp. Bisector Plane"


def bisecting_plane_of_line(plane, line, hide_extra=True):
    '''
    Align the obj (a plane) to the perpendicular bisector plane of
    the segment AB. The Z axis of the returned obj is parallel to AB.
    The X, Y axis are not determined.

    plane:   Source plane       (Blender Object)
    line:    Line Segment       (Blender Object; Curve; Line)
    '''
    A = objects.new_point(hide=hide_extra)
    B = objects.new_point(hide=hide_extra)
    A.name = "line start"
    B.name = "line end"
    lines.line_ends(A, B, line)

    bisecting_plane_of_points(plane, A, B, hide_extra)
