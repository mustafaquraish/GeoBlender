import math

from ..utils import objects
from ..utils import constraints
from ..utils import geometry
from ..utils import drivers

from . import core

# --------------------------------------------------------------------------- #
#                               CONSTRUCTIONS                                 #
# --------------------------------------------------------------------------- #


def segment(line, A, B, axis='X'):
    '''
    This function creates the line to the segment defined by the points A, B.

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    axis:       Axis to align   ('X', 'Y')
    '''
    constraints.copy_location(line, A)
    constraints.damped_track(line, axis='X', target=B)
    drivers.add_driver_distance(
        obj=line,
        prop='scale',
        fields='XYZ',
        A=A,
        B=B
    )


def ray(line, A, B, length=100, axis='X'):
    '''
    Forms a ray starting at the point A, towards the point B with the given
    length

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    axis:       Axis to align   ('X', 'Y')
    '''
    constraints.copy_location(line, A)
    constraints.damped_track(line, axis='X', target=B)
    objects.uniform_scale(line, length)


def line(line, A, B, length=100):
    '''
    Places a full line through the points A, B. her. Effectively, move center
    at the middle point of the line, copy location of A, align to B and stretch
    the given axis a desired amount (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    objects.move_origin_center(line)
    constraints.copy_location(line, A)
    constraints.damped_track(line, axis='X', target=B)
    objects.uniform_scale(line, length)

# --------------------------------------------------------------------------- #
#                           DISTANCE AND AREA                                 #
# --------------------------------------------------------------------------- #


def distance_function(A, B):
    '''
    Returns the distance of the points A, B

    A, B:       2 points        (Blender Objects)
    '''
    v = A.location - B.location
    x, y, z = v[0], v[1], v[2]
    dist = math.sqrt(x * x + y * y + z * z)
    return dist


def area_function(A, B, C):
    '''
    Returns the are of the triangle ABC

    A, B, C:       3 points        (Blender Objects)
    '''
    c = distance_function(A, B)
    a = distance_function(B, C)
    b = distance_function(C, A)

    s = (a + b + c) / 2
    yes = s * (s - a) * (s - b) * (s - c)
    area = math.sqrt(yes)
    return area


def area_function_from_lines(A, B, C):
    '''
    Returns the are of the triangle ABC

    A, B, C:       3 lines        (Blender Objects)
    '''
    a = A.scale[0]
    b = B.scale[0]
    c = C.scale[0]

    s = (a + b + c) / 2
    yes = s * (s - a) * (s - b) * (s - c)
    area = math.sqrt(yes)
    return area


# --------------------------------------------------------------------------- #
#                           PLACING ON A LINE                                 #
# --------------------------------------------------------------------------- #

def midpoint(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that
        (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)

    NOTE: Midpoint takes the orientation of A
    '''

    # Note that location of B is copied first to make influence consistent
    constraints.copy_location(obj, target=B)
    constraints.copy_location(obj, target=A, influence=influence)
    constraints.copy_rotation(obj, A)


def line_ends(A, B, line):
    '''
    Places the two input objects A and B at the two extreme ends of the line.

    A, B:       2 points        (Blender Objects)
    line:       The line        (Blender Object; Curve; Line)
    '''
    # Position on curve
    constraints.position_on_curve(A, line, position=0)
    constraints.position_on_curve(B, line, position=1)

    # Make sure that the points' Z axis is aligned with that of the line
    constraints.copy_rotation(A, line)
    constraints.copy_rotation(B, line)


# --------------------------------------------------------------------------- #
#                           PARALLEL LINES                                    #
# --------------------------------------------------------------------------- #

def parallel_line(parallel_line, A, line, hide_extra=True):
    '''
    This function places a line (parallel_line) to go through a point A and
    be parallel to a another given line.

    parallel_line:      Line to place   (Blender Object; Curve; Line)
    A:                  Point           (Blender Object)
    line:               Other line      (Blender Object; Curve; Line)
    '''
    objects.move_origin_center(parallel_line, center='MEDIAN')
    constraints.copy_location(parallel_line, A)
    constraints.copy_rotation(parallel_line, line)


# --------------------------------------------------------------------------- #
#                              ORTHOGONALITY                                  #
# --------------------------------------------------------------------------- #

'''
- The next functions heavily rely on the property that the Z axis of points
  is normal to the parent plane.
'''


def orthogonal_proj_to_points(obj, A, B, C, hide_extra=True):
    '''
    This function moves obj to the orthogonal projection in 2D of A on
    the line defined by the points B, C. The Y axis of obj is aligned with
    BC and the X axis is aligned with the perpendicular direction and the Z
    axis is the same as that of A.

    obj:      The object                (Blender Object)
    A:        Point to project from     (Blender Object)
    B, C:     Points defining line      (Blender Object; Curve; Line)
    '''
    pr_plane = objects.new_plane(hide=hide_extra)
    pr_plane.name = "projection plane"
    core.make_orthogonal_to(pr_plane, C, B, A)

    constraints.copy_location(obj, A)
    constraints.copy_rotation(obj, A)
    constraints.project_nearest(obj, target=pr_plane)

    # Add tracks to both ends in case A overlaps one of the points
    constraints.locked_track(obj, lock='Z', axis='Y', target=B)
    constraints.locked_track(obj, lock='Z', axis='-Y', target=C)


