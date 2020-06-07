import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import distance_function


class LengthMeasurement(bpy.types.Operator):
    bl_label = "Length"
    bl_idname = "geometry.measure_length"
    bl_description = ("Computes the length of a segment. Select a line")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    

    
    


    @classmethod
    def poll(cls, context):
        return True

        
    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]

       
        #WILL NOT ALWAYS WORK! BECAUSE A, B MIGHT BE CONSTRAINT AND LOC =0. 
        #I introduce drivers, but it returns only zero

        B_clone = new_point(use_spheres=False, hide = False)
        A_clone = new_point(use_spheres=False, hide = False)
        
        
        add_driver(obj=B_clone,
                   prop='location',
                   fields='XYZ',
                   vars_def={'a1': ('transform', B, 'location', '-'), },
                   expr="a1")
        
        add_driver(obj = A_clone,
                   prop = 'location',
                   fields= 'XYZ',
                   vars_def={'current': ('transform', A, 'location', '-'),},
                   expr="current")

        yes = distance_function(A_clone, B_clone)    

        context.scene.geoblender_measurements.length = yes

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_length")
        row.prop(measurements, "length", text="")

    
        

        