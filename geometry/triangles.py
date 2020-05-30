from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import lines
from . import circles
from . import intersections


# --------------------------------------------------------------------------- #
#                         MEDIANS, BARYCENTER                                 #
# --------------------------------------------------------------------------- #

def median(line, mid_point, A, B, C, hide_extra=True):
    '''
    Places the median (line) and the midpoint (point) of the
    triangle ABC from A.
    line:       Line to make median         (Blender Object; Curve; Line)
    mid_point:  Point to place at foot      (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    lines.midpoint(mid_point, B, C, influence=0.5)
    lines.segment(line, A, mid_point)

# STEFANOS:
# While i like the idea of using the intersection functions here...
# I think it is unnecessarily overkill. We add so many more objects and
# complexity to the scene when doing it this way. Doing it directly
# like in ..utils.geometry.put_at_barycenter() would be a lot more
# efficient, no? Same for the other centers...


def barycenter(point, A, B, C, hide_extra=True):
    '''
    Places the barycenter (point) of the triangle ABC.
    point;      Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    median1 = objects.new_line(hide=hide_extra)
    median2 = objects.new_line(hide=hide_extra)
    median1.name = "median 1"
    median2.name = "median 2"
    mid1 = objects.new_point(hide=hide_extra)
    mid2 = objects.new_point(hide=hide_extra)
    mid1.name = "midpoint 1"
    mid2.name = "midpoint 2"

    median(median1, mid1, A, B, C)
    median(median2, mid2, A, B, C)
    intersections.line_line_inteserction(
        inter=point, 
        line1=median1, 
        line2=median2, 
        hide_extra=hide_extra
    )


# --------------------------------------------------------------------------- #
#                       ALTITUDE, ORTHOCENTER                                 #
# --------------------------------------------------------------------------- #


def altitude(line, point, A, B, C, hide_extra=True):
    '''
    Places the altitude (line) and its foot (point) of the
    triangle ABC from A.
    line:       Line to make altitude       (Blender Object; Curve; Line)
    point:      Point to place at foot      (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    lines.orthogonal_proj_to_points(point, A, B, C, hide_extra=hide_extra)
    lines.segment(line, A, point)


def orthocenter(point, A, B, C, hide_extra=True):
    '''
    Places the orthocenter (point) of the triangle ABC.
    point;      Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    altitude1 = objects.new_line(hide=hide_extra)
    altitude2 = objects.new_line(hide=hide_extra)
    altitude1.name = "altitude 1"
    altitude2.name = "altitude 2"

    lines.orthogonal_line_to_points(altitude1, A, B, C, hide_extra=hide_extra)
    lines.orthogonal_line_to_points(altitude2, B, A, C, hide_extra=hide_extra)

    intersections.line_line_inteserction(
        inter=point, 
        line1=altitude1, 
        line2=altitude2, 
        hide_extra=hide_extra
    )


# --------------------------------------------------------------------------- #
#                      CIRCUMCENTER, CIRCUMCIRCLE                             #
# --------------------------------------------------------------------------- #

def circumcenter(point, A, B, C, hide_extra=True):
    '''
    Places the circumcenter (point) of the triangle ABC. It has the same
    orientation as A.
    point;      Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    perp1 = objects.new_line(hide=hide_extra)
    perp2 = objects.new_line(hide=hide_extra)
    perp1.name = "perp. bisector 1"
    perp2.name = "perp. bisector 2"
    lines.bisecting_line_of_points(perp1, A, B)
    lines.bisecting_line_of_points(perp1, A, C)

    intersections.line_line_inteserction(
        inter=point, 
        line1=perp1, 
        line2=perp2, 
        hide_extra=hide_extra
    )


def circumcircle(circle, center, A, B, C, hide_extra=True):
    '''
    Places the circumcircle (circle) of the triangle ABC. It has the same
    orientation as A. It also places its centre (optionally).
    circle:     Circle to place             (Blender Object; Curve; Circle)
    center:     Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    circumcenter(center, A, B, C)
    circles.circle_from_center_point(circle, center, A)


# --------------------------------------------------------------------------- #
#                  EULER CENTER, CIRCLE, LINE                                 #
# --------------------------------------------------------------------------- #

def euler_center(point, A, B, C, hide_extra=True):
    '''
    Places the Euler center (point) of the triangle ABC. It is
    returned with the same orientation as the point A.
    point;      Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    circum = objects.new_point(hide=hide_extra)
    circum.name = "circumcenter"
    circumcenter(circum, A, B, C)

    ortho = objects.new_point(hide=hide_extra)
    ortho.name = "orthocenter"
    orthocenter(ortho, A, B, C)

    lines.midpoint(point, circum, ortho)


def euler_line(line, A, B, C, hide_extra=True):
    '''
    Places the Euler line (line) of the triangle ABC.
    line:       Line to place           (Blender Object; Curve; Line)
    A, B, C:    Points of triangle      (Blender Objects)
    '''

    circum = objects.new_point(hide=hide_extra)
    circum.name = "circumcenter"
    circumcenter(circum, A, B, C)

    ortho = objects.new_point(hide=hide_extra)
    ortho.name = "orthocenter"
    orthocenter(ortho, A, B, C)

    lines.line(line, circum, ortho)


def euler_circle(circle, center, A, B, C, hide_extra=True):
    '''
    Places the Euler circle (circle) of the triangle ABC.
    It has the same orientation as A. Places its center (optionally).
    circle:     Circle to place             (Blender Object; Curve; Circle)
    center:     Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    euler_center(center, A, B, C)

    mid_point = objects.new_point(hide=hide_extra)
    lines.midpoint(mid_point, B, C)

    circles.circle_from_center_point(circle, center, mid_point)


