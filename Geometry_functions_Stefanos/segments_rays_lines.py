def segment(line, A, B):
    '''
    This function returns line to the segment defined by 
    the points A, B.
    '''
    stretch_between_points(line, A, B, axis='Z')


def ray(line, A, B):
    '''
    This function returns line to the ray defined by 
    the point A to the point B (B active).
    '''
    stretch_between_points(line, A, B, axis='Z')
    line.scale.z = 10e4 #make sure that line has its origin at A with pos=0


def full_line(line, A, B):
    '''
    This function returns line to the full line defined by 
    the point A to the point B (B active).
    '''
    stretch_between_points(line, A, B, axis='Z')
    move_origin_center(line, center='MEDIAN')
    line.scale.z = 10e4 