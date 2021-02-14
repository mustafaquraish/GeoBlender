import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line, uniform_scale
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import ray


class AngleArcTwoPointsFree(bpy.types.Operator):
    bl_label = "Arc for angle"
    bl_idname = "geometry.create_angle_arc_free"
    bl_description = ("Add the arc of an angle with given center "
                      "and one point on each of the two sides of the angle. "
                      "Select three points. The center should "
                      "be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    other_angle: bpy.props.BoolProperty(
        name="Display the outer angle:",
        description="Display the outer angle",
        default=True,
    )

    hide_arc: bpy.props.BoolProperty(
        name="Hide arc:",
        description="Hide the arc",
        default=False,
    )

    hide_endpoints: bpy.props.BoolProperty(
        name="Hide endpoints:",
        description="Hide the arc endpoints",
        default=True,
    )

    display_sides: bpy.props.BoolProperty(
        name="Display sides:",
        description="Display the angle sides",
        default=False,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of arc bevel",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    radius: bpy.props.FloatProperty(
        name="Arc radius:",
        description="Radius of arc",
        min=0.01,
        soft_max=20,
        default=1
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Point radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 3 and
                context.object is not None)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-3:]
        others.remove(A)
        B, C = others

        arc = new_arc(angle=360, sides=64, hide=self.hide_arc)

        if self.display_sides:
            side1 = new_line()
            add_abs_bevel(side1, self.bevel_depth)
            side2 = new_line()
            add_abs_bevel(side2, self.bevel_depth)
            ray(side1, A, B)
            ray(side2, A, C)

        uniform_scale(arc, self.radius)

        add_abs_bevel(arc, self.bevel_depth)
        align_to_plane_of(arc, A, B, C)

        if self.other_angle:
            B, C = C, B

        add_driver(
            obj=arc.data,
            prop='bevel_factor_start',
            vars_def={
                'ax': ('transform', A, 'location', 'X'),
                'ay': ('transform', A, 'location', 'Y'),
                'az': ('transform', A, 'location', 'Z'),
                'bx': ('transform', B, 'location', 'X'),
                'by': ('transform', B, 'location', 'Y'),
                'bz': ('transform', B, 'location', 'Z'),
                'cx': ('transform', C, 'location', 'X'),
                'cy': ('transform', C, 'location', 'Y'),
                'cz': ('transform', C, 'location', 'Z'),
            },
            expr='gb_drive_angle_bevel(True,ax,ay,az,bx,by,bz,cx,cy,cz)'
        )

        add_driver(
            obj=arc.data,
            prop='bevel_factor_end',
            vars_def={
                'ax': ('transform', A, 'location', 'X'),
                'ay': ('transform', A, 'location', 'Y'),
                'az': ('transform', A, 'location', 'Z'),
                'bx': ('transform', B, 'location', 'X'),
                'by': ('transform', B, 'location', 'Y'),
                'bz': ('transform', B, 'location', 'Z'),
                'cx': ('transform', C, 'location', 'X'),
                'cy': ('transform', C, 'location', 'Y'),
                'cz': ('transform', C, 'location', 'Z'),
            },
            expr='gb_drive_angle_bevel(False,ax,ay,az,bx,by,bz,cx,cy,cz)'
        )

        end1 = new_point(radius=self.sphere_radius, hide=self.hide_endpoints)
        end1.name = "Arc endpoint"
        end2 = new_point(radius=self.sphere_radius, hide=self.hide_endpoints)
        end2.name = "Arc endpoint"
        position_on_curve(end1, arc, position=0)
        position_on_curve(end2, arc, position=1)

        add_driver(
            obj=end1.constraints[-1],
            prop='offset_factor',
            vars_def={
                'bev': ("datapath", arc, "data.bevel_factor_start"),
            },
            expr="bev"
        )

        add_driver(
            obj=end2.constraints[-1],
            prop='offset_factor',
            vars_def={
                'bev': ("datapath", arc, "data.bevel_factor_end"),
            },
            expr="bev"
        )

        return {'FINISHED'}
