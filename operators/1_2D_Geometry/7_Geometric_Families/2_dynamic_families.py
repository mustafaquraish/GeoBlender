import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, duplicate, add_to_collection
from GeoBlender.geometry.lines import segment


class StaticVariety(bpy.types.Operator):
    bl_label = "Dynamic family"
    bl_idname = "geometry.dynamic_family"
    bl_description = ("Dynamically adds still copies of a dependent object "
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

        for i in range(self.copies_number):

            frame_num = (1 + i * self.frame_gap)

            B.constraints["Follow Path"].offset_factor = i / self.copies_number
            B.constraints["Follow Path"].keyframe_insert(
                data_path='offset_factor',
                frame=frame_num
            )

            copy = duplicate(A, remove_all=True)
            add_to_collection(copy, "Dynamic Family")

            # Option to change bevel
            if (isinstance(copy.data, bpy.types.Curve)):
                add_abs_bevel(copy, self.bevel_depth)

            copy.hide_render = True
            copy.keyframe_insert(data_path='hide_render', frame=0)

            copy.hide_render = False
            copy.keyframe_insert(data_path='hide_render', frame=frame_num)

            if self.for_test:
                mat = bpy.data.materials.new(name=f"Test Material {i}")
                mat.use_nodes = True
                mat.blend_method = 'BLEND'
                mat_alpha = mat.node_tree.nodes["Principled BSDF"].inputs[18]

                mat_alpha.default_value = 0
                mat_alpha.keyframe_insert(data_path='default_value',
                                          frame=frame_num - 1)

                mat_alpha.default_value = 1
                mat_alpha.keyframe_insert(data_path='default_value',
                                          frame=frame_num)

                # Assign it to object
                if copy.data.materials:     # If material exists, replace
                    copy.data.materials[0] = mat
                else:                       # Otherwise create new one
                    copy.data.materials.append(mat)

        return {'FINISHED'}
