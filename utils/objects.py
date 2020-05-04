import bpy

def set_hidden(obj, hide=True):
    obj.hide_viewport = hide
    obj.hide_render = hide

def new_plane(size=10, location=(0,0,0), hide=False):
    bpy.ops.mesh.primitive_plane_add(
        size=size, 
        enter_editmode=False, 
        align='WORLD', 
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

def new_empty(location=(0,0,0), hide=False):
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

def new_circle(radius=1, location=(0,0,0), hide=False):
    bpy.ops.curve.primitive_bezier_circle_add(
        radius=radius, 
        enter_editmode=False, 
        align='WORLD', 
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

def new_line(length=1, hide=False):
    bpy.ops.curve.simple(
        align='WORLD', 
        location=(0, 0, 0), 
        rotation=(0, 0, 0), 
        Simple_Type='Line', 
        Simple_endlocation=(0, 0, length), 
        shape='3D', 
        use_cyclic_u=False, 
        edit_mode=False
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

def cylinder_origin_to_bottom(obj, depth=1):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.transform.translate(
        value=(0, 0, depth/2), 
        orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL', 
        constraint_axis=(False, False, True), 
        mirror=True, 
        use_proportional_edit=False, 
        proportional_edit_falloff='SMOOTH', 
        proportional_size=1, 
        use_proportional_connected=False, 
        use_proportional_projected=False
    )
    bpy.ops.object.editmode_toggle()


def new_cylinder(radius=1, depth=1, vertices=20, location=(0,0,0), hide=False):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, 
        radius=radius, 
        depth=depth, 
        enter_editmode=False, 
        align='WORLD', 
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object
