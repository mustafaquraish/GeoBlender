from ..utils import objects
from ..utils import constraints
from ..utils import geometry
from ..utils import drivers


def make_segment(line, A, B, axis='X'):
    '''
    This function creates the line to the segment defined by the points A, B.

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    axis:       Axis to align   ('X', 'Y')
    '''
    constraints.copy_location(line, A)
    constraints.copy_rotation(line, A)
    constraints.locked_track(
        obj=line,
        lock='Z',
        axis='X',
        target=B
    )
    drivers.add_driver_distance(
        obj=line,
        prop='scale',
        fields='XYZ',
        A=A,
        B=B
    )


def make_ray(line, A, B, length=100, axis='X'):
    '''
    Forms a ray starting at the point A, towards the point B with the given
    length

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    axis:       Axis to align   ('X', 'Y')
    '''
    constraints.copy_location(line, A)
    constraints.copy_rotation(line, A)
    constraints.locked_track(
        obj=line,
        lock='Z',
        axis='X',
        target=B
    )
    objects.uniform_scale(line, length)



def make_line(line, A, B, length=100):
    '''
    Places a full line through the points A, B. her. Effectively, move center 
    at the middle point of the line, copy location of A, align to B and stretch
    the given axis a desired amount (scale).

    obj:        Source object   (Blender Object)
    axis:       Axis to align   ('X', 'Y' or 'Z')
    A, B:       2 points        (Blender Objects)
    scale:      stretch scale   (float)
    '''
    objects.move_origin_center(line)
    constraints.copy_location(line, A)
    constraints.copy_rotation(line, A)
    constraints.locked_track(
        obj=line,
        lock='Z',
        axis='X',
        target=B
    )
    objects.uniform_scale(line, length)


def put_at_line_ends(A, B, line):
    '''
    Places the two input objects A and B at the two extreme ends of the line.

    A, B:       2 points        (Blender Objects)
    line:       The line        (Blender Object; Curve; Line)
    '''
    # Position on curve
    constraints.position_on_curve(A, line, position=0)
    constraints.position_on_curve(B, line, position=1)
    
    # Make sure that the points' Z axis is aligned with that of the line
    constraints.copy_rotation(A, line)
    constraints.copy_rotation(B, line)