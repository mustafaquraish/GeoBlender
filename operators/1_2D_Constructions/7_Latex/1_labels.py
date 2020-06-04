import bpy

from .latex_utils import import_latex
from GeoBlender.utils import drivers


class LatexLabel(bpy.types.Operator):
    """Enter Latex Label"""          # Use this as a tooltip for menu items and buttons.
    bl_idname = "add.latex_label"            # Unique identifier for buttons and menu items to reference.
    bl_label = "Latex Label"           # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    text: bpy.props.StringProperty(name="Latex:", description="Label text")

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

        curve.parent = A
        curve.data.bevel_depth = 0.00002  # Seems to work decent
        drivers.add_driver(curve, 'location', 'Z', expr="0.01")
        curve.name = "Label"

        return {'FINISHED'}
