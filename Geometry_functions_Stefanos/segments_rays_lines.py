def segment(line, A, B):
    '''
    This function returns line to the segment defined by
    the points A, B.
    '''
    stretch_between_points(line, A, B, axis='Z')


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
    copy_location(line, target=A)
    damped_track(line, axis=Z, target=B)
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
    copy_location(line, target=A)
    damped_track(line, axis=Z, target=B)
    add_driver(line, 'scale', fields='XYZ', vars_def={}, expr="1000")
