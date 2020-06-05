import bpy
import math
from GeoBlender.utils.objects import new_circle, new_empty, duplicate
from GeoBlender.utils.drivers import add_driver_distance
from GeoBlender.utils.drivers import add_driver
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_point
from GeoBlender.geometry.lines import bisecting_line_of_points
from GeoBlender.geometry.lines import bisecting_line_of_line
from GeoBlender.geometry.lines import line_ends
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, copy_scale


class ScratchHommnum(bpy.types.Operator):
    bl_label = "Homothety with number ratio"
    bl_idname = "geometry.homothety_ratio"
    bl_description = (
        "Adds the homothetic tranform of an object (active) relative"
        " to an origin (point). The ratio is the number set at the " 
        "operator panel. Select the object (active) and an origin")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    ratio: bpy.props.FloatProperty(
        name="Homothety ratio:",
        description="Sets the homothety ratio",
        min=-150,
        soft_max=150,
        default=2,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of curve",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    display_center: bpy.props.BoolProperty(
        name="Display center:",
        description="Display center when object is a circle",
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
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth

        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

        e_help = new_empty(hide=self.hide_extra)
        e_help.name = "Object defining drivers"
        e_help.location[0] = self.ratio

        if not (isinstance(A.data, bpy.types.Curve)):
            new = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)
            new.name = "Homothetic object"

        # Can try to duplicate instead and then clear all constraints
        if 'Line' in A.data.name:
            new = new_line()
            new.name = "Homothetic object"
            add_abs_bevel(new, self.bevel_depth)

        if 'Circle' in A.data.name:
            new = new_circle()
            new.name = "Homothetic object"
            add_abs_bevel(new, self.bevel_depth)

        copy_rotation(new, A)
        add_driver(obj=new,
                   prop='location',
                   fields='XYZ',
                   vars_def={'x1': ('transform', e_help, 'location', 'X'),
                             'b1': ('transform', B, 'location', '-'),
                             'a1': ('transform', A, 'location', '-'), },
                   expr="b1 + x1*(a1-b1)")

        if 'Circle' in A.data.name:

            add_driver(obj=new,
                       prop='scale',
                       fields='XYZ',
                       vars_def={'x1': ('transform', e_help, 'location', 'X'),
                                 's1': ('transform', A, 'scale', 'X'), },
                       expr="x1*s1")

            if self.display_center:
                center = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
                copy_location(center, new)
                copy_rotation(center, new)

        if 'Line' in A.data.name:
            add_driver(obj=new,
                       prop='scale',
                       fields='XYZ',
                       vars_def={'x1': ('transform', e_help, 'location', 'X'),
                                 's1': ('transform', A, 'scale', 'X'), },
                       expr="x1*s1")
            end1 = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
            end2 = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
            line_ends(end1, end2, new)

        return {'FINISHED'}
