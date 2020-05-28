def parallel_line(A, line, length, hide_extra=True):
    '''
    This function creates a line of length through a point A and
    parallel to a line.
    '''

    line_start = new_empty(hide=hide_extra)
    position_on_curve(line_start, line, 0)

    line_end = new_empty(hide=hide_extra)
    position_on_curve(line_end, line, 1)

    proj_a = new_empty(hide=hide_extra)
    orthogonal_projection(proj_a, A, line, hide_extra=True)

    perp_line = new_line(hide=hide_extra)
    stretch_between_points(perp_line, A, proj_a, axis='Z')

    orthogonal_line(A, perp_line, length)
