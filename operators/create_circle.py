import bpy
from ..utils.objects import new_circle, add_abs_bevel
from ..geometry.circles import make_circle_from_center_point


class CreateCircle(bpy.types.Operator):
    bl_label = "Create Circle"
    bl_idname = "geometry.create_circle"
    bl_description = "Create a circle through a given center and point"
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        # B is the point on the circle, A is the center
        B = context.active_object
        others = context.selected_objects[-2:]
        others.remove(B)
        A = others[0]

        circ = new_circle()
        
        make_circle_from_center_point(circ, A, B)

        add_abs_bevel(circ, self.bevel_depth)
        circ.name = "Circle"

        return {'FINISHED'}
