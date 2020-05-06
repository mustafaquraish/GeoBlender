'''
Utilites to add constraints to objects.
'''


def copy_location(obj, target, axes='XYZ', influence=1.0):
    '''
    Makes object copy the location of another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='COPY_LOCATION')
    obj.constraints[-1].target = target
    obj.constraints[-1].use_x = ('X' in axes.upper())
    obj.constraints[-1].use_y = ('Y' in axes.upper())
    obj.constraints[-1].use_z = ('Z' in axes.upper())
    obj.constraints[-1].influence = influence


def copy_rotation(obj, target, axes='XYZ', influence=1.0):
    '''
    Makes object copy the rotation of another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='COPY_ROTATION')
    obj.constraints[-1].target = target
    obj.constraints[-1].use_x = ('X' in axes.upper())
    obj.constraints[-1].use_y = ('Y' in axes.upper())
    obj.constraints[-1].use_z = ('Z' in axes.upper())
    obj.constraints[-1].influence = influence


def copy_scale(obj, target, axes='XYZ', influence=1.0):
    '''
    Makes object copy the scale of another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='COPY_SCALE')
    obj.constraints[-1].target = target
    obj.constraints[-1].use_x = ('X' in axes.upper())
    obj.constraints[-1].use_y = ('Y' in axes.upper())
    obj.constraints[-1].use_z = ('Z' in axes.upper())
    obj.constraints[-1].influence = influence


def copy_transforms(obj, target, transforms='LRS', mix='REPLACE', influence=1):
    '''
    Makes object copy the transformations of another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    influence:  Influence       (float, 0-1)
    '''
    # If all the transformations don't want to be copied, apply the needed
    # constraints individually
    if transforms != "LRS":
        dic = {'L': copy_location, 'S': copy_scale, 'R': copy_rotation}
        for t in transforms:
            dic[t.upper()](obj=obj, target=target, influence=influence)
    else:
        obj.constraints.new(type='COPY_TRANSFORMS')
        obj.constraints[-1].target = target
        obj.constraints[-1].mix_mode = mix
        obj.constraints[-1].influence = influence


def locked_track(obj, lock, axis, target, influence=1):
    '''
    Tracks one object to another with an axis locked.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    lock:       Locked Axis     ('X', 'Y' or 'Z')
    axis:       Tracked Axis    ('X', 'Y' or 'Z')
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='LOCKED_TRACK')
    obj.constraints[-1].lock_axis = 'LOCK_' + lock.upper()
    obj.constraints[-1].track_axis = 'TRACK_' + axis.upper()
    obj.constraints[-1].target = target
    obj.constraints[-1].influence = influence


def damped_track(obj, axis, target, influence=1):
    '''
    Damped-tracks one object to another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    axis:       Tracked Axis    ('+X', 'Y' or 'Z')
    influence:  Influence       (float, 0-1)
    '''
    track_axis = 'TRACK_'
    track_axis += ('NEGATIVE_' if axis[0] == '-' else '')
    track_axis += axis[-1].upper()

    obj.constraints.new(type='DAMPED_TRACK')
    obj.constraints[-1].track_axis = track_axis
    obj.constraints[-1].target = target
    obj.constraints[-1].influence = influence


def track_to(obj, axis, target, up='Z', target_z=False, influence=1):
    '''
    Damped-tracks one object to another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    axis:       Tracked Axis    ('X', 'Y' or 'Z')
    influence:  Influence       (float, 0-1)
    '''
    track_axis = 'TRACK_'
    track_axis += ('NEGATIVE_' if axis[0] == '-' else '')
    track_axis += axis[-1].upper()

    obj.constraints.new(type='TRACK_TO')
    obj.constraints[-1].track_axis = track_axis
    obj.constraints[-1].target = target
    obj.constraints[-1].use_target_z = target_z
    obj.constraints[-1].up_axis = 'UP_' + up.upper()
    obj.constraints[-1].influence = influence


def project_along_axis(obj, axis, target, opposite=False,
                       align_to_normal=None, influence=1):
    '''
    Projects one object to another along an axis.

    obj:                Source object           (Blender Object)
    axis:               Axis to project along   ('+X', '-X', '+Y', ...)
    target:             Target object           (Blender Object)
    opposite:           Project Opposite        (Boolean)
    align_to_normal     Align axis to normal    (None, or '+X', '-X', ...)
    influence:          Influence               (float, 0-1)
    '''
    project_axis = ''
    project_axis += ('NEG_' if axis[0] == '-' else 'POS_')
    project_axis += axis[-1].upper()

    obj.constraints.new(type='SHRINKWRAP')
    obj.constraints[-1].shrinkwrap_type = 'PROJECT'
    obj.constraints[-1].project_axis = project_axis
    obj.constraints[-1].target = target
    obj.constraints[-1].use_project_opposite = opposite
    obj.constraints[-1].influence = influence

    if align_to_normal is not None:
        obj.constraints[-1].influence = True
        align_axis = 'TRACK_'
        align_axis += ('NEGATIVE_' if align_to_normal[0] == '-' else '')
        align_axis += align_to_normal[-1].upper()
        obj.constraints[-1].use_track_normal = True
        obj.constraints[-1].track_axis = align_axis


def project_nearest(obj, target, align_to_normal=None, influence=1):
    '''
    Projects one object to another at the nearest surface point.

    obj:                Source object           (Blender Object)
    target:             Target object           (Blender Object)
    align_to_normal     Align axis to normal    (None, or '+X', '-X', ...)
    influence:          Influence               (float, 0-1)
    '''
    obj.constraints.new(type='SHRINKWRAP')
    obj.constraints[-1].shrinkwrap_type = 'NEAREST_SURFACE'
    obj.constraints[-1].target = target
    obj.constraints[-1].influence = influence

    if align_to_normal is not None:
        obj.constraints[-1].influence = True
        align_axis = 'TRACK_'
        align_axis += ('' if align_to_normal[0] == '+' else 'NEGATIVE_')
        align_axis += align_to_normal[1].upper()
        obj.constraints[-1].use_track_normal = True
        obj.constraints[-1].track_axis = align_axis


def follow_path(obj, target, follow=False, fixed=False, offset=0, influence=1):
    '''
    TODO: update this doc.

    Places an object along the given curve at the given position

    obj:                Source object           (Blender Object)
    target:             Target object           (Blender Object)
    align_to_normal     Align axis to normal    (None, or '+X', '-X', ...)
    influence:          Influence               (float, 0-1)
    '''
    obj.constraints.new(type='FOLLOW_PATH')
    obj.constraints[-1].use_curve_follow = follow
    obj.constraints[-1].use_fixed_location = fixed
    obj.constraints[-1].target = target
    obj.constraints[-1].offset_factor = offset


def position_on_curve(obj, target, position=0, influence=1):
    '''
    Places an object along the given curve at the given position

    obj:                Source object           (Blender Object)
    target:             Target object           (Blender Object)
    align_to_normal     Align axis to normal    (None, or '+X', '-X', ...)
    influence:          Influence               (float, 0-1)
    '''
    obj.constraints.new(type='FOLLOW_PATH')
    obj.constraints[-1].use_fixed_location = True
    obj.constraints[-1].target = target
    obj.constraints[-1].offset_factor = position
