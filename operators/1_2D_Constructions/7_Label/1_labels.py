import bpy

from .latex_utils import import_latex
from GeoBlender.utils import drivers
from GeoBlender.utils.objects import move_origin_center


class LatexLabel(bpy.types.Operator):
    """Select an object and then enter a label (needs internet connection)"""
    bl_idname = "add.latex_label"  # Unique identifier.
    bl_label = "Label"           # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    text: bpy.props.StringProperty(name="Label:", description="Label text")

    scale_property: bpy.props.FloatProperty(
        name="Scale:",
        description="Scale of label",
        min=0.01,
        soft_max=10,
        default=1,
    )

    xlocation: bpy.props.FloatProperty(
        name="X location:",
        description="X location of label (relative to object)",
        min=-5,
        soft_max=5,
        default=1,
    )

    ylocation: bpy.props.FloatProperty(
        name="Y location:",
        description="Y location of label (relative to object)",
        min=-5,
        soft_max=5,
        default=-1,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 1 and
                context.object is not None)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    # execute() is called when running the operator.
    def execute(self, context):
        A = context.object

        # The original script
        curve = import_latex(self.text)

        if curve is None:
            # Error parsing LaTeX
            self.report({'ERROR'}, 'Invalid Latex Source')
            return {'CANCELLED'}

        curve.scale *= self.scale_property

        bpy.ops.object.select_all(action='DESELECT')
        curve.select_set(True)
        bpy.context.view_layer.objects.active = curve
        bpy.context.object.active_material.roughness = 0

        curve.parent = A
        curve.data.bevel_depth = 0  # Seems to work decent
        curve.location[0] = self.xlocation
        curve.location[1] = self.ylocation
        drivers.add_driver(curve, 'location', 'Z', expr="0.01")
        curve.name = "Label"

        return {'FINISHED'}
