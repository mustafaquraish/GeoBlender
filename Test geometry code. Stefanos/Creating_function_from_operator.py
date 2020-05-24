
def circle_circle_intersection(A, B, hide_extra=True):
    '''
    Finds the intersections of two circles, A, B. It first places a hidden empty at the intersection
    of the radical axis and the line through the centers of the circles A, B and then projects that 
    empty to the circle A orthogonally.

    A, B:       2 circles        (Blender Objects; circle curves)
    returns to empties (even if they coincide; in the tangential case)

    Note: This method creates additional objects that are needed to help find
          the intersections. These are hidden by default
    '''
    #place a hidden empty at the radical axis and the line connecting the centers
    int_center = new_empty(hide=hide_extra)
    put_at_radical_intercept(int_center, A, B)

    #create a hidden cylinder whose Z axis coincides, in particular, with the Z axis of the circle A
    pr_cyl = new_cylinder(hide=hide_extra)
    copy_transforms(pr_cyl, target=A)

    #project hidden empty on the mesh cylinder (projection points are on the circle)
    int_1 = new_empty()
    copy_location(int_1, int_center)
    copy_rotation(int_1, A)
    locked_track(int_1, lock='Z', axis='X', target=B)
    project_along_axis(int_1, axis='Y', target=pr_cyl)

    int_2 = new_empty()
    copy_location(int_2, int_center)
    copy_rotation(int_2, A)
    locked_track(int_2, lock='Z', axis='X', target=B)
    project_along_axis(int_2, axis='-Y', target=pr_cyl)

'''
Do I need to incldue the name of the hidden and the visible obljects that we create here? (yes..)
'''

'''
What about the arguments of the circle_circle_intersection function? should they just be the given 
circles A,B and then we return the empties, or should we define the empties before the function and 
put them in the function as argument (in which case we will have four arguments)? If this is better, 
then maybe change the geometry functions as well to simply return the desired object without having 
to accept it as argument in the first place?
'''

'''
it would be very nice if we define a new function that test if two circles do not intersect, are
tangent, or intersect at two distinct points (again to some numerical accuracy based on the distance
of the int_1 and int_2 empties above
'''