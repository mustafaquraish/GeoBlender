def parallel_line(parallel_line, A, line, hide_extra=True):

    '''
    This function places a line (parallel_line) to go through a point A and
    be parallel to a line.
    '''
    move_origin_center(parallel_line, center='MEDIAN')
    copy_location(parallel_line, A)
    copy_rotation(parallel_line, line)

