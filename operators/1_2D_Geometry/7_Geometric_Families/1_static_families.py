import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, duplicate, add_to_collection
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

        for i in range(self.copies_number):

            B.constraints["Follow Path"].offset_factor = i / self.copies_number

            copy = duplicate(A, remove_all=True)
            add_to_collection(copy, "Static Family")

            # Option to change bevel
            if (isinstance(copy.data, bpy.types.Curve)):
                add_abs_bevel(copy, self.bevel_depth)

        return {'FINISHED'}
