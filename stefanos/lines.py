from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

from .circles import *
from .intersections import *
from .inversion import *
from .triangle_constructions import *

def segment(line, A, B):
    '''
    This function returns line to the segment defined by 
    the points A, B.
    '''
    copy_location(obj, target=A)
    copy_rotation(obj, A)
    locked_track(obj, lock='Z', axis='X', target=B)

    add_driver_distance(
        obj=obj,
        prop='scale',
        fields='XYZ',
        A=A,
        B=B,
        scale=scale
    )



def ray(line, A, B):
    '''
    Places a full line (line) through the points A, B. Effectively, copy 
    location of A, align to B and stretch the given axis a desired amount 
    (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    copy_location(obj, target=A)
    copy_rotation(obj, A)
    locked_track(obj, lock='Z', axis='X', target=B)
    add_driver(line, 'scale', fields='XYZ', vars_def={}, expr="1000")
    


def full_line(line, A, B):
    '''
    Places a full line (line) through the points A, B. her. Effectively, move 
    center at the middle point of the line, copy location of A, align to B 
    and stretch the given axis a desired amount (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    move_origin_center(line, center='MEDIAN')
    copy_location(obj, target=A)
    copy_rotation(obj, A)
    locked_track(obj, lock='Z', axis='X', target=B)
    add_driver(line, 'scale', fields='XYZ', vars_def={}, expr="1000")

def midpoint(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that
        (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)
    Midpoint takes the orientation of A
    '''

    # Note that location of B is copied first to make influence consistent
    copy_location(obj, target=B)
    copy_location(obj, target=A, influence=influence)
    copy_rotation(obj, A)


###############################################################################
# Parallel lines

def parallel_line(parallel_line, A, line, hide_extra=True):

    '''
    This function places a line (parallel_line) to go through a point A and
    be parallel to a line.
    '''
    move_origin_center(parallel_line, center='MEDIAN')
    copy_location(parallel_line, A)
    copy_rotation(parallel_line, line)

###############################################################################
# Orthogonality

# The next two functions heavily use that the Z axis of points is 
# normal to the parent plane.

def orthogonal_projection(obj, A, line, hide_extra=True):

    ''' 
    This function moves obj to the orthogonal projection in 2D of A on 
    the line. The X axis  of obj is aligned with BC and the Y axis
    is aligned with the perpendicular direction and the Z axis is the same
    as that of A. A must be the active object.
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
    

def orthogonal_line(perp_line, A, line,  hide_extra=True):

    ''' 
    This function moves perp_line so that it is the normal to line 
    through the point A. It is placed on the XY plane of the point A.
    perp_line and A have the same Z axis.

    The midpoint of the constructed orthogonal line is always placed
    at the foot of the orthogonality (so line is symmetric relative
    to the line it is orthogonal to)
    '''

    B = new_empty(hide=hide_extra)
    position_on_curve(B, line, 0)

    C = new_empty(hide=hide_extra)
    position_on_curve(C, line, 1)

    proje = new_empty(hide=hide_extra)
    orthogonal_projection(proje, A, line)

    line0 = new_line(length = 2, axis='Y', hide=hide_extra)
    move_origin_center(line0)
    copy_location(line0, proje)
    copy_rotation(line0, proje)
 
    # This line is normal to BC and parallel to its Y axis. So we need to change 
    # this to X because by convention we assume that all line are parallel to
    # their local X axis. We do this by creating a new line. 

    point0 = new_empty(hide=hide_extra)
    position_on_curve(point0, line0, position=1, influence=1)

    move_origin_center(perp_line)
    copy_location(perp_line, proje)
    copy_rotation(perp_line, A)
    locked_track(perp_line, lock='Z', axis='X', target=point0)
    



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


def perpendicular_bisector_of_2points(line, A, B, hide_extra = True):
    '''
    Given two points A, B on a 2D plane, construct the 2D perpendicular 
    bisector.
    '''

    mid_point = new_empty(hide=hide_extra)
    put_in_between(mid_point, A, B, influence=0.5)
    copy_rotation(mid_point, A)

    seg = new_line(hide=hide_extra)
    segment(seg, A, B)

    orthogonal_line(line, mid_point, seg)


def perpendicular_bisector_of_line(perp, line,  hide_extra = True):
    '''
    Given a line on a 2D plane, construct the 2D perpendicular 
    bisector (line).
    '''

    B = new_empty(hide=hide_extra)
    position_on_curve(B, line, 0)

    C = new_empty(hide=hide_extra)
    position_on_curve(C, line, 1)

    mid_point=new_empty(hide=hide_extra)
    copy_rotation(mid_point, line)
    put_in_between(mid_point, B, C, influence=0.5)

    orthogonal_line(perp, mid_point, line) #midpoing and line have same Z


    


def reflection_across_line(point, line, A, hide_extra = True):
    '''Places a point to the relection of another point A relative
    to a given line (line). A should be active.
    '''
    proje = new_empty(hide=hide_extra)
    orthogonal_projection(proje, A, line)

    add_driver(
        obj=point,
        prop='location',
        fields='XYZ',
        vars_def={
            'o1': ('transform', A, 'location', '-'),
            'o2': ('transform', proje, 'location', '-'),
        },
        expr='gb_reflect(o1, o2)'
    )
    copy_rotation(point, A)



