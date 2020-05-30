from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import circles
from . import lines
from . import intersections


# --------------------------------------------------------------------------- #
#                          INVERSION OF POINTS                                #
# --------------------------------------------------------------------------- #

def inversion_point(inv_point, point, circle_of_inv, hide_extra=True):
    '''
    Places a point (inverted_point) to the inversion defined by the
    circle_of_inversion (see also comments above).

    inv_point:      Point to place          (Blender Object)
    point:          Point to invert         (Blender Object)
    circle_of_inv:  Circle of inversion     (Blender Object; Curve; Circle)
    '''
    constraints.copy_rotation(inv_point, point)
    drivers.add_driver(
        obj=inv_point,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('transform', circle_of_inv, 'scale', 'X'),
            'r': ('distance', point, circle_of_inv),
            'o1': ('transform', circle_of_inv, 'location', '-'),
            'o2': ('transform', point, 'location', '-'),
        },
        expr='gb_inversion_expres(d, r, o1, o2)'
    )


# --------------------------------------------------------------------------- #
#                          INVERSION OF CIRCLES                               #
# --------------------------------------------------------------------------- #

def inversion_on_cicle(inv_circle, circle, circle_of_inv, hide_extra=True):
    '''
    Places a line (inverted_circle) to the inversion defined by the
    circle_of_inversion. The origin of the inversion should be
    constrained on the circle.

    inv_circle:      Circle to place        (Blender Object; Curve; Circle)
    circle:          Circle to invert       (Blender Object; Curve; Circle)
    circle_of_inv:   Circle of inversion    (Blender Object; Curve; Circle)
    '''
    connecting_line = objects.new_line(hide=hide_extra)
    connecting_line.name = "connecting line"
    lines.segment(connecting_line, circle_of_inv, circle)

    antipodal = objects.new_point(hide=hide_extra)
    antipodal.name = "antipodal"
    lines.reflect_across_point(antipodal, circle_of_inv, circle)

    inversion_inter = objects.new_point(hide=hide_extra)
    inversion_inter.name = "inversion intersection"
    constraints.copy_rotation(inversion_inter, circle_of_inv)

    drivers.add_driver(
        obj=inversion_inter,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('transform', circle_of_inv, 'scale', 'X'),
            'r': ('transform', circle, 'scale', 'X'),
            'o1': ('transform', circle_of_inv, 'location', '-'),
            'o2': ('transform', antipodal, 'location', '-'),
        },
        expr='gb_inversion_expres(d, r, o1, o2)'
    )
    lines.orthogonal_line_to_line(inv_circle, inversion_inter, connecting_line)


def inversion_not_on_circle(inv_circle, inv_center, circle,
                            circle_of_inv, hide_extra=True):
    '''
    Places a circle (inverted_circle), with center the inverted_center,
    to the inversion of a given circle (circle). The inversion is defined
    by the circle_of_inversion. The origin of the inversion should not be
    constrained on the circle.

    inv_circle:      Circle to place        (Blender Object; Curve; Circle)
    inv_center:      Inverted center        (Blender Object)
    circle:          Circle to invert       (Blender Object; Curve; Circle)
    circle_of_inv:   Circle of inversion    (Blender Object; Curve; Circle)
    '''
    connecting_line = objects.new_line(hide=hide_extra)
    connecting_line.name = "connecting line"
    lines.segment(connecting_line, circle_of_inv, circle)

    inter1 = objects.new_point(hide=hide_extra)
    inter1.name = "interesction 1"
    inter2 = objects.new_point(hide=hide_extra)
    inter2.name = "interesction 2"

    intersections.line_circle_intersections(
        inter1,
        inter2,
        connecting_line,
        circle
    )
    # inter1 and inter2 have the orientation of the circle

    inter1_inverted = objects.new_point(hide=hide_extra)
    inter1_inverted.name = "interesction 1 inverted"
    inter2_inverted = objects.new_point(hide=hide_extra)
    inter2_inverted.name = "interesction 2 inverted"

    inversion_point(inter1_inverted, inter1, circle_of_inv)
    inversion_point(inter2_inverted, inter2, circle_of_inv)

    circles.circle_from_diameter(inv_circle, inter1_inverted, inter2_inverted)
    lines.midpoint(inv_center, inter1_inverted, inter2_inverted)


# --------------------------------------------------------------------------- #
#                          INVERSION OF LINES                                 #
# --------------------------------------------------------------------------- #

def inversion_on_line(inv_line, line, circle_of_inv, hide_extra=True):
    '''
    Places a line to the inversion of another line defined by the given circle
    of inversion. The origin of inversion should be constrained on the line.

    inv_line:        Line to place          (Blender Object; Curve; Line)
    line:            Line to invert         (Blender Object; Curve; Line)
    circle_of_inv:   Circle of inversion    (Blender Object; Curve; Circle)
    '''
    # The inversion line is the same. Here we just make it a full line to show.
    objects.move_origin_center(inv_line)
    constraints.copy_transforms(inv_line, target=line, transforms='LR')
    objects.uniform_scale(inv_line, 100)


def inversion_line_not_on(inv_circle, line, circle_of_inv, hide_extra=True):
    '''
    Places a circle (inv_line) to the inversion of a line (line) defined
    by the circle_of_inv. The origin of the inversion should not be
    constrained on the line.

    inv_circle:      Circle to place        (Blender Object; Curve; Circle)
    line:            Line to invert         (Blender Object; Curve; Line)
    circle_of_inv:   Circle of inversion    (Blender Object; Curve; Circle)
    '''
    proje = objects.new_point(hide=hide_extra)
    proje.name = "projection onto line"
    inverted_point = objects.new_point(hide=hide_extra)
    inverted_point.name = "inverted point"

    lines.orthogonal_proj_to_line(proje, circle_of_inv, line)
    inversion_point(inverted_point, proje, circle_of_inv)
    circles.circle_from_diameter(inv_circle, circle_of_inv, inverted_point)
