def circle_from_diameter(obj, A, B, hide_extra=True):
    '''
    Finds the circle with diameter AB. It first puts an empty O at the midpoint of AB and 
    then draws the circle with center O and radius equal to half AB. 

    A, B:       2 POINTS        (Blender Objects; circle curves)

    Note: This method creates additional objects that are needed to help find
          the intersections. These are hidden by default
    '''
    #place a hidden empty at the midpoint of AB
    mid_point = new_empty(hide=hide_extra)
    put_in_between(mid_point, A, B, 0.5)

    #place the circle obj with center at the midpoint

    copy_location(obj, target=mid_point)
    
    #add_driver(obj, scale, 'XYZ', vars_def={'d': ('distance', A, B)}, expr="0.5*d"):
    
    add_driver_distance(obj, scale, 'XYZ', A, B, 0.5)

    