# --------------------------------------------------------------------------- #
#                       ANGLE BISECTORS                                       #
# --------------------------------------------------------------------------- #

def angle_bisector_foot(point, A, B, C, hide_extra=True):
    '''
    Places the angle bisector foot on BC of the angle BAC.
    point:      Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''

    pr_plane = objects.new_plane(hide=hide_extra)
    pr_plane.name = "projection plane"
    core.make_orthogonal_to(pr_plane, C, B, A)

    constraints.copy_transforms(point, A, transforms='LR')
    core.track_to_angle_between(point, B, C)
    constraints.project_along_axis(
        point,
        axis='X',
        target=pr_plane,
        opposite=True
    )


def angle_bisector(line, point, A, B, C, hide_extra=True):
    '''
    Places the angle bisector of the angle BAC.
    line:       Line to make bisector       (Blender Object; Curve; Line)
    point:      Point to place at foot      (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    angle_bisector_foot(point, B, A, C, hide_extra=hide_extra)
    lines.segment(line, A, point)


def external_bisector(line, A, B, C, hide_extra=True):
    '''
    Places the external angle bisector (line) of the angle BAC.
    
    line:       Line to make bisector       (Blender Object; Curve; Line)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    internal = objects.new_line(hide=hide_extra)
    internal.name = "internal bisector"
    foot = objects.new_point(hide=hide_extra)
    foot.name = "bisector foot"
    angle_bisector(internal, foot, A, B, C)
    lines.orthogonal_line_to_line(line, A, internal, hide_extra=hide_extra)


# --------------------------------------------------------------------------- #
#                  INCENTER/CIRCLE, EXCENTER/CIRCLE                           #
# --------------------------------------------------------------------------- #

def incenter(point, A, B, C, hide_extra=True):
    '''
    Places the incenter  (point) of the triangle ABC. It has the
    same orientation as A.
    point:      Point to place at incenter      (Blender Object)
    A, B, C:    Points of triangle              (Blender Objects)
    '''
    bisec1 = objects.new_line(hide=hide_extra)
    bisec2 = objects.new_line(hide=hide_extra)
    bisec1.name = "bisector 1"
    bisec2.name = "bisector 2"
    foot1 = objects.new_point(hide=hide_extra)
    foot2 = objects.new_point(hide=hide_extra)
    foot1.name = "bisector foot 1"
    foot2.name = "bisector foot 2"

    angle_bisector(bisec1, foot1, A, B, C)
    angle_bisector(bisec2, foot2, B, A, C)

    intersections.line_line_inteserction(
        inter=point, 
        line1=bisec1, 
        line2=bisec2, 
        hide_extra=hide_extra
    )


def incircle(circle, center, A, B, C, hide_extra=True):
    '''
    Places the incircle (circle) of the triangle ABC. It has the same 
    orientation as A.  Places also the center (optionally).
    circle:     Circle to place             (Blender Object; Curve; Circle)
    center:     Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''

    incenter(center, A, B, C)

    proje = objects.new_point(hide=hide_extra)
    proje.name = "circle point"
    lines.orthogonal_proj_to_points(proje, center, B, C)

    circles.circle_from_center_point(circle, center, proje)


def excenter(point, A, B, C, hide_extra=True):
    '''
    Places the excenter (point) of the triangle ABC opposite to A. It has the
    same orientation as A.
    point:      Point to place at incenter      (Blender Object)
    A, B, C:    Points of triangle              (Blender Objects)
    '''
    bisec1 = objects.new_line(hide=hide_extra)
    bisec2 = objects.new_line(hide=hide_extra)
    bisec1.name = "external bisector 1"
    bisec2.name = "external bisector 2"

    external_bisector(bisec1, A, B, C)
    external_bisector(bisec2, B, A, C)

    intersections.line_line_inteserction(
        inter=point, 
        line1=bisec1, 
        line2=bisec2, 
        hide_extra=hide_extra
    )


def excircle(circle, center, A, B, C, hide_extra=True):
    '''
    Places the excircle (circle) of the triangle ABC opposite to A.
    It has the same orientation as A.  Places its center (optionally).
    circle:     Circle to place             (Blender Object; Curve; Circle)
    center:     Point to place              (Blender Object)
    A, B, C:    Points of triangle          (Blender Objects)
    '''
    excenter(center, A, B, C)

    proje = objects.new_point(hide=hide_extra)
    proje.name = "circle point"
    lines.orthogonal_proj_to_points(proje, center, B, C)

    circles.circle_from_center_point(circle, center, proje)