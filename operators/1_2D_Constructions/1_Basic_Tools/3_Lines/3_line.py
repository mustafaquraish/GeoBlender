import bpy


class Line(bpy.types.Operator):
    bl_label = "Line"
    bl_idname = "geometry.line"
    bl_description = "Add a line through 2 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Lines'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.0,
    )

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of line",
        min=0,
        soft_max=300,
        default=100,
    )

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
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        radical_axis = new_line(length=self.length, axis='Y')
        move_origin_center(radical_axis)
        put_at_radical_intercept(radical_axis, A, B)
        copy_rotation(radical_axis, target=A)
        locked_track(radical_axis, lock='Z', axis='X', target=B)
        for i in range(3):
            radical_axis.scale[i] = self.length
        add_abs_bevel(radical_axis, self.bevel_depth)
        radical_axis.name = "Radical Axis"

        return {'FINISHED'}
