import bpy
from GeoBlender.utils.objects import new_plane, new_line, new_arc
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line


class Scratch(bpy.types.Operator):
    bl_label = "Scratch"
    bl_idname = "geometry.create_angle_scratch_mea"
    bl_description = 'To display the angle between two points from the '\
                     'active object'
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide: bpy.props.BoolProperty(
        name="Hide:",
        description="hide",
        default=True,
    )

    other_angle: bpy.props.BoolProperty(
        name="Use other side:",
        description="Display the outer angle",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of arc bevel",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of Arc",
        min=0.01,
        soft_max=20,
        default=1,
    )

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        (B, C) = others
        
        arc = new_arc(angle=360, sides=64)

        for i in range(3):
            arc.scale[i] = self.radius

        add_abs_bevel(arc, self.bevel_depth)
        align_to_plane_of(arc, A, B, C)
        
        return {'FINISHED'}
