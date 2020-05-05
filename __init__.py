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

import bpy
from sys        import modules 
from inspect    import getmembers, isclass

# Import operator classes
from .operators.Scratch                 import Scratch
from .operators.bisect_plane            import BisectPlane
from .operators.empty_middle            import EmptyMiddle
from .operators.points_plane            import PointsPlane
from .operators.draw_triangle           import DrawTriangle
from .operators.empty_incenter          import EmptyIncenter
from .operators.empty_barycenter        import EmptyBarycenter
from .operators.empty_orthocenter       import EmptyOrthocenter
from .operators.draw_circumcircle       import DrawCircumcircle
from .operators.empty_circumcenter      import EmptyCircumcenter
from .operators.line_between_points     import LineBetweenPoints
from .operators.draw_inscribed_circle   import DrawInscribedCircle

# Register all classes in the current module
classes = [obj for _, obj in getmembers(modules[__name__]) if isclass(obj)]
register, unregister = bpy.utils.register_classes_factory(classes)
