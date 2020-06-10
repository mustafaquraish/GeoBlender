import bpy
from .drivers import add_driver


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
        bpy.ops.object.select_all(action='DESELECT')
        for obj in prev_selected:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = prev_active

        return ret

    # Return the wrapped function
    return new_func


def shade_smooth_option(func):

    def new_func(*args, **kwargs):

        # Call the original functions
        ret = func(*args, **kwargs)

        # Shade smooth
        if bpy.context.scene.geoblender_settings.shade_smooth:
            bpy.ops.object.shade_smooth()

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

    old_collections = obj.users_collection  # get old collection
    collection.objects.link(obj)    # put obj in extras collection
    for coll in old_collections:
        coll.objects.unlink(obj)    # unlink from old collection

    obj.hide_viewport = hide
    obj.hide_render = hide


@preserve_selection
def move_origin_center(obj, center='BOUNDS'):
    # Object needs to be visible to do this, temporarily make it visible
    prev_hidden = obj.hide_viewport
    obj.hide_viewport = False

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center=center)

    obj.hide_viewport = prev_hidden

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


@preserve_selection
def duplicate(obj, hide=False):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def duplicate_to_mesh(obj, hide=False):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.duplicate()
    bpy.ops.object.convert(target='MESH')
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def convert_to_mesh(obj, hide=False):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


def add_abs_bevel(obj, bevel_depth):
    from bpy.types import Curve
    if not isinstance(obj.data, Curve):
        return
    add_driver(
        obj=obj.data,
        prop='bevel_depth',
        vars_def={
            'sx': ('transform', obj, 'scale', 'X'),
            'sy': ('transform', obj, 'scale', 'Y'),
            'sz': ('transform', obj, 'scale', 'Z'),
        },
        expr=f'{bevel_depth} / max(sx, sy, sz)'
    )


def uniform_scale(obj, scale):
    for i in range(3):
        obj.scale[i] = scale


@preserve_selection
def set_parent(obj, here_parent):
    '''
    Using parenting without inverse.

    ---------------------------------------------------------------------------
    ------------------------------ DEPRECATED CODE ----------------------------
    ---------------------------------------------------------------------------

        Just do `obj.parent = here_parent` in the calling function instead.

    '''
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    parent_here.select_set(True)
    bpy.context.view_layer.objects.active = parent_here
    bpy.ops.object.parent_no_inverse_set()

# ----------------------------------------------------------------------------


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
    bpy.context.object.data.resolution_u = 64
    bpy.context.object.data.bevel_resolution = 32
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_arc(radius=1, location=(0, 0, 0), angle=180, sides=40, hide=False):
    bpy.ops.curve.simple(
        align='WORLD',
        location=location,
        rotation=(0, 0, 0),
        Simple_Type='Arc',
        Simple_endangle=angle,
        Simple_sides=sides,
        Simple_radius=radius,
        use_cyclic_u=False,
        shape='3D',
        edit_mode=False
    )
    bpy.context.object.data.resolution_u = 64
    bpy.context.object.data.bevel_resolution = 32
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_right_angle(length=2, location=(0, 0, 0), hide=False):
    bpy.ops.curve.simple(
        align='WORLD',
        location=location,
        rotation=(0, 0, 0),
        Simple_Type='Angle',
        Simple_angle=90,
        Simple_length=length,
        use_cyclic_u=False,
        shape='2D',
        edit_mode=False
    )
    bpy.context.object.data.fill_mode = 'NONE'
    bpy.context.object.data.resolution_u = 64
    bpy.context.object.data.bevel_resolution = 32
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_mesh_circle(radius=1, vert=100, location=(0, 0, 0), hide=False):
    bpy.ops.mesh.primitive_circle_add(
        radius=radius,
        vertices=vert,
        fill_type='NGON',
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_line(length=1, axis='X', hide=False):
    '''
    It is highly recommended that this function only be called with axis='X'
    for the sake of consistency with the rest of the addon.
    '''
    end_loc = (
        length if axis == 'X' else 0,
        length if axis == 'Y' else 0,
        length if axis == 'Z' else 0
    )

    bpy.ops.curve.simple(
        align='WORLD',
        location=(0, 0, 0),
        rotation=(0, 0, 0),
        Simple_Type='Line',
        Simple_endlocation=end_loc,
        shape='3D',
        use_cyclic_u=False,
        edit_mode=False
    )
    bpy.context.object.data.resolution_u = 64
    bpy.context.object.data.bevel_resolution = 32
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


@preserve_selection
def new_cylinder(radius=1, depth=1, vert=256, location=(0, 0, 0), hide=False):
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
@shade_smooth_option
def new_cone(vertices=32, radius1=1, radius2=0, depth=2, hide=False):
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices,
        radius1=radius1,
        radius2=radius2,
        depth=depth,
        enter_editmode=False,
        align='WORLD'
        )
    set_hidden(bpy.context.object, hide)
    bpy.context.object.rotation_euler[1] = 1.5708
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    bpy.context.object.data.use_auto_smooth = True
    bpy.context.object.location[0] = - depth/2
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
  

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
@shade_smooth_option
def new_sphere(radius=1, segments=32, location=(0, 0, 0), hide=False):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments,
        ring_count=segments // 2,
        radius=radius,
        enter_editmode=False,
        align='WORLD',
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object


# ----------------------------------------------------------------------------

def new_point(use_spheres=None, radius=None, segments=None, hide=False):
    '''
    Specific to the GeoBlender addon. We want to be able to make points as
    spheres or empties based on the global settings.
    '''
    # Check the global settings to see if we're making a sphere
    if use_spheres is None:
        use_spheres = bpy.context.scene.geoblender_settings.use_spheres

    if use_spheres:
        # Get the sphere properties from the global settings
        if radius is None:
            radius = bpy.context.scene.geoblender_settings.sphere_radius
        if segments is None:
            segments = bpy.context.scene.geoblender_settings.sphere_subdivisions
        point = new_sphere(
            radius=radius,
            segments=segments,
            hide=hide,
        )

    else:
        point = new_empty(hide=hide)

    return point
