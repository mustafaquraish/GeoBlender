import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.geometry.intersections import line_circle_intersections



class LineCircleIntersection(bpy.types.Operator):
    bl_label = "Line - Circle"
    bl_idname = "geometry.line_circle_intersection"
    bl_description = "Returns the intersections of a line " +\
                     "and circle. Select a line and a circle"
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
        if (len(context.selected_objects) != 2):
            return False

        (A, B) = context.selected_objects[-2:]

        if not (isinstance(A.data, bpy.types.Curve) and
                isinstance(B.data, bpy.types.Curve)):
            return False

        if (not ('Circle' in A.data.name and 'Line' in B.data.name) and
                not ('Line' in A.data.name and 'Circle' in B.data.name)):
            return False

        return True

    def invoke(self, context, event):
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius

        return self.execute(context)

    def execute(self, context):
        (A, B) = context.selected_objects[-2:]

        if 'Circle' in A.data.name and 'Line' in B.data.name:
            circle, line = A, B
        elif 'Line' in A.data.name and 'Circle' in B.data.name:
            circle, line = B, A
        else:
            self.report({'ERROR'}, 'Need to select a line and a circle')
            return {'CANCELLED'}  # Shouldn't get here...

        (A, B) = context.selected_objects[-2:]

        X = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius)
        Y = new_point(use_spheres=self.use_spheres,
                           radius=self.sphere_radius)
        line_circle_intersections(
            X, Y, line, circle, hide_extra=self.hide_extra)

        return {'FINISHED'}