import bpy

from GeoBlender.utils import objects
from GeoBlender.utils import geometry
from GeoBlender.utils import constraints


class PlanePlaneIntersection(bpy.types.Operator):
    """Form the line of intersection between two planes. Select both planes."""
    bl_idname = "add.planeplaneintersection"             # Unique identifier.
    bl_label = "Plane Plane Intersection"               # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}           # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of line",
        min=0,
        soft_max=0.5,
        default=0.2,
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
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Mesh) and
                isinstance(B.data, bpy.types.Mesh)):
            return False

        if not ('Plane' in A.data.name and 'Plane' in B.data.name):
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.length = context.scene.geoblender_settings.length
        return self.execute(context)

    # execute() is called when running the operator.
    def execute(self, context):
        _A, _B = context.selected_objects[-2:]

        A = objects.new_plane(hide=self.hide_extra)
        constraints.copy_transforms(A, _A, transforms='LR')

        B = objects.new_plane(hide=self.hide_extra)
        constraints.copy_transforms(B, _B, transforms='LR')
        
        # A point on the normal of Plane A
        A_norm = objects.new_empty(hide=self.hide_extra)
        A_norm.name = "A Norm"
        objects.uniform_scale(A_norm, 0.1)
        objects.set_parent(A_norm, A, keep_inverse=False)
        A_norm.location[2] = 1.0

        # Empty located a A, but in the same orientation as B
        B_rot_at_A = objects.new_empty(hide=self.hide_extra)
        B_rot_at_A.name = "B_rot_at_A"
        constraints.copy_location(B_rot_at_A, A)
        constraints.copy_rotation(B_rot_at_A, B)

        # (B_norm_at_a - A) gives the normal direction of B
        B_norm_at_a = objects.new_empty(hide=self.hide_extra)
        B_norm_at_a.name = "B_norm_at_a"
        objects.set_parent(B_norm_at_a, B_rot_at_A, keep_inverse=False)
        B_norm_at_a.location[2] = 1.0

        intersection_line = objects.new_line(axis='Z', length=self.length)
        objects.move_origin_center(intersection_line)
        objects.add_abs_bevel(intersection_line, self.bevel_depth)

        geometry.align_to_plane_of(intersection_line, A, A_norm, B_norm_at_a)        
        constraints.project_along_axis(intersection_line, 'Y', B, opposite=True)

        return {'FINISHED'}
