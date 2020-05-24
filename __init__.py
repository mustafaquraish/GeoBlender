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
import addon_utils
from bpy.app.handlers import persistent

from .operators import operator_list
from .interface import panel_list
from .properties import GeoBlenderSettings
from .properties import GeoBlenderMeasurements

# -----------------------------------------------------------------------------

bl_info = {
    "name": "GeoBlender",
    "description": "A 3D Geometry addon for Blender",
    "author": "Mustafa Quraish",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View Sidebar > GeoBlender tab",
    "wiki_url": "https://github.com/mustafaquraish/GeoBlender",
    "tracker_url": "https://github.com/mustafaquraish/GeoBlender",
    "category": "Geometry"
}

# -----------------------------------------------------------------------------

# Enable the Extra Objects: Curves addon
(installed, enabled) = addon_utils.check("add_curve_extra_objects")
if installed and (not enabled):
    addon_utils.enable("add_curve_extra_objects")

# -----------------------------------------------------------------------------


@persistent
def load_post_handler(dummy):
    '''
    This function is meant to be called after a file is loaded. Use this to
    add functions to the driver namespace, since they are not persistent by
    default.
    '''
    from types import FunctionType
    from .utils import driver_helpers as d_h

    # Extract all the elements of the module that are functions and have names
    # beginning with 'gb_'.
    custom_funcs = [getattr(d_h, name)
                    for name in dir(d_h)
                    if isinstance(getattr(d_h, name), FunctionType)
                    if name.startswith("gb_")]

    for func in custom_funcs:
        bpy.app.driver_namespace[func.__name__] = func
        print(f"*** Added {func.__name__} to driver namespace")

# -----------------------------------------------------------------------------


classes = [
    GeoBlenderSettings,
    GeoBlenderMeasurements,
] + operator_list + panel_list


def register():
    for cl in classes:
        bpy.utils.register_class(cl)

    load_post_handler(None)
    bpy.app.handlers.load_post.append(load_post_handler)

    # Add GeoBlender properties to the Scene
    geo_props = bpy.props.PointerProperty(type=GeoBlenderSettings)
    geo_measures = bpy.props.PointerProperty(type=GeoBlenderMeasurements)
    bpy.types.Scene.geoblender_settings = geo_props
    bpy.types.Scene.geoblender_measurements = geo_measures


def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)

    bpy.app.handlers.load_post.remove(load_post_handler)
