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

from inspect import getmembers
from inspect import isclass
from sys import modules
import bpy

# Import operator classes
from .operators.create_inscribed_circle import CreateInscribedCircle
from .operators.create_circumcircle     import CreateCircumcircle
from .operators.create_line_segment     import CreateLineSegment
from .operators.create_triangle         import CreateTriangle
from .operators.create_line             import CreateLine

from .operators.empty_at_circumcenter   import EmptyAtCircumcenter
from .operators.empty_at_orthocenter    import EmptyAtOrthocenter
from .operators.empty_at_barycenter     import EmptyAtBarycenter
from .operators.empty_at_incenter       import EmptyAtIncenter
from .operators.empty_at_middle         import EmptyAtMiddle

from .operators.plane_through_points    import PlaneThroughPoints
from .operators.bisect_plane            import BisectPlane

from .operators.Scratch                 import Scratch

bl_info = {
    "name": "GeoBlender",
    "description": "A Geometry addon for Blender",
    "author": "Mustafa Quraish",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/mustafaquraish/GeoBlender",
    "tracker_url": "https://github.com/mustafaquraish",
    "category": "Geometry"
}


# Register all classes in the current module
classes = [obj for _, obj in getmembers(modules[__name__]) if isclass(obj)]
register, unregister = bpy.utils.register_classes_factory(classes)
