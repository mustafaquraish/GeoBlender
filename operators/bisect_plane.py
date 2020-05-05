import bpy
from ..utils.objects import new_plane
from ..utils.geometry import put_in_between
from ..utils.constraints import damped_track


class BisectPlane(bpy.types.Operator):
    bl_label = "Perperndicular Bisecting Plane"
    bl_idname = "geometry.bisect_plane"
    bl_description = "Make a plane that is a perpendicular bisector of two points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    influence: bpy.props.FloatProperty(
        name="Position:",
        description="Influence",
        max=1.0,
        min=0.0,
        default=0.5,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        plane = new_plane(size=10)
        put_in_between(plane, A, B, influence=self.influence)
        damped_track(plane, axis='Z', target=A)

        return {'FINISHED'}
