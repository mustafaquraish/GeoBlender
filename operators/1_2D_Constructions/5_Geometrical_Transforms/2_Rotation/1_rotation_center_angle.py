import bpy
import math
from GeoBlender.utils.objects import new_arc, new_empty, duplicate
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver_distance
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, copy_scale


class ScratchRot(bpy.types.Operator):
    bl_label = "Rotation about a point"
    bl_idname = "geometry.rotation_about_point"
    bl_description = ("Adds the rotation of any object about a point."
                      " Select an object and the origin of rotation."
                      " The object should be active")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    angle_rot: bpy.props.FloatProperty(
        name="Angle of rotation:",
        description="Sets the angle of rotation in degrees",
        min=0,
        soft_max=360,
        default=45,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of circle",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects
        others.remove(A)
        B = others[0]

        e_rot = new_empty(hide=self.hide_extra)
        e_rot.name = "e_rot"
        e_loc = new_empty(hide=self.hide_extra)
        e_loc.name = "e_loc"
        e_center_X_track = new_empty(hide=self.hide_extra)
        e_center_X_track.name = "e_center_track"
        e_center_X_rotated = new_empty(hide=self.hide_extra)
        e_center_X_rotated.name = "e_center_rotated"

        e_rot.parent = A
        e_rot.rotation_euler[2] = math.radians(self.angle_rot)

        copy_location(e_center_X_track, B)
        copy_rotation(e_center_X_track, B)
        locked_track(e_center_X_track, 'Z', 'X', A)

        e_center_X_rotated.parent = e_center_X_track
        e_center_X_rotated.rotation_euler[2] = math.radians(self.angle_rot)

        e_loc.parent = e_center_X_rotated

        add_driver_distance(e_loc, 'location', 'X', A, B)
        copy_rotation(e_loc, e_rot)

        dupli_A = duplicate(A)
        dupli_A.name = "Rotated object"
        copy_location(dupli_A, e_loc)
        copy_rotation(dupli_A, e_loc)
        copy_scale(dupli_A, A)

        if (isinstance(A.data, bpy.types.Curve)):
            add_abs_bevel(dupli_A, self.bevel_depth)

        

        return {'FINISHED'}
