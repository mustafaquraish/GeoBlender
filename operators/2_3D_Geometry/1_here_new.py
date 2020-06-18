import bpy

class InversionPoinSft3d(bpy.types.Operator):
    bl_label = "TO DO"
    bl_idname = "geometry.placeholder_thing"
    bl_description = ("We are still working on 3D!")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        return {'FINISHED'}
