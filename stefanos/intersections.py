from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

from ..stefanos.circles import *
from ..stefanos.inversion import *
from ..stefanos.lines import *
from ..stefanos.triangle_constructions import *

def line_line_inteserction(obj, line1, line2, hide_extra=True):

    ''' 
    This function moves obj to the intersection of two lines.
    We need to re-orient appropriately intersection after using this
    function. 
    '''

    a_start = new_empty(hide=hide_extra)
    position_on_curve(a_start, line1, 0)

    a_end = new_empty(hide=hide_extra)
    position_on_curve(a_end, line1, 1)

    pr_plane = new_plane(hide=hide_extra)
    make_orthogonal_to(pr_plane, a_start, a_end, line2)

    copy_transforms(obj, line2 , transforms='LR')
    project_along_axis(obj, 'X', target=pr_plane, opposite=True)
    
    




def line_circle_intersections(inter1, inter2, line, circle, hide_extra=True):
    '''
    This function moves  inter1 and inter2 to the intersection points of a 
    line and a circle. Intersections have same orientation as circle.  
    (see the extra copy rotation constraint at the end).
    '''

    line2 = new_line(hide=hide_extra)
    move_origin_center(line2, center='MEDIAN')
    # Make the line really large to ensure it encompasses the circle
    line2.scale.z = 10e4
    copy_transforms(line2, line, transforms='LR')

    pr_cyl = new_cylinder(vert=1000, hide=self.hide_extra)
    copy_transforms(pr_cyl, circle, transforms='LR')
    copy_scale(pr_cyl, target=circle, axes='XY')  # Don't copy Z scale

    inter_1 = new_empty()
    position_on_curve(inter_1, line2, position=0)
    copy_rotation(inter_1, line2)
    project_along_axis(inter_1, 'X', target=pr_cyl, opposite=True)
    copy_rotation(inter_1, circle)
    inter_1.name = "Intersection 1"

    inter_2 = new_empty()
    position_on_curve(inter_2, line2, position=1)
    copy_rotation(inter_2, line2)
    project_along_axis(inter_2, 'X', target=pr_cyl, opposite=True)
    copy_rotation(inter_2, circle)
    inter_2.name = "Intersection 2"

    

    


def circle_circle_intersection(int_1, int_2, A, B, hide_extra=True):
      
    '''
    Finds the intersections of two circles, A, B. It first places a hidden empty
    at the intersection of the radical axis and the line through the centers of 
    the circles A, B and then projects that empty to the circle A orthogonally.
    Intersections have same orientation as circle A.  

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
