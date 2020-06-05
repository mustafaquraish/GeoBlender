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
from GeoBlender.geometry.lines import line_ends


class Homothety_lengths(bpy.types.Operator):
    bl_label = "Homothety with length ratio"
    bl_idname = "geometry.homothety_ratio_distances"
    bl_description = (
        "Adds the homothetic tranform of an object (active) relative"
        " to an origin (point) and ratio s/r, with s the length of a line segment" 
        " and r the radius of a circle. Select the object (active), the origin,"
        " a line segment (s) and a circle (r)")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    
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
        if (len(context.selected_objects) == 4 and
                context.object is not None):
            A = context.active_object
            others = context.selected_objects[-4:]
            others.remove(A)
            (O_test, L_test, R_test) = others
            if 'Sphere' in O_test.data.name:
                O = O_test
            elif 'Sphere' in L_test.data.name:
                O = L_test
            elif 'Sphere' in R_test.data.name:
                O = R_test
            else:
                return False
            others.remove(O)
            (L_test, R_test) = others
            if ('Line' in L_test.data.name and 
                'Circle' in R_test.data.name):
                return True
            elif ('Line' in R_test.data.name and 
                'Circle' in L_test.data.name):
                return True
            else: 
                return False
        else: 
            return False
        
        
        

    def invoke(self, context, event):
        self.use_spheres = context.scene.geoblender_settings.use_spheres
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        self.hide_extra = context.scene.geoblender_settings.hide_extra
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth

        return self.execute(context)

    def execute(self, context):

        A = context.active_object
        others = context.selected_objects[-4:]
        others.remove(A)
        (O_test, L_test, R_test) = others
        if 'Sphere' in O_test.data.name:
            O = O_test
        if 'Sphere' in L_test.data.name:
            O = L_test
        if 'Sphere' in R_test.data.name:
            O = R_test
        others.remove(O)
        (L_test, R_test) = others
        if 'Line' in L_test.data.name:
            L = L_test
            R = R_test               
        if 'Line' in R_test.data.name:
            L = R_test
            R = L_test

        # A: object to transform, O: origin, L: line, R: circle
               
        if not (isinstance(A.data, bpy.types.Curve)):
            new = new_point(use_spheres=self.use_spheres,
                            radius=self.sphere_radius)
            new.name = "Homothetic object"

        
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
                   vars_def={'s': ('transform', L, 'scale', 'X'),
                             'r': ('transform', R, 'scale', 'X'),
                             'b1': ('transform', O, 'location', '-'),
                             'a1': ('transform', A, 'location', '-'), },
                   expr="b1 + (s/r)*(a1-b1)")

        if 'Circle' in A.data.name:

            add_driver(obj=new,
                       prop='scale',
                       fields='XYZ',
                       vars_def={'s': ('transform', L, 'scale', 'X'),
                                 'r': ('transform', R, 'scale', 'X'),
                                 's1': ('transform', A, 'scale', 'X'), },
                       expr="(s/r)*s1")

            if self.display_center:
                center = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
                copy_location(center, new)
                copy_rotation(center, new)

        if 'Line' in A.data.name:
            add_driver(obj=new,
                       prop='scale',
                       fields='XYZ',
                       vars_def={'s': ('transform', L, 'scale', 'X'),
                                 'r': ('transform', R, 'scale', 'X'),
                                 's1': ('transform', A, 'scale', 'X'), },
                       expr="(s/r)*s1")
            end1 = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
            end2 = new_point(use_spheres=self.use_spheres,
                                   radius=self.sphere_radius)
            line_ends(end1, end2, new)

            

        return {'FINISHED'}
