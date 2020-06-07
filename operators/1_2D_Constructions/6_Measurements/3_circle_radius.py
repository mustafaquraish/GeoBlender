import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import distance_function 


class RadiusMeasurement(bpy.types.Operator):
    bl_label = "Radius"
    bl_idname = "geometry.measure_radius"
    bl_description = ("Computes the radius of a segment. Select a circle")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    

    
    


    @classmethod
    def poll(cls, context):
        return True

        
    def execute(self, context):
        A = context.active_object # A : circle
        B = new_point(hide=True) 
        position_on_curve(B, A) # B : point on the circle
        yes =  distance_function(A, B) # computing the radius

        context.scene.geoblender_measurements.radius = yes

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_radius")
        row.prop(measurements, "radius", text="")

    
        

        