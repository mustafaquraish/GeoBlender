import bpy
from ..utils.objects import new_circle, new_empty, new_plane
from ..utils.geometry import put_at_incenter, make_orthogonal_to, PLANE_SIZE
from ..utils.constraints import copy_transforms, project_nearest, copy_location
from ..utils.drivers import add_driver_distance


class DrawInscribedCircle(bpy.types.Operator):
    bl_label = "Create Inscribed Circle"
    bl_idname = "geometry.create_inscribed_circle"
    bl_description = "Form the inscribed circle of the 3 points"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed for inscribed circle",
        default=True,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Depth for circle bevel",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
    )

    def execute(self, context):

        if (len(context.selected_objects) != 3):
            self.report({'ERROR'}, 'Need to select 3 objects')
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]

        plane_ab = new_plane(size=PLANE_SIZE, hide=self.hide_extra)
        plane_ab.name = 'plane_ab'
        make_orthogonal_to(plane_ab, A, B, C)

        inscribed_center = new_empty(hide=self.hide_extra)
        inscribed_center.name = "Inscribed center"
        put_at_incenter(inscribed_center, A, B, C, hide_extra=self.hide_extra)

        circ_point = new_empty(hide=self.hide_extra)
        copy_location(circ_point, inscribed_center)
        project_nearest(circ_point, target=plane_ab)

        circle = new_circle()
        copy_transforms(circle, target=inscribed_center, transforms="LR")
        add_driver_distance(
            obj=circle,
            prop='scale',
            fields='XY',
            A=inscribed_center,
            B=circ_point
        )
        circle.data.bevel_depth = self.bevel_depth
        circle.name = "Inscribed circle"

        return {'FINISHED'}
