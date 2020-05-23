import bpy
from ..utils.objects import new_sphere
from ..utils.geometry import put_in_between
from ..utils.constraints import damped_track, locked_track
from ..utils.drivers import add_driver


class CreateEllipsoid(bpy.types.Operator):
    bl_label = "Create Ellipsoid"
    bl_idname = "geometry.create_ellipsoid"
    bl_description = "Create an ellipsoid through a point and the focii"
    bl_options = {'REGISTER', 'UNDO'}

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    segments: bpy.props.IntProperty(
        name="Resolution:",
        description="Resolution for the Sphere",
        min=3,
        soft_max=150,
        default=64,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        # C is the point on the ellipsoid, A and B are the focii
        C = context.active_object
        others = context.selected_objects[-3:]
        others.remove(C)
        A, B = others

        sphere = new_sphere()
        put_in_between(sphere, A, B)
        damped_track(sphere, axis='X', target=B)
        locked_track(sphere, lock='X', axis='Y', target=C)

        add_driver(
            obj=sphere,
            prop='scale',
            fields='ZY',
            vars_def={
                'ab': ('distance', A, B),
                'ac': ('distance', A, C),
                'bc': ('distance', B, C),
            },
            expr='sqrt((ac+bc+ab)*(ac+bc-ab))/2'
        )

        add_driver(
            obj=sphere,
            prop='scale',
            fields='X',
            vars_def={
                'ac': ('distance', A, C),
                'bc': ('distance', B, C),
            },
            expr='(ac + bc)/2'
        )

        sphere.name = "Ellipsoid"
        sphere.data.name = "Ellipsoid"

        return {'FINISHED'}