def orthogonal_proj_to_line(obj, A, line, hide_extra=True):
    '''
    This function moves obj to the orthogonal projection in 2D of A on
    the line. The Y axis of obj is aligned with BC and the X axis
    is aligned with the perpendicular direction and the Z axis is the same
    as that of A.

    obj:      The object                (Blender Object)
    A:        Point to project from     (Blender Object)
    line:     line to project to        (Blender Object; Curve; Line)
    '''
    B = objects.new_point(hide=hide_extra)
    C = objects.new_point(hide=hide_extra)
    B.name = "line start"
    C.name = "line end"
    line_ends(B, C, line)

    orthogonal_proj_to_points(obj, A, B, C, hide_extra)


def orthogonal_line_to_line(perp_line, A, line, hide_extra=True):
    '''
    This function moves perp_line so that it is the normal to line
    through the point A. It is placed on the XY plane of the point A.
    perp_line and A have the same Z axis.

    The midpoint of the constructed orthogonal line is always placed
    at the foot of the orthogonality (so line is symmetric relative
    to the line it is orthogonal to)

    perp_line:      Line to place             (Blender Object; Curve; Line)
    A:              Point to project from     (Blender Object)
    line:           line to project to        (Blender Object; Curve; Line)
    '''
    objects.move_origin_center(perp_line)

    # The orthogonally_project already aligns everything for us. This function
    # is defined just for clear naming.
    orthogonal_proj_to_line(perp_line, A, line, hide_extra)


def orthogonal_line_to_points(perp_line, A, B, C, hide_extra=True):
    '''
    This function moves perp_line so that it is the normal to line defined
    by the points B, C and goes through the point A. It is placed on the XY
    plane of the point A. perp_line and A have the same Z axis.

    The midpoint of the constructed orthogonal line is always placed
    at the foot of the orthogonality (so line is symmetric relative
    to the line it is orthogonal to)

    perp_line:      Line to place             (Blender Object; Curve; Line)
    A:              Point to project from     (Blender Object)
    B, C:           Points defining line      (Blender Objects)
    '''
    objects.move_origin_center(perp_line)

    # The orthogonally_project already aligns everything for us. This function
    # is defined just for clear naming.
    orthogonal_proj_to_points(perp_line, A, B, C, hide_extra)


def bisecting_line_of_points(line, A, B, hide_extra=True):
    '''
    Given two points A, B on a 2D plane, construct the 2D perpendicular
    bisector.

    line:       Line to place             (Blender Object; Curve; Line)
    A, B:       Points defining line      (Blender Object)
    '''
    mid_point = objects.new_point(hide=hide_extra)
    mid_point.name = "midpoint"
    midpoint(mid_point, A, B)
    orthogonal_line_to_points(line, mid_point, A, B, hide_extra=hide_extra)


def bisecting_line_of_line(line, other_line, hide_extra=True):
    '''
    Given a line on a 2D plane, construct the 2D perpendicular bisector.

    line:           Line to place             (Blender Object; Curve; Line)
    other_line:     Line to bisect            (Blender Object; Curve; Line)
    '''
    mid_point = objects.new_point(hide=hide_extra)
    mid_point.name = "midpoint"
    constraints.position_on_curve(mid_point, other_line, position=0.5)
    constraints.copy_rotation(mid_point, other_line)

    orthogonal_line_to_line(line, mid_point, other_line, hide_extra=hide_extra)


# --------------------------------------------------------------------------- #
#                            REFLECTION                                       #
# --------------------------------------------------------------------------- #

def reflect_across_point(obj, A, point, hide_extra=True):
    '''
    Places an object to the relection of another point A relative to a given
    point.

    obj:        Object to place             (Blender Object)
    A:          Object to reflect           (Blender Object)
    B:          Point to reflect across     (Blender Object)
    '''
    drivers.add_driver(
        obj=obj,
        prop='location',
        fields='XYZ',
        vars_def={
            'o1': ('transform', A, 'location', '-'),
            'o2': ('transform', point, 'location', '-'),
        },
        expr='o1 + 2*(o2-o1)'
    )
    constraints.copy_rotation(obj, A)


def reflect_across_line(obj, A, line, hide_extra=True):
    '''
    Places the object to the relection of another point A relative to a given
    line.

    obj:        Object to place             (Blender Object)
    A:          Object to reflect           (Blender Object)
    B:          Line to reflect across      (Blender Object; Curve; Line)
    '''
    proje = objects.new_point(hide=hide_extra)
    proje.name = "orth. projection to line"
    orthogonal_proj_to_line(proje, A, line, hide_extra=hide_extra)

    reflect_across_point(obj, A, proje, hide_extra=hide_extra)


def reflect_across_line_of_points(obj, A, B, C, hide_extra=True):
    '''
    Places the object to the relection of another point A relative to the line
    defined by the points B, C.

    obj:        Object to place                     (Blender Object)
    A:          Object to reflect                   (Blender Object)
    B, C:       Defining Line to reflect across     (Blender Objects)
    '''
    proje = objects.new_point(hide=hide_extra)
    proje.name = "orth. projection to line"
    orthogonal_proj_to_points(proje, A, B, C, hide_extra=hide_extra)

    reflect_across_point(obj, A, proje, hide_extra=hide_extra)
