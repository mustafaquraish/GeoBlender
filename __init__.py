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

from .operators import operator_list
from .interface import panel_list
from .properties import GeoBlenderSettings

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

# Enable the Extra Objects: Curves addon
(installed, enabled) = addon_utils.check("add_curve_extra_objects")
if installed and (not enabled):
    addon_utils.enable("add_curve_extra_objects")


def register():
    # Register Panels and Operators
    for cl in panel_list + operator_list:
        bpy.utils.register_class(cl)
    # Register GeoBlender properties to the Scene
    bpy.utils.register_class(GeoBlenderSettings)
    pointer_prop = bpy.props.PointerProperty(type=GeoBlenderSettings)
    bpy.types.Scene.geoblender_settings = pointer_prop


def unregister():
    # Unregister Panels and Operators
    for cl in panel_list + operator_list:
        bpy.utils.unregister_class(cl)
    # Unregister Properties
    bpy.utils.unregister_class(GeoBlenderSettings)
