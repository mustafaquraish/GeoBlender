import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, duplicate
from GeoBlender.geometry.lines import segment


class StaticVariety(bpy.types.Operator):
    bl_label = "Static family"
    bl_idname = "geometry.static_family"
    bl_description = ("Adds still copies of a dependent object "
                      "while another point moves on a curve (point must be "
                      "constrained on a curve). Select the object(active) "
                      "and the point")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


        

    copies_number: bpy.props.IntProperty(
        name="Copies number:",
        description="Number of particles to create along the locus",
        min=0,
        soft_max=100,
        default=5,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of the copies (if curves)",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    @classmethod
    def poll(cls, context):
         return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth

        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]
        
        
        prev_selected = bpy.context.selected_objects
        prev_active = bpy.context.object

        COLLECTION_NAME = bpy.context.scene.geoblender_settings.collection_name

        if COLLECTION_NAME not in bpy.data.collections:
            collection = bpy.data.collections.new(COLLECTION_NAME)
            bpy.context.scene.collection.children.link(collection)
        else:
            collection = bpy.data.collections[COLLECTION_NAME]

           
        
        for i in range(1, (self.copies_number)+1):
            
            B.constraints["Follow Path"].offset_factor = (i-1) / (self.copies_number)
            
                                     
            
            bpy.ops.object.select_all(action='DESELECT')
            
            copy = duplicate(A)
            copy.select_set(True)
            

            copy.driver_remove('scale')
            copy.driver_remove('location')
            copy.driver_remove('rotation_euler')

            bpy.ops.object.visual_transform_apply()
        
            for constraint in copy.constraints:
                copy.constraints.remove(constraint)

            
            

            # Option to change bevel
            if (isinstance(copy.data, bpy.types.Curve)):
                add_abs_bevel(copy, self.bevel_depth)

            old_collections = copy.users_collection  # get old collection
            collection.objects.link(copy)    # put obj in extras collection
            for coll in old_collections:
                coll.objects.unlink(copy)    # unlink from old collection

            bpy.ops.object.select_all(action='DESELECT')
            for obj in prev_selected:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = prev_active

            

         
            
         

        return {'FINISHED'}