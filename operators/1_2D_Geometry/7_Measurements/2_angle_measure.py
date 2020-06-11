import bpy
from GeoBlender.utils.objects import new_arc, add_abs_bevel, new_point
from GeoBlender.utils.objects import new_line
from GeoBlender.utils.geometry import align_to_plane_of
from GeoBlender.utils.drivers import add_driver, add_driver_distance
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.constraints import locked_track, position_on_curve
from GeoBlender.geometry.lines import ray


class AngleMeasurement(bpy.types.Operator):
    bl_label = "Angle"
    bl_idname = "geometry.measure_angle"
    bl_description = ("Computes the size of an angle. Create an arc (if not" 
                      " already) and select it")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    

    
    


    @classmethod
    def poll(cls, context):
        if (len(context.selected_objects) == 1 and
                context.object is not None):
            A = context.active_object
           

            if not (isinstance(A.data, bpy.types.Curve)):
                return False

            elif 'Arc' not in A.data.name:
                return False

            else:
                return True

        
        else:
            return False

        
    def execute(self, context):

        # The user needs to first create an arc, otherwise the measurement operator
        # will need to create such an arc (and everything else) every time.

        A = context.active_object
        
        start = A.data.bevel_factor_start 
        end = A.data.bevel_factor_end
        yes = abs(start-end)*360



        context.scene.geoblender_measurements.angle = yes

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_angle")
        row.prop(measurements, "angle", text="")

    
        

        