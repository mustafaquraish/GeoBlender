import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.intersections import plane_plane_intersection


class planeplaneInter(bpy.types.Operator):
    bl_label = "Plane - Plane"
    bl_idname = "geometry.plane_plane"
    bl_description = ("Returns the intersection of 2 planes. Select 2 planes."
                      "NOT IMPLEMENTED YET")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use spheres for points. Otherwise use empties.",
        default=True,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    @classmethod
    def poll(cls, context):
        # Temporarily...
        return False

        if not (len(context.selected_objects) == 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve)):
            return False

        if not (isinstance(B.data, bpy.types.Curve)):
            return False

        if 'plane' not in A.data.name:
            return False

        if 'plane' not in B.data.name:
            return False

        return True

    def invoke(self, context, event):
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]
        inter = new_point(use_spheres=self.use_spheres,
                          radius=self.sphere_radius)

        plane_plane_intersection(inter, A, B, hide_extra=self.hide_extra)

        return {'FINISHED'}
