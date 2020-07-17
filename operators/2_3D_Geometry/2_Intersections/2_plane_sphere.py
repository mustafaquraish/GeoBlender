import bpy
from GeoBlender.utils.objects import new_circle, add_abs_bevel, new_point
from GeoBlender.geometry.intersections import plane_sphere_intersection


class PlaneSphereIntersection(bpy.types.Operator):
    bl_label = "Plane - Sphere"
    bl_idname = "geometry.plane_sphere_intersection"
    bl_description = ("Returns the intersections of a plane "
                      "and sphere. Select a plane and a sphere")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of segment",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if (not ('Sphere' in A.data.name and 'Plane' in B.data.name) and
                not ('Plane' in A.data.name and 'Sphere' in B.data.name)):
            return False

        return True

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        if 'Sphere' in A.data.name and 'Plane' in B.data.name:
            sphere, plane = A, B
        elif 'Plane' in A.data.name and 'Sphere' in B.data.name:
            sphere, plane = B, A
        else:
            self.report({'ERROR'}, 'Need to select a plane and a sphere')
            return {'CANCELLED'}  # Shouldn't get here...

        circle = new_circle()
        plane_sphere_intersection(circle, plane, sphere, hide_extra=True)
        add_abs_bevel(circle, self.bevel_depth)
        return {'FINISHED'}
