import bpy
from ..utils.objects import new_empty
from ..utils.drivers import add_driver


class ReflectAboutPoint(bpy.types.Operator):
    bl_label = "Reflect about Point"
    bl_idname = "geometry.reflect_about_point"
    bl_description = "Replect an object about a point"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]
        active = bpy.context.object

        if active is None:
            self.report({'ERROR'}, 'No active object selected')
            return {'CANCELLED'}

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
