import bpy


def preserve_selection(func):
    '''
    A wrapper for functions that preserves the previous selection in the
    Blender context. Use as follows:

    >   @preserve_selection
        def original_function(...):
            ...

    func:   The original function
    '''

    # Define the wrapped function:
    def new_func(*args, **kwargs):
        # Store selections
        prev_selected = bpy.context.selected_objects
        prev_active = bpy.context.object

        # Call the original functions
        ret = func(*args, **kwargs)

        # Restore the selection
        if ret is not None:
            ret.select_set(False)
        for obj in prev_selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = prev_active

        return ret

    # Return the wrapped function
    return new_func


def set_hidden(obj, hide=True):
    '''
    Simple function to hide / unhide objects from the viewport and render.
    If the object is supposed to be hidden, it is moved to a new collection
    with the name defined in COLLECTION_NAME.
    '''
    # Don't need to bother with collections
    if not hide:
        return

    COLLECTION_NAME = bpy.context.scene.geoblender_settings.collection_name

    # Make a new collection for extra objects if needed.
    if COLLECTION_NAME not in bpy.data.collections:
        collection = bpy.data.collections.new(COLLECTION_NAME)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[COLLECTION_NAME]

    old_collection = obj.users_collection[0]  # get old collection
    collection.objects.link(obj)        # put obj in extras collection
    old_collection.objects.unlink(obj)  # unlink from old collection

    obj.hide_viewport = hide
    obj.hide_render = hide


@preserve_selection
def move_origin_center(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    return obj


@preserve_selection
def join_objects(obj_list):
    if len(obj_list) == 0:
        return None

    bpy.ops.object.select_all(action='DESELECT')
    c = {}  # Temporary context for joining objects
    c["object"] = c["active_object"] = obj_list[0]
    c["selected_objects"] = c["selected_editable_objects"] = obj_list
    bpy.ops.object.join(c)
    return obj_list[0]


###############################################################################


@preserve_selection
def new_plane(size=None, location=(0, 0, 0), hide=False):
    if size is None:
        size = bpy.context.scene.geoblender_settings.plane_size

    bpy.ops.mesh.primitive_plane_add(
        size=size,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_empty(location=(0, 0, 0), hide=False):
    bpy.ops.object.empty_add(
        type='PLAIN_AXES',
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_circle(radius=1, location=(0, 0, 0), hide=False):
    bpy.ops.curve.primitive_bezier_circle_add(
        radius=radius,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
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


@preserve_selection
def new_cylinder(radius=1, depth=1, vert=20, location=(0, 0, 0), hide=False):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vert,
        radius=radius,
        depth=depth,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_icosphere(radius=1.0, subdivisions=2, location=(0, 0, 0), hide=False):
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=radius,
        subdivisions=subdivisions,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_sphere(radius=1, segments=32, rings=16, location=(0, 0, 0), hide=False):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=rings,
        radius=radius,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object
