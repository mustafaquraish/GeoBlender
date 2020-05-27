def circle_from_diameter(circle, A, B, hide_extra=True):
    
    '''
    Finds the circle with diameter AB. It first puts an empty O at the midpoint
    of AB and  then draws the circle with center O and radius equal to half AB. 
    The circle has the same orientation as A.

    A, B:       2 POINTS        (Blender Objects; circle curves)
    '''
   
    # Place the circle obj with center at the midpoint
    copy_rotation(circle, A)
    put_in_between(circle, A, B, 0.5)
    add_driver_distance(circle, scale, 'XYZ', A, B, 0.5)


def circle_center_point(circle, center, point,  hide_extra=True):

    '''
    Finds the circle with given center and passes through a given point. 
    It is a  2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center, point:       2 POINTS        (Blender Objects)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)
    # damped_track(circle, axis='X', target=B) 
    # Non needed for 2D constructions, because Z axis of center gives
    # the plane.

    add_driver_distance(circle, 'scale', 'XYZ', center, point)


def circle_center_radius_distance(circle, center, A, B, hide_extra=True):
    '''
    Place the circle at given center with given radius AB. It is a 
    2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center, A, B:       3 POINTS        (Blender Objects)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)
    
    add_driver_distance(circle, 'scale', 'XYZ', A, B)

def circle_center_radius_number(circle, center, number, hide_extra=True):
    '''
    Place the circle at given center with given radius number. It is a 
    2D construction. The circle has the orientation of the center.
    The center must be the active object.

    center       1 POINTS        (Blender Objects)
    number        radius         (float)
    '''
    copy_location(circle, center)
    copy_rotation(circle, center)
    
    add_driver(circle, 'scale', 'XYZ', vars_def={}, expr="number")

 