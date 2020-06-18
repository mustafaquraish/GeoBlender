import bpy
import math
from GeoBlender.utils.objects import new_circle, new_empty, duplicate
from GeoBlender.utils.drivers import add_driver_distance
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, copy_scale


class Scratch(bpy.types.Operator):
    bl_label = "Segment divider"
    bl_idname = "geometry.segment_divider"
    bl_description = ("Adds a point P that divides a segment AB with given "
                      "ratio PB/PA. The ratio is set at the operator panel. "
                      "Select two points, A, B. The point A (as above) "
                      "should be the active object")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    ratio: bpy.props.FloatProperty(
        name="Ratio:",
        description="Sets the ratio for dividing the segment",
        min=0,
        soft_max=1000,
        default=0.5,
    )

    display_inside: bpy.props.BoolProperty(
        name="Display inside:",
        description="Display point inside the selected segment",
        default=True,
    )

    display_outside: bpy.props.BoolProperty(
        name="Display outside:",
        description="Display point outside the selected segment",
        default=True,
    )

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
        return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        e_help = new_empty(hide=self.hide_extra)
        e_help.name = "Object defining drivers"
        e_help.location[0] = self.ratio

        if self.display_inside:
            new_inside = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
            new_inside.name = "Segment divider inside"
            copy_rotation(new_inside, A)

            add_driver(obj=new_inside,
                       prop='location',
                       fields='XYZ',
                       vars_def={'x1': ('transform', e_help, 'location', 'X'),
                                 'b1': ('transform', B, 'location', '-'),
                                 'a1': ('transform', A, 'location', '-'), },
                       expr="b1 + (x1/(1+x1))*(a1-b1)")

        if self.display_outside:

            if self.ratio > 1:

                new_outside = new_point(use_spheres=self.use_spheres,
                                        radius=self.sphere_radius)
                new_outside.name = "Segment divider outside"
                copy_rotation(new_outside, A)

                add_driver(
                    obj=new_outside,
                    prop='location',
                    fields='XYZ',
                    vars_def={
                        'x1': (
                            'transform',
                            e_help,
                            'location',
                            'X'),
                        'b1': (
                            'transform',
                            B,
                            'location',
                            '-'),
                        'a1': (
                            'transform',
                            A,
                            'location',
                            '-'),
                    },
                    expr="b1 + (x1/(x1-1))*(a1-b1)")

            if self.ratio < 1:
                new_outside = new_point(use_spheres=self.use_spheres,
                                        radius=self.sphere_radius)
                new_outside.name = "Segment divider outside"
                copy_rotation(new_outside, A)

                add_driver(
                    obj=new_outside,
                    prop='location',
                    fields='XYZ',
                    vars_def={
                        'x1': (
                            'transform',
                            e_help,
                            'location',
                            'X'),
                        'b1': (
                            'transform',
                            B,
                            'location',
                            '-'),
                        'a1': (
                            'transform',
                            A,
                            'location',
                            '-'),
                    },
                    expr="b1 - (x1/(1-x1))*(a1-b1)")

        return {'FINISHED'}
