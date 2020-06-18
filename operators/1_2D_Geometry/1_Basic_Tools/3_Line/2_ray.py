import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel
from GeoBlender.geometry.lines import ray


class Ray(bpy.types.Operator):
    bl_label = "Ray"
    bl_idname = "geometry.ray"
    bl_description = ("Add a ray from a point to another point. Select two "
                      "points. The origin of the ray should be active")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of ray",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of ray",
        min=0,
        soft_max=300,
        default=100,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        line = new_line()
        ray(line, A, B, length=self.length)
        add_abs_bevel(line, self.bevel_depth)
        line.name = "Ray"

        return {'FINISHED'}
