import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, duplicate, add_to_collection
from GeoBlender.geometry.lines import segment


class StaticVariety(bpy.types.Operator):
    bl_label = "Locus Curve"
    bl_idname = "geometry.locus_curve"
    bl_description = ("Add the a curve representing the locus of a free point "
                      "determined by the motion of another point (source) "
                      "along a curve. Select two points. The free point "
                      "should be active")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    frame_start: bpy.props.IntProperty(
        name="Start frame:",
        description="Frame from which the locus curve starts",
        min=0,
        soft_max=1000,
        default=0,
    )

    frame_end: bpy.props.IntProperty(
        name="End frame:",
        description="Frame from which the locus curve ends",
        min=1,
        soft_max=1000,
        default=10,
    )

    resolution: bpy.props.IntProperty(
        name="Vertices:",
        description="Resolution of the curve",
        min=3,
        soft_max=200,
        default=100,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of the copies (if curves)",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    vector_handles: bpy.props.BoolProperty(
        name="Use vector handles:",
        description="Use vector handles for bezier points instead of auto",
        default=False
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

        num_verts = self.resolution
        prev_offset = B.constraints["Follow Path"].offset_factor

        path = bpy.data.curves.new('path', 'CURVE')
        curve = bpy.data.objects.new('Locus Curve', path)
        context.collection.objects.link(curve)
        path.dimensions = '3D'
        spline = path.splines.new('BEZIER')
        spline.bezier_points.add(num_verts)

        handle_type = 'VECTOR' if self.vector_handles else 'AUTO'

        for i, o in enumerate(spline.bezier_points):
            B.constraints["Follow Path"].offset_factor = i / num_verts
            bpy.context.view_layer.update()

            o.co = A.matrix_world.to_translation()

            o.handle_right_type = handle_type
            o.handle_left_type = handle_type

        B.constraints["Follow Path"].offset_factor = prev_offset
        bpy.context.view_layer.update()

        add_abs_bevel(curve, self.bevel_depth)

        # Set keyframes for the start
        # ---------------------------
        curve.data.bevel_factor_end = 0
        curve.data.keyframe_insert(data_path='bevel_factor_end',
                                   frame=self.frame_start)
        B.constraints["Follow Path"].offset_factor = 0
        B.constraints["Follow Path"].keyframe_insert(
            data_path='offset_factor',
            frame=self.frame_start
        )

        curve.data.bevel_factor_end = 1
        curve.data.keyframe_insert(data_path='bevel_factor_end',
                                   frame=self.frame_end)
        B.constraints["Follow Path"].offset_factor = 1
        B.constraints["Follow Path"].keyframe_insert(
            data_path='offset_factor',
            frame=self.frame_end
        )
        return {'FINISHED'}
