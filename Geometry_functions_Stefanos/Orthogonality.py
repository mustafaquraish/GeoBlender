# The next two functions heavily use that the Z axis of points is 
# normal to the parent plane.

def orthogonal_projection(obj, A, line, hide_extra=True):

   ''' 
    This function moves obj to the orthogonal projection in 2D of A on 
    the line. The X axis  of obj is aligned with BC and the Y axis
    is alighned with the perpendicular direction. A must be the active object.
    '''

    B = new_empty(hide=hide_extra)
    position_on_curve(B, line, 0)

    C = new_empty(hide=hide_extra)
    position_on_curve(C, line, 1)

    pr_plane = new_plane(hide=hide_extra)
    pr_plane.name = "projection plane"
    make_orthogonal_to(pr_plane, B, C, A, axis='Z')

    
    copy_location(obj, A)
    copy_rotation(obj, A)
    project_nearest(obj, target=pr_plane)
    locked_track(obj, lock='Z', axis='X', target=B)
    locked_track(obj, lock='Z', axis='-X', target=C)

    
def orthogonal_line(A, line, length=100, hide_extra=True):

   ''' 
    This function creates the normal line of length to a line through 
    a point A. 
    '''

    B = new_empty(hide=hide_extra)
    position_on_curve(B, line, 0)

    C = new_empty(hide=hide_extra)
    position_on_curve(C, line, 1)

    proje = new_empty(hide=hide_extra)
    orthogonal_projection(proje, A, B, C)

    line0 = new_line(length = 2, axis='Y', hide=hide_extra)
    move_origin_center(line0)
    copy_location(line0, proje)
    copy_rotation(line0, proje)
    

    # This line is normal to BC and parallel to its Y axis. So we need to change 
    # this to Z. We do this by creating a new line. 

    point0 = new_empty(hide=hide_extra)
    position_on_curve(point, line0, position=1, influence=1)

    perp_line = new_line(length, axis='Z')
    move_origin_center(perp_line)
    copy_location(perp_line, proje)
    damped_track(perp_line, 'Z', point0)



def perpendicular_bisector_plane(obj, A, B, hide_extra=True):
    '''
    Align the obj (a plane) to the perpendicular bisector plane of
    the segment AB. The Z axis of the returned obj is parallel to AB.
    The X, Y axis are not determined. 
    
    A, B:       2 points        (Blender Objects; circle curves)
    
    '''

    put_in_between(obj, A, B)
    damped_track(plane, axis='Z', target=A)
    plane.name = "Perp. Bisector Plane"


def perpendicular_bisector_from_points(A, B, length, hide_extra = True):
    '''
    Given two points A, B on a 2D plane, construct the 2D perpendicular 
    bisector.
    '''

    mid_point=new_empty(hide=hide_extra)
    orthogonal_projection(mid_point, A, B) # Y axis of mid_point is perp to AB

    orthogonal_line(mid_point, A, B, length)


def perpendicular_bisector_of_line(line, length, hide_extra = True):
     '''
    Given a line on a 2D plane, construct the 2D perpendicular 
    bisector (line).
    '''

    B = new_empty(hide=hide_extra)
    position_on_curve(B, line, 0)

    C = new_empty(hide=hide_extra)
    position_on_curve(C, line, 1)

    mid_point=new_empty(hide=hide_extra)
    orthogonal_projection(mid_point, B, C) # Y axis of mid_point is perp to AB

    orthogonal_line(mid_point, B, C, length)
