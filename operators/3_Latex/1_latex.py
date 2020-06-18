import bpy

from GeoBlender.utils.latex import import_latex

class LatexLabelLatex(bpy.types.Operator):
    """Enter Latex Expression (needs internet connection)"""   
    bl_idname = "add.latexlatex"            # Unique identifier.
    bl_label = "Latex Expression"           # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    text: bpy.props.StringProperty(name="Latex:", description="Latex Code (do not insert $)")

    scale_property: bpy.props.FloatProperty(
        name="Scale:",
        description="Scale of label",
        min=0.01,
        soft_max=10,
        default=1,
    )

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

        curve.scale *= self.scale_property

        bpy.ops.object.select_all(action='DESELECT')
        curve.select_set(True)
        bpy.context.view_layer.objects.active = curve
        bpy.context.object.active_material.roughness = 0

        curve.name = "Expression"
        curve.data.bevel_depth = 0 # Seems to work decent

        return {'FINISHED'}
