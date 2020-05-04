import bpy

def copy_location(obj, target, influence=1.0):
    '''
    Makes object copy the location of another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='COPY_LOCATION')
    obj.constraints["Copy Location"].target = target
    obj.constraints["Copy Location"].influence = influence

def locked_track(obj, lock, track, target, influence=1):
    '''
    Tracks one object to another with an axis locked.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    lock:       Locked Axis     ('X', 'Y' or 'Z')
    track:      tracked Axis    ('X', 'Y' or 'Z')
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='LOCKED_TRACK')
    obj.constraints["Locked Track"].lock_axis = 'LOCK_' + lock.upper()
    obj.constraints["Locked Track"].track_axis = 'TRACK_' + track.upper()
    obj.constraints["Locked Track"].target = target
    obj.constraints["Locked Track"].influence = influence

def damped_track(obj, track, target, influence=1):
    '''
    Damped-tracks one object to another.

    obj:        Source object   (Blender Object)
    target:     Target object   (Blender Object)
    track:      tracked Axis    ('X', 'Y' or 'Z')
    influence:  Influence       (float, 0-1)
    '''
    obj.constraints.new(type='DAMPED_TRACK')
    obj.constraints["Damped Track"].track_axis = 'TRACK_' + track.upper()
    obj.constraints["Damped Track"].target = target
    obj.constraints["Damped Track"].influence = influence