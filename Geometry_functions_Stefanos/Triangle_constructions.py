
##############################################################################
# Median, barycenter of triangle

def median(line, point, A, B, C, hide_extra=True):
    '''
    Constructs the median (line) and the midpoint (point) of the 
    triangle ABC from A. A is the active point.
    '''
    put_in_between(point, B, C, influence=0.5)
    segment(line, A, point)


def barycenter(point, A, B, C, hide_extra=True):
    '''
    Constructs the barycenter of the triangle ABC. A is the active point.
    '''
    median1 = new_line(hide=hide_extra)
    mid1 = new_empty(hide=hide_extra)
  
    median2 = new_line(hide=hide_extra)
    mid2 = new_empty(hide=hide_extra)

    median(median1, mid1, A, B, C)
    median(median2, mid2, A, B, C)
    line_line_inteserction(point, median1, median2)
    copy_rotation(point, A) # To make sure point has the correct Z axis




##############################################################################
# Altitude, orthocenter of triangle

def altitude(line, point, A, B, C, hide_extra=True):
    '''
    Constructs the altitude (line) and its foot (point) of the 
    triangle ABC from A. A is the active point.
    '''
    side_bc = new_line(hide=hide_extra)
    segment(side_bc, B, C)
    orthogonal_projection(point, A, side_bc)   
    segment(line, A, point)


def orthocenter(point, A, B, C, hide_extra=True):
    '''
    Constructs the barycenter of the triangle ABC. A is the active point.
    '''
    altitude1 = new_line(hide=hide_extra)
    foot1 = new_empty(hide=hide_extra)
  
    altitude2 = new_line(hide=hide_extra)
    foot2 = new_empty(hide=hide_extra)

    altitude(altitude1, foot1, A, B, C)
    altitude(altitude2, foot2, A, B, C)
    line_line_inteserction(point, altitude1, altitude2)
    copy_rotation(point, A) # To make sure point has the correct Z axis



##############################################################################
# Circumcenter, circumcircle of triangle

def circumcenter(point, A, B, C, hide_extra=True):
    '''
    Constructs the circumcenter of the triangle ABC. It has the same 
    orientation as A.  
    '''
    perp1 = new_line(hide=hide_extra)
    perpendicular_bisector_of_2points(perp1, A, B)
  
    perp2 = new_line(hide=hide_extra)
    perpendicular_bisector_of_2points(perp2, A, C)

    line_line_inteserction(point, perp1, perp2)
    copy_rotation(point, A) # To make sure point has the correct Z axis


def circumcircle(circle, A, B, C, hide_extra=True):
    '''
    Constructs the circumcenter of the triangle ABC. It has the same 
    orientation as A. 
    '''
    center_point = new_empty(hide=hide_extra)
    circumcenter(center_point, A, B, C)
    circle_center_radius_distance(circle, center_point, center_point, A)




##############################################################################
# Euler center, Euler line, Euler circle

def euler_center(point, A, B, C, hide_extra=True):
    '''
    Constructs the Euler center (point) of the triangle ABC. It is 
    returned with the same orientation as the point A.
    '''
    circcum = new_empty(hide=hide_extra)
    circumcenter(circum, A, B, C)

    ortho = new_empty(hide=hide_extra)
    orthocenter(ortho, A, B, C)

    put_in_between(point, circum, ortho, influence=0.5)
    copy_rotation(point, A) # To make sure point has the correct Z axis


def euler_line(line, A, B, C, hide_extra=True):
    '''
    Constructs the Euler line (line) of the triangle ABC.
    '''

    circcum = new_empty(hide=hide_extra)
    circumcenter(circum, A, B, C)

    ortho = new_empty(hide=hide_extra)
    orthocenter(ortho, A, B, C)

    full_line(line, circum, ortho)


