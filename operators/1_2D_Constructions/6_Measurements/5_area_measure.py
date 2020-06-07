import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import distance_function, area_function


class AreaMeasurement(bpy.types.Operator):
    bl_label = "Area"
    bl_idname = "geometry.measure_area"
    bl_description = ("Computes the Area of a triangle. Select three points")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    

    
    


    @classmethod
    def poll(cls, context):
        return True

        
    def execute(self, context):
        
        (A, B, C) = context.selected_objects[-3:]

        yes = area_function(A, B, C)

         
        context.scene.geoblender_measurements.area = yes

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_area")
        row.prop(measurements, "area", text="")

    
        

        