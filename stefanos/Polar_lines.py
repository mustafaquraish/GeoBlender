def put_at_polar_intersection(obj, A, circle):
    '''
    Place the given object at the  intersection point of the polar axis
    of a point A relative to a circle.

    obj:        Source object   (Blender Object)
    A:          Point           (Blender Objects)
    circle:     Circle          (Blender Objects)
    '''
    add_driver(
        obj=obj,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('distance', A, B),
            'r': ('transform', circle, 'scale', 'X'),
            'o1': ('transform', circle, 'location', '-'),
            'o2': ('transform', A, 'location', '-'),
        },
        expr='gb_polar_intersection(d, r, o1, o2)'
    )


def polar_line(line, circle, A, hide_extra=True):
    '''
    This function places a line to be the polar of the point A (active)
    relative to the circle and returns it as the line argument.
    '''
    foot_polar = new_empty(hide=hide_extra)
    put_at_polar_intersection(foot_polar, A, circle)

    # We next construct the line connecting the point and the center
    connecting_line = new_line(hide=hide_extra)
    segment(connecting_line, circle, A)

    # Finally we place line to the polar line
    orthogonal_line(line, foot_polar, connecting line)
