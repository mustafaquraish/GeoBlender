from . import operators
import bpy


class GeoBlenderPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender"
    bl_label = "GeoBlender"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.geoblender_settings

        row = layout.row()
        row.label(text="Default Properties", icon="SETTINGS")

        row = layout.row()
        row.prop(settings, 'hide_extra')

        row = layout.row()
        row.prop(settings, "plane_size", expand=True)

        row = layout.row()
        row.prop(settings, 'bevel_depth', expand=True)

        row = layout.row()
        row.prop(settings, 'collection_name', expand=True)

        layout.row().separator()

        row = layout.row()
        row.label(text="Geometric Operators", icon="VIEW3D")

        for op in operators:
            row = layout.row()
            row.operator(op.bl_idname)