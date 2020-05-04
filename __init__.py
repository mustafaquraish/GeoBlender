'''
Copyright (C) 2020 Mustafa Quraish
mustafa@cs.toronto.edu

Created by Mustafa Quraish

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

bl_info = {
    "name": "GeoBlender",
    "description": "A Geometry addon for Blender",
    "author": "Mustafa Quraish",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/mustafaquraish",
    "tracker_url": "https://github.com/mustafaquraish",
    "category": "Geometry"
}

import bpy

from .operators.points_plane import PointsPlane

classes = [PointsPlane]

register, unregister = bpy.utils.register_classes_factory(classes)

# def register():
#     print(".................LOADING ADDON")
#     bpy.utils.register_module(__name__)

# def unregister():
#     bpy.utils.unregister_module(__name__)
