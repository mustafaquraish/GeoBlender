import bpy

class Plane(bpy.types.Operator):
    bl_label = "Plane"
    bl_idname = "geometry.plane"
    bl_description = "Add a plane"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Planes'

    
    @classmethod
    def poll(cls, context):
        # return False
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        if 'Circle' not in A.data.name or 'Circle' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        (A, B) = context.selected_objects[-2:]

        X = new_point()
        Y = new_point()
        circle_circle_intersection(X, Y, A, B, hide_extra=self.hide_extra)

        return {'FINISHED'}
