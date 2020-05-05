import bpy
from ..utils.objects import new_plane
from ..utils.geometry import align_to_plane_of


class PointsPlane(bpy.types.Operator):
    bl_label = "Plane through Points"
    bl_idname = "geometry.points_plane"
    bl_description = "Constrained plane through 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]
        plane = new_plane(size=20)
        align_to_plane_of(plane, A, B, C)

        return {'FINISHED'}
