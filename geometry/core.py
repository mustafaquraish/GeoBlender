from ..utils import constraints
from ..utils import geometry
from ..utils import drivers
from ..utils import objects


def put_in_between(obj, A, B, influence=0.5):
    '''
    Positions an object on the line between two other objects, such that
                (distance to A)/(distance to B) = influence

    obj:        Source object   (Blender Object)
    A, B:       2 points        (Blender Objects)
    influence:  Influence       (float, 0-1)
    '''

    # Note that location of B is copied first to make influence consistent
    constraints.copy_location(obj, target=B)
    constraints.copy_location(obj, target=A, influence=influence)


def track_to_angle_between(obj, A, B, axes='XYZ', influence=0.5):
    '''
    Make the given axis of the object point towards the bisector (or other
    intermediary angle) of the angle formed by the lines from the object
    to A and B.

    obj:        Source object   (Blender Object)
    A, B:       2 Objects       (Blender Objects)
    axes:       Axes (in order) ('XYZ', 'XZY', 'YZX', ...)
    influence   Influence       (float, 0-1)
    '''
    constraints.damped_track(obj, axis=axes[0].upper(), target=A)
    constraints.locked_track(
        obj=obj,
        axis=axes[1].upper(),
        lock=axes[0].upper(),
        target=B
    )
    constraints.locked_track(
        obj=obj,
        axis=axes[0].upper(),
        lock=axes[2].upper(),
        target=B,
        influence=influence
    )


def make_orthogonal_to(obj, A, B, C):
    '''
    Locates the object at A, aligns X axis with AB and Z axis to AC as much as
    possible.

    obj:        Source Object       (Blender object)
    A, B, C:    3 points            (Blender Objects)
    '''
    constraints.copy_location(obj, target=A)
    constraints.damped_track(obj, axis='X', target=B)
    constraints.locked_track(obj, axis='Z', lock='X', target=C)


