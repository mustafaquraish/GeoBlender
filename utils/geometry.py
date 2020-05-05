from .constraints import copy_location
from .constraints import damped_track, locked_track
from .constraints import project_along_axis, project_nearest
from .drivers import add_driver_distance
from .objects import new_empty, new_plane

PLANE_SIZE = 300


def align_to_plane_of(obj, A, B, C):
    '''
    Aligns an object to the plane defined by 3 points

    obj:        Source object (Blender Object)
    A, B, C:    3 points      (Blender Objects)
    '''
    copy_location(obj, target=A)
    damped_track(obj, axis='X', target=B)
    locked_track(obj, axis='Y', lock='X', target=C)


def track_to_angle_between(obj, A, B, axes='XYZ', influence=0.5):
    '''
    Make the given axis of the object point towards the bisector (or other 
    intermediary angle) of the angle formed by the lines to A and B.

    obj:        Source object   (Blender Object)
    A, B:       2 Objects       (Blender Objects)
    axes:       Axes (in order) ('XYZ', 'XZY', 'YZX', ...)
    influence   Influence       (float, 0-1)
    '''
    damped_track(obj, axis=axes[0].upper(), target=A)
    locked_track(obj, axis=axes[1].upper(), lock=axes[0].upper(), target=B)
    locked_track(obj, axis=axes[0].upper(), lock=axes[2].upper(), target=B,
                 influence=influence)


def make_orthogonal_to(obj, A, B, C, axis='Z'):
    '''
    Aligns the object so that the object is on the line AB, and the given
    axis points towards C.

    obj:        Source Object       (Blender object)
    A, B, C:    3 points            (Blender Objects)  
    axis:       Axis pointing to C  ('X', 'Y' or 'Z')
    '''
    copy_location(obj, target=A)
    damped_track(obj, axis='X', target=B)
    locked_track(obj, axis='Z', lock='X', target=C)


def put_in_between(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that 
        (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)
    '''

    # Note that location of B is copied first to make influence consistent
    copy_location(obj, target=B)
    copy_location(obj, target=A, influence=influence)


def put_at_circumcenter(obj, A, B, C, hide_extra=True):
    '''
    Constrain the given object at the circumcenter of 3 points. 

    obj:        Source object   (Blender Object)
    A, B, C:    3 points        (Blender Objects)

    Note: This method creates additional objects that are needed to help find
          the circumcenter. These are hidden by default.
    '''
    # Construct the perp. bisector plane of A-B
    ab_perp_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    ab_perp_plane.name = "perpendicular plane"
    put_in_between(ab_perp_plane, A, B, influence=0.5)
    damped_track(ab_perp_plane, axis='Z', target=A)

    # Put the object at the midpoint of A-C, and align it with the triangle.
    put_in_between(obj, A, C, influence=0.5)
    damped_track(obj, axis='X', target=A)
    locked_track(obj, lock='X', axis='Y', target=B)

    # Project it onto the plane from above to get the circumcenter
    project_along_axis(obj, axis='+Y', target=ab_perp_plane, opposite=True)


def put_at_barycenter(obj, A, B, C, hide_extra=True):
    '''
    Constrain the given object at the barycenter of 3 points. 

    obj:        Source object   (Blender Object)
    A, B, C:    3 points        (Blender Objects)

    Note: This method creates additional objects that are needed to help find
          the circumcenter. These are hidden by default.
    '''
    # Construct the plane going through mid-AB and C, perp to plane.
    ab_mid_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    ab_mid_plane.name = "plane through midpoint"
    put_in_between(ab_mid_plane, A, B, influence=0.5)
    damped_track(ab_mid_plane, axis='X', target=C)
    locked_track(ab_mid_plane, axis='Z', lock='X', target=A)

    # Project mid-AC going towards B.
    put_in_between(obj, A, C, influence=0.5)
    damped_track(obj, axis='X', target=B)
    locked_track(obj, axis='Y', lock='X', target=A)
    project_along_axis(obj, axis='X', target=ab_mid_plane, opposite=True)


def put_at_orthocenter(obj, A, B, C, hide_extra=True):
    '''
    Constrain the given object at the orthocenter of 3 points. 

    obj:        Source object   (Blender Object)
    A, B, C:    3 points        (Blender Objects)

    Note: This method creates additional objects that are needed to help find
          the circumcenter. These are hidden by default.
    '''
    # Construct planes going through AB and BC, orthogonal to the plane
    # containing the triangle ABC.
    ab_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    ab_plane.name = "side 1 orth plane"
    make_orthogonal_to(ab_plane, A, B, C)

    bc_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    bc_plane.name = "side 2 orth plane"
    make_orthogonal_to(bc_plane, B, C, A)

    # Form the projections of A and C onto the opposite planes. Note that
    # this is because we omitted side CA above, and don't need to consider
    # the projection of B
    proj_a = new_empty(hide=hide_extra)
    proj_a.name = "projection of vertex 1"
    copy_location(proj_a, target=A)
    project_nearest(proj_a, target=bc_plane)

    proj_c = new_empty(hide=hide_extra)
    proj_c.name = "projection of vertex 3"
    copy_location(proj_c, target=C)
    project_nearest(proj_c, target=ab_plane)

    # Now we want the intersection of the lines a-proj_a and c-proj_c
    # Use the plane-project method to do this. First, a-proj_a plane
    pr_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    pr_plane.name = "projection plane"
    make_orthogonal_to(pr_plane, proj_a, A, B)

    # Now project from c onto the plane along the axis pointing to proj_c.
    copy_location(obj, target=C)
    damped_track(obj, axis='X', target=proj_c)
    locked_track(obj, axis='Y', lock='X', target=A)
    project_along_axis(obj, axis='X', target=pr_plane, opposite=True)


def put_at_incenter(obj, A, B, C, hide_extra=True):
    '''
    Constrain the given object at the incenter of 3 points. 

    obj:        Source object   (Blender Object)
    A, B, C:    3 points        (Blender Objects)

    Note: This method creates additional objects that are needed to help find
          the circumcenter. These are hidden by default.
    '''
    # Find intersection of projections on opposite plane along bisectors
    pr_plane = new_plane(size=PLANE_SIZE, hide=hide_extra)
    pr_plane.name = "projection plane"
    copy_location(pr_plane, target=A)
    # Using axes="XZY" here since we the plane to be orth. to the
    track_to_angle_between(pr_plane, B, C, axes='XZY')

    copy_location(obj, target=C)
    track_to_angle_between(obj, B, A)
    project_along_axis(obj, axis='X', target=pr_plane, opposite=True)


def stretch_between_points(obj, A, B, axis='Z', scale=1):
    '''
    'Stretch' the object from one point to another. Effectively, copy
    location of A, align to B and stretch the given axis to length A-B.

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    copy_location(obj, target=A)
    damped_track(obj, axis=axis.upper(), target=B)
    add_driver_distance(obj, 'scale', axis * scale, A, B)
