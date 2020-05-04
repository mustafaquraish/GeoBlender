import bpy
from ..utils.new_objects import new_plane
from ..utils.constraints import copy_location, damped_track, locked_track

class PointsPlane(bpy.types.Operator):
    bl_label = "Plane through Points"
    bl_idname = "geometry.points_plane"
    bl_description = "Constrained plane through 3 points"

    def execute(self, context):
        
        if (len(context.selected_objects) < 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        plane = new_plane(context, size=20)
        copy_location(plane, target=A)
        damped_track(plane, track='X', target=B)
        locked_track(plane, track='Y', lock='X', target=C)

        return {'FINISHED'}
