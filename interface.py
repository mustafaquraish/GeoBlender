import bpy

from .operators.create_inscribed_circle import CreateInscribedCircle
from .operators.create_radical_axis import CreateRadicalAxis
from .operators.create_circumcircle import CreateCircumcircle
from .operators.create_circumsphere import CreateCircumsphere
from .operators.create_euler_circle import CreateEulerCircle
from .operators.create_euler_line import CreateEulerLine
from .operators.create_line_segment import CreateLineSegment
from .operators.create_triangle import CreateTriangle
from .operators.create_line import CreateLine

from .operators.create_triangle_altitude import CreateTriangleAltitude
from .operators.create_triangle_bisector import CreateTriangleBisector
from .operators.create_triangle_median import CreateTriangleMedian

from .operators.empty_at_circumcenter import EmptyAtCircumcenter
from .operators.empty_at_orthocenter import EmptyAtOrthocenter
from .operators.empty_at_barycenter import EmptyAtBarycenter
from .operators.empty_at_incenter import EmptyAtIncenter
from .operators.empty_at_middle import EmptyAtMiddle

from .operators.line_line_intersection import LineLineIntersection
from .operators.line_circle_intersection import LineCircleIntersection
from .operators.circle_circle_intersection import CircleCircleIntersection

from .operators.plane_through_points import PlaneThroughPoints
from .operators.bisect_plane import BisectPlane


class GeoBlenderProperties(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_props"
    bl_label = "Default Properties"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.geoblender_settings

        row = layout.row()
        row.prop(settings, 'hide_extra')

        row = layout.row()
        row.prop(settings, "plane_size", expand=True)

        row = layout.row()
        row.prop(settings, 'bevel_depth', expand=True)

        row = layout.row()
        row.prop(settings, 'collection_name', expand=True)


# class GeoBlenderOperators(bpy.types.Panel):
#     bl_idname = "OBJECT_PT_geoblender_ops"
#     bl_label = "Operators"
#     bl_category = "GeoBlender"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout
#         layout.use_property_split = True

#         row = layout.row()
#         row.label(text="Geometric Operators", icon="VIEW3D")

#         for op in operators:
#             row = layout.row()
#             row.operator(op.bl_idname)


class GeoBlender2DConstructions(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_2d_construtions"
    bl_label = "2D Constructions"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        operators = [
            CreateInscribedCircle,
            EmptyAtCircumcenter,
            CreateRadicalAxis,
            CreateCircumcircle,
            CreateEulerCircle,
            CreateEulerLine,
            CreateLineSegment,
            CreateLine,
        ]

        for op in operators:
            row = layout.row()
            row.operator(op.bl_idname)


class GeoBlender3DConstructions(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_3d_construtions"
    bl_label = "3D Constructions"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        operators = [
            PlaneThroughPoints,
            CreateCircumsphere,
            BisectPlane,
        ]

        for op in operators:
            row = layout.row()
            row.operator(op.bl_idname)


class GeoBlenderTriangleConstructions(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_tri_construtions"
    bl_label = "Triangle Constructions"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        operators = [
            CreateTriangle,
            EmptyAtIncenter,
            CreateTriangleAltitude,
            CreateTriangleBisector,
            CreateTriangleMedian,
            EmptyAtBarycenter,
            EmptyAtOrthocenter
        ]

        for op in operators:
            row = layout.row()
            row.operator(op.bl_idname)


class GeoBlenderPlanarIntersections(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_planar_intersections"
    bl_label = "Planar Intersections"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        row = layout.row()
        row.label(text="For objects on the same plane")

        operators = [
            LineLineIntersection,
            LineCircleIntersection,
            CircleCircleIntersection
        ]

        for op in operators:
            row = layout.row()
            row.operator(op.bl_idname)
