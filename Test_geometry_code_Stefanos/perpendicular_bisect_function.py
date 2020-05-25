def perpendicular_bisect(obj, A, B, hide_extra=True):
    '''
    Align the obj (most common a plane) to the perpendicular bisector of the segment AB. The Z axis of
    the returned obj is parallel to AB. The X, Y axis are not determined. 
    
    A, B:       2 points        (Blender Objects; circle curves)
    
    '''

    put_in_between(obj, A, B)
    damped_track(plane, axis='Z', target=A)
    plane.name = "Perp. Bisector Plane"