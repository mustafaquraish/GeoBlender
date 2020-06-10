import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_cone
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_empty
from GeoBlender.geometry.lines import segment
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track
from GeoBlender.utils.drivers import add_driver, add_driver_distance


class Vector(bpy.types.Operator):
    bl_label = "Vector"
    bl_idname = "geometry.vector"
    bl_description = (
        "Add a vector from one point (origin) to another (endpoint)."
        " Select two points. The endpoint should be active")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # GeoBlender Panel Type
    gb_panel = '2D Constructions > Basic Tools > Lines'

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of segment",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    cone_radius: bpy.props.FloatProperty(
        name="Arrow radius:",
        description="Radius of the arrow",
        min=0,
        soft_max=4,
        default=1,
    )

    cone_length: bpy.props.FloatProperty(
        name="Arrow length:",
        description="Length of the arrow",
        min=0,
        soft_max=5,
        default=2,
    )

    hide_endpoint: bpy.props.BoolProperty(
        name="Hide endpoint:",
        description="Hide the selected endpoint of the vector",
        default=False
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        A_new = new_empty(hide=True)
        e_new = new_empty(hide=True)
        e_new.location[0] = self.bevel_depth
        e_new.location[1] = self.cone_length
        e_new.location[2] = self.cone_radius

        add_driver(obj=A_new,
                   prop='location',
                   fields='XYZ',
                   vars_def={'d': ('distance', A, B),
                             'b1': ('transform', B, 'location', '-'),
                             'a1': ('transform', A, 'location', '-'),
                             'bev': ('transform', e_new, 'location', 'X'),
                             'dep': ('transform', e_new, 'location', 'Y'),
                             'r1': ('transform', e_new, 'location', 'Z'), },
                   expr="b1 + (1-(bev*dep)/(r1*d))*(a1-b1)")

        line = new_line()
        segment(line, B, A_new)
        add_abs_bevel(line, self.bevel_depth)
        line.name = "Vector"

        cone = new_cone(radius1=self.cone_radius, depth=self.cone_length)
        copy_location(cone, A)
        copy_rotation(cone, A)
        locked_track(
            obj=cone,
            lock='Z',
            axis='-X',
            target=B
        )
        A.hide_viewport = self.hide_endpoint

        return {'FINISHED'}
