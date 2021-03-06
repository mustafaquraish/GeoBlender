from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects

from . import core
from . import circles
from . import lines


def line_line_intersection(inter, line1, line2, hide_extra=True):
    '''
    This function moves obj to the intersection of two lines.
    We need to re-orient appropriately intersection after using this
    function.
    '''

    A = objects.new_empty(hide=hide_extra)
    B = objects.new_empty(hide=hide_extra)
    lines.line_ends(A, B, line1)

    pr_plane = objects.new_plane(hide=hide_extra)
    core.make_orthogonal_to(pr_plane, A, B, line2)

    constraints.copy_transforms(inter, line2, transforms='LR')
    constraints.project_along_axis(inter, 'X', target=pr_plane, opposite=True)


def line_circle_intersection(inter1, inter2, line, circle, hide_extra=True):
    '''
    This function moves  inter1 and inter2 to the intersection points of a
    line and a circle. Intersections have same orientation as circle.
    (see the extra copy rotation constraint at the end).
    '''

    line2 = objects.new_line(hide=hide_extra)
    objects.move_origin_center(line2, center='MEDIAN')

    # Make the line really large to ensure it encompasses the circle
    objects.uniform_scale(line2, 10e4)
    constraints.copy_transforms(line2, line, transforms='LR')

    pr_cyl = objects.new_cylinder(vert=1000, hide=hide_extra)
    constraints.copy_transforms(pr_cyl, circle)

    lines.line_ends(inter1, inter2, line2)

    constraints.project_along_axis(inter1, 'X', target=pr_cyl, opposite=True)
    constraints.copy_rotation(inter1, circle)
    inter1.name = "Intersection 1"

    constraints.project_along_axis(inter2, 'X', target=pr_cyl, opposite=True)
    constraints.copy_rotation(inter2, circle)
    inter2.name = "Intersection 2"


def circle_circle_intersection(inter1, inter2, A, B, hide_extra=True):
    '''
    Finds the intersections of two circles, A, B. It first places a hidden empty
    at the intersection of the radical axis and the line through the centers of
    the circles A, B and then projects that empty to the circle A orthogonally.
    Intersections have same orientation as circle A.

    A, B:       2 circles        (Blender Objects; circle curves)
    puts at the intersection the two objects inter1, inter2

    Note: This method creates additional objects that are needed to help find
          the intersections. These are hidden by default
    '''

    # Place a hidden empty at the radical axis and the line connecting the
    # centers
    int_center = objects.new_empty(hide=hide_extra)
    int_center.name = "radical axis intercept"
    circles.radical_intercept(int_center, A, B)

    # Create a hidden cylinder whose Z axis coincides, in particular, with the
    # Z axis of the circle A
    pr_cyl = objects.new_cylinder(hide=hide_extra)
    pr_cyl.name = "projection cylinder"
    constraints.copy_transforms(pr_cyl, target=A)

    # Project hidden empty on the mesh cylinder (projection points are on the
    # circle)
    constraints.copy_transforms(inter1, int_center, transforms='LR')
    constraints.locked_track(inter1, lock='Z', axis='X', target=B)
    constraints.project_along_axis(inter1, axis='Y', target=pr_cyl)

    constraints.copy_transforms(inter2, int_center, transforms='LR')
    constraints.locked_track(inter2, lock='Z', axis='X', target=B)
    constraints.project_along_axis(inter2, axis='-Y', target=pr_cyl)


###############################################################################
#                           3D INTERSECTIONS                                  #
###############################################################################

def plane_plane_intersection(inter, plane1, plane2, hide_extra=True):
    '''
    This function moves the line to the intersection of two plane.
    '''

    pass


def plane_sphere_intersection(circle, plane, sphere, hide_extra=True):
    '''
    This function moves the circle to the intersection of a plane and sphere.
    '''
    import bpy
    size = bpy.context.scene.geoblender_settings.plane_size
    plane_copy = objects.new_plane(size=size, hide=hide_extra)
    constraints.copy_transforms(plane_copy, plane, transforms='LR')

    proj = objects.new_empty(hide=hide_extra)
    constraints.copy_location(proj, sphere)
    constraints.project_nearest(proj, target=plane_copy, align_to_normal='Z')

    pt = objects.new_point(hide=hide_extra)
    constraints.copy_transforms(pt, proj, transforms='LR')
    constraints.project_along_axis(pt, axis='X', target=sphere)

    circles.circle_from_center_point(circle, proj, pt)


def sphere_sphere_intersection(circle, sphere1, sphere2, hide_extra=True):
    '''
    This function moves the circle to the intersection of 2 spheres.
    '''
    pt = objects.new_empty(hide=hide_extra)
    circles.radical_intercept(pt, sphere1, sphere2, align_2D=False)

    pt2 = objects.new_empty(hide=hide_extra)
    constraints.copy_transforms(pt2, pt, transforms='LR')
    constraints.project_along_axis(pt2, axis='X', target=sphere1)

    circles.circle_from_center_point(circle, pt, pt2)
