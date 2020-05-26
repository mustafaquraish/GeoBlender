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

