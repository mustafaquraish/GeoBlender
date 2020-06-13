import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, duplicate
from GeoBlender.geometry.lines import segment


class StaticVariety(bpy.types.Operator):
    bl_label = "Dynamic family"
    bl_idname = "geometry.dynamic_family"
    bl_description = ("Dynamically adds still copies of a dependent object "
                      "while another point moves on a curve (point must be "
                      "constrained on a curve). Select the object(active)"
                      " and the point")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


        

    copies_number: bpy.props.IntProperty(
        name="Copies number:",
        description="Number of particles to create along the locus",
        min=0,
        soft_max=100,
        default=5,
    )

    frame_gap: bpy.props.IntProperty(
        name="Frame gap:",
        description="Number of frames between the creation of new copies.",
        min=0,
        soft_max=100,
        default=5,
    )



    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of the copies (if curves).",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    for_test: bpy.props.BoolProperty(
        name="Testing copies:",
        description=("Select for testing dynamic creation of copies "
                     "in viewport. Creates new materials with transparency"),
        default=False,
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
            
            B.constraints["Follow Path"].keyframe_insert(
                                                    data_path='offset_factor', 
                                                    frame=1+i*self.frame_gap)
            
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
            
            copy.hide_render = True
            copy.keyframe_insert(data_path='hide_render', frame=1)
            copy.hide_render = False
            copy.keyframe_insert(data_path='hide_render', frame=1+i*self.frame_gap)

            if self.for_test:
                mat = bpy.data.materials.new(name="TEST MATERIAL {}".format(i))
                mat.use_nodes = True
                mat.blend_method = 'BLEND'
                mat_alpha = mat.node_tree.nodes["Principled BSDF"].inputs[18]
                
                mat_alpha.default_value = 0
                mat_alpha.keyframe_insert(data_path='default_value', frame=1)

                mat_alpha.default_value = 1
                mat_alpha.keyframe_insert(data_path='default_value', frame=1+i*self.frame_gap)
                # Assign it to object
                if copy.data.materials:
                    # assign to 1st material slot
                    copy.data.materials[0] = mat
                else:
                    # no slots
                    copy.data.materials.append(mat)
            
        



            bpy.ops.object.select_all(action='DESELECT')
            for obj in prev_selected:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = prev_active

            

         
            
         

        return {'FINISHED'}