def euler_circle(circle, A, B, C, hide_extra=True):
    '''
    Constructs the Euler circle (circle) of the triangle ABC.
    It has the same orientation as A.
    '''
        
    center_point = new_empty(hide=hide_extra)
    euler_center(center_point, A, B, C)

    mid_point = new_empty(hide=hide_extra)
    put_in_between(mid_point, B, C, influence=0.5)

    circle_center_radius_distance(circle, center_point, center_point, mid_point)




##############################################################################
# Angle bisectors (internal and external), 
# incenter, inscribed circle, exscribed circle

def angle_bisector(bisector, B, C, A, hide_extra=True):
    '''
    Constructs the angle bisector of the angle BAC, A is the active point.
    '''

    pr_plane = new_plane(hide=hide_extra)
    make_orthogonal_to(pr_plane, B, C, A, axis='Z')

        bisector_point = new_empty(hide=hide_extra)
        copy_location(bisector_point, A)
        track_to_angle_between(bisector_point, B, C)
        project_along_axis(
            bisector_point,
            axis='X',
            target=pr_plane,
            opposite=True
        )

        line = new_line()
        stretch_between_points(line, A, bisector_point, axis='Z')

def angle_bisector_foot(bisector_foot, B, C, A, hide_extra=True):
    
    '''
    Constructs the angle bisector foot on BC
    of the angle BAC, A is the active point.
    '''

    pr_plane = new_plane(hide=hide_extra)
    make_orthogonal_to(pr_plane, B, C, A, axis='Z')

    bisector_point = new_empty()
    copy_location(bisector_point, A)
    track_to_angle_between(bisector_point, B, C)
    project_along_axis(
        bisector_foot,
        axis='X',
        target=pr_plane,
        opposite=True
        )

def external_bisector(external, B, C, A, hide_extra= True):
    
    '''
    Constructs the external angle bisector of the angle BAC,
    A is the active point.
    '''
    internal = new_line(hide=hide_extra)
    angle_bisector(internal, B, C, A, hide_extra=True)

    orthogonal_line(external, A, internal, hide_extra=True)


def incenter(point, A, B, C, hide_extra=True):
    '''
    Constructs the incenter of the triangle ABC. It has the 
    same orientation as A.
    '''
    bis1 = new_line(hide=hide_extra)
    angle_bisector(bis1, B, C, A)
  
    bis2 = new_line(hide=hide_extra)
    angle_bisector(bis2, B, A, C)

    line_line_inteserction(point, bis1, bis2)
    copy_rotation(point, A) # To make sure point has the correct Z axis


def incircle(circle, A, B, C, hide_extra=True):
    '''
    Constructs the incircle of the triangle ABC. It has the same orientation
    as A.  
    '''
    center_point = new_empty(hide=hide_extra)
    incenter(center_point, A, B, C)

    side_bc = new_line(hide=hide_extra)
    segment(side_bc, B, C)

    proje_point = new_empty(hide=hide_extra)
    orthogonal_projection(proje_point, center_point, side_bc)
    circle_center_radius_distance(circle, center_point, center_point, proje_point)


def excenter(point, A, B, C, hide_extra=True):
    '''
    Constructs the excenter of the triangle ABC opposite to A. It has the 
    same orientation as A. A must be the active point.
    '''
    bis1 = new_line(hide=hide_extra)
    external_bisector(bis1, C, A, B)
  
    bis2 = new_line(hide=hide_extra)
    external_bisector(bis2, B, A, C)

    line_line_inteserction(point, bis1, bis2)
    copy_rotation(point, A) # To make sure point has the correct Z axis


def excircle(circle, A, B, C, hide_extra=True):
    '''
    Constructs the excircle of the triangle ABC opposite to A. It has the same orientation
    as A.  
    '''
    center_point = new_empty(hide=hide_extra)
    excenter(center_point, A, B, C)

    side_bc = new_line(hide=hide_extra)
    segment(side_bc, B, C)

    proje_point = new_empty(hide=hide_extra)
    orthogonal_projection(proje_point, center_point, side_bc)
    circle_center_radius_distance(circle, center_point, center_point, proje_point)
