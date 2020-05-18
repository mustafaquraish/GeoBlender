import bpy
from ..utils.objects import new_plane
from ..utils.geometry import put_at_circumcenter
from ..utils.constraints import damped_track, locked_track


class PlaneThroughPoints(bpy.types.Operator):
    bl_label = "Plane through Points"
    bl_idname = "geometry.points_plane"
    bl_description = "Constrained plane through 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '3D Constructions'

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for incenter",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3)

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B, C) = context.selected_objects[-3:]

        plane = new_plane(size=20)
        put_at_circumcenter(plane, A, B, C, hide_extra=self.hide_extra)
        damped_track(plane, axis='X', target=A)
        locked_track(plane, axis='Y', lock='X', target=B)
        plane.name = "Points Plane"

        return {'FINISHED'}
