'''
Copyright (C) 2020 Mustafa Quraish
mustafa@cs.toronto.edu

Created by Mustafa Quraish

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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

    TODO: Move the objects to another collection.
    '''
    obj.hide_viewport = hide
    obj.hide_render = hide

###############################################################################

@preserve_selection
def new_plane(size=10, location=(0,0,0), hide=False):
    bpy.ops.mesh.primitive_plane_add(
        size=size, 
        enter_editmode=False, 
        align='WORLD', 
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

@preserve_selection
def new_empty(location=(0,0,0), hide=False):
    bpy.ops.object.empty_add(
        type='PLAIN_AXES', 
        align='WORLD', 
        location=location
    )
    set_hidden(bpy.context.object, hide)
    return bpy.context.object

@preserve_selection
def new_circle(radius=1, location=(0,0,0), hide=False):
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
