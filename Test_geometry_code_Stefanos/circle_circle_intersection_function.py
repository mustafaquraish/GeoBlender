
def circle_circle_intersection(int_1, int_2, A, B, hide_extra=True):
      
    '''
    Finds the intersections of two circles, A, B. It first places a hidden empty
    at the intersection of the radical axis and the line through the centers of 
    the circles A, B and then projects that empty to the circle A orthogonally.

    A, B:       2 circles        (Blender Objects; circle curves)
    puts at the intersection the two objects int_1, int_2

    Note: This method creates additional objects that are needed to help find
          the intersections. These are hidden by default
    '''

    # Place a hidden empty at the radical axis and the line connecting the centers
    int_center = new_empty(hide=hide_extra)
    put_at_radical_intercept(int_center, A, B)

    # Create a hidden cylinder whose Z axis coincides, in particular, with the Z 
    # axis of the circle A
    pr_cyl = new_cylinder(hide=hide_extra)
    copy_transforms(pr_cyl, target=A)

    # Project hidden empty on the mesh cylinder (projection points are on the circle)
    copy_location(int_1, int_center)
    copy_rotation(int_1, A)
    locked_track(int_1, lock='Z', axis='X', target=B)
    project_along_axis(int_1, axis='Y', target=pr_cyl)
      
    copy_location(int_2, int_center)
    copy_rotation(int_2, A)
    locked_track(int_2, lock='Z', axis='X', target=B)
    project_along_axis(int_2, axis='-Y', target=pr_cyl)


