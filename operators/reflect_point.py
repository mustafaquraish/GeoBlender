import bpy
from ..utils.objects import new_empty
from ..utils.drivers import add_driver


class ReflectAboutPoint(bpy.types.Operator):
    bl_label = "Reflect about Point"
    bl_idname = "geometry.reflect_about_point"
    bl_description = "Reflect an object about a point"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        active = bpy.context.object

        others = [A, B]
        others.remove(active)
        other = others[0]

        # active, other

        empty = new_empty()
        add_driver(
            obj=empty,
            prop='location',
            fields='XYZ',
            vars_def={
                'a': ('transform', active, 'location', '-'),
                'o': ('transform', other, 'location', '-'),
            },
            expr='o + (a-o)*2'
        )

        return {'FINISHED'}
