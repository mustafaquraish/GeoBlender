import bpy

def new_plane(context, size=10, location=(0,0,0)):
    bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', location=location)
    ret = context.object
    return ret

def new_empty(context, location=(0,0,0)):
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
    ret = context.object
    return rets