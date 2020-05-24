import bpy
import math

class CreateAngleArc(bpy.types.Operator):
    bl_label = "Measure Angle"
    bl_idname = "geometry.measure_angle"
    bl_description = 'Measure angle between two points from the '\
                     'active object'
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    other_angle: bpy.props.BoolProperty(
        name="Use other side:",
        description="Display the outer angle",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        B, C = others


        v1 = B.location - A.location
        v2 = C.location - A.location
        frac = v1.dot(v2) / (v1.length * v2.length)
        angle = math.acos(frac)
        normal = v1.cross(v2)

        # This is tricky: we need to establish some sort of 'correct' normal for
        # the plane around which everything is oriented. Arbitrarily, we assume
        # that the normal with greater Z component is 'correct'. If equal, compare
        # Y, then X.
        is_correct = (
            (normal.z < 0) or
            (normal.z == 0 and normal.y < 0) or
            (normal.z == normal.y == 0 and normal.x < 0)
        )

        if is_correct:
            signed_angle = angle
        else:
            signed_angle = math.tau - angle
        
        if self.other_angle:
            signed_angle = math.tau - signed_angle

        context.scene.geoblender_measurements.angle = signed_angle

        return {'FINISHED'}
