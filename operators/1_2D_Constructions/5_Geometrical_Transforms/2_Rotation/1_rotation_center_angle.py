import bpy
import math
from GeoBlender.utils.objects import new_arc, new_empty, duplicate, new_circle
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver_distance, add_driver
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.circles import circle_from_center_point
from GeoBlender.geometry.lines import bisecting_line_of_line
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, copy_scale, follow_path


class ScratchRot(bpy.types.Operator):
    bl_label = "Rotation about a point"
    bl_idname = "geometry.rotation_about_point"
    bl_description = ("Adds the rotation of any object about a point."
                      " Select an object and the origin of rotation."
                      " The object should be active. The angle of rotation "
                      "can be dynamically changed via the X coordinate of the "
                      "Rotation Driver empty that is created")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    angle_rot: bpy.props.FloatProperty(
        name="Angle of rotation:",
        description="Sets the angle of rotation in degrees",
        min=0,
        soft_max=360,
        default=0,
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

        for obj in others:
            # Make duplicate and reset position
            new_obj = duplicate(obj)
            new_obj.location *= 0
            copy_rotation(new_obj, obj)

            # Form circle at origin going through point
            circle = new_circle()
            circle_from_center_point(circle, A, obj)
            locked_track(circle, lock='Z', axis='Y', target=obj)

            follow_path(
                new_obj, 
                target=circle, 
                follow=True, 
                fixed=True, 
                offset=(self.angle_rot/360.0) % 1
            )

            # Option to change bevel
            if (isinstance(obj.data, bpy.types.Curve)):
                add_abs_bevel(new_obj, self.bevel_depth)

        return {'FINISHED'}
