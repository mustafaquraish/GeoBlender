import bpy

from .latex_utils import import_latex
from GeoBlender.utils import driver

class LatexLabel(bpy.types.Operator):
    """Enter Latex Expression"""          # Use this as a tooltip for menu items and buttons.
    bl_idname = "add.latex"            # Unique identifier for buttons and menu items to reference.
    bl_label = "Latex Expression"           # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    text: bpy.props.StringProperty(name="Latex:", description="Latex Code")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    # execute() is called when running the operator.
    def execute(self, context):
        # The original script
        curve = import_latex(self.text)

        if curve is None:
            # Error parsing LaTeX
            self.report({'ERROR'}, 'Invalid Latex Source')
            return {'CANCELLED'}

        curve.name = "Expression"
        curve.data.bevel_depth = 0.00002  # Seems to work decent

        return {'FINISHED'}
