import bpy
from ..utils.objects import new_circle, add_abs_bevel
from ..utils.geometry import put_in_between
from ..utils.constraints import damped_track, locked_track
from ..utils.drivers import add_driver


class CreateEllipse(bpy.types.Operator):
    bl_label = "Create Ellipse"
    bl_idname = "geometry.create_ellipse"
    bl_description = "Create an ellipse through a point and the focii"
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = '2D Constructions'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of ellipse",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        # C is the point on the ellipse, A and B are the focii
        C = context.active_object
        others = context.selected_objects[-3:]
        others.remove(C)
        A, B = others

        circ = new_circle()
        put_in_between(circ, A, B)
        damped_track(circ, axis='X', target=B)
        locked_track(circ, lock='X', axis='Y', target=C)

        add_driver(
            obj=circ,
            prop='scale',
            fields='YZ',  # Scale Z too so bevel looks 3D.
            vars_def={
                'ab': ('distance', A, B),
                'ac': ('distance', A, C),
                'bc': ('distance', B, C),
            },
            expr='sqrt((ac+bc+ab)*(ac+bc-ab))/2'
        )

        add_driver(
            obj=circ,
            prop='scale',
            fields='X', 
            vars_def={
                'ac': ('distance', A, C),
                'bc': ('distance', B, C),
            },
            expr='(ac + bc)/2'
        )

        add_abs_bevel(circ, self.bevel_depth)
        circ.name = "Ellipse"
        circ.data.name = "Ellipse"

        return {'FINISHED'}
