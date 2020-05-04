import bpy
from ..utils.new_objects import new_plane
from ..utils.constraints import copy_location, damped_track, locked_track

class EmptyMiddle(bpy.types.Operator):
    bl_label = "Add empty in middle"
    bl_idname = "geometry.empty_middle"
    bl_description = "Add an empty exactly in the middle of objects"

    def execute(self, context):
        
        if (len(context.selected_objects) != 2):
            self.report({'ERROR'}, 'Need to select 2 objects')
            return {'CANCELLED'}

        (A, B) = context.selected_objects[-2:]

        empty = new_empty(context, size=20)
        copy_location(plane, target=A)
        damped_track(plane, track='X', target=B)
        locked_track(plane, track='Y', lock='X', target=C)

        return {'FINISHED'}
