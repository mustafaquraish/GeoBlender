import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import distance_function, segment


class LengthMeasurement(bpy.types.Operator):
    bl_label = "Length"
    bl_idname = "geometry.measure_length"
    bl_description = ("Computes the length of a segment. Select line segment")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    

    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1 and
                context.object is not None):
            A = context.active_object
           

            if isinstance(A.data, bpy.types.Curve):
                return 'Line' in A.data.name

        return False

            
    def execute(self, context):
        A = context.active_object
        
        length = A.scale[0]
        context.scene.geoblender_measurements.length = length

        # Clearly the problem is with adding DRIVERS at the SAME FILE. 
        # existing drivers are recorded properly.

        # context.scene.geoblender_measurements.length = B_clone.matrix_world.translation[0]

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_length")
        row.prop(measurements, "length", text="")

    
        

        