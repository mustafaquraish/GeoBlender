import bpy
from collections import defaultdict
from .operators import operator_list


###############################################################################


def operator_panel_factory(label, ops):
    '''
    Makes an additional GeoBlender panel with the given label and list of ops,
    and returns the class to be registered.
    '''

    id_name = "OBJECT_PT_geoblender_" + label.lower().replace(' ', '_')

    class OperatorPanel(bpy.types.Panel):
        bl_idname = id_name
        bl_label = label
        bl_category = "GeoBlender"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            layout = self.layout
            layout.use_property_split = True

            for op in ops:
                row = layout.row()
                row.operator(op.bl_idname)

    return OperatorPanel


###############################################################################


class GeoBlenderPropertiesPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_props"
    bl_label = "Default Properties"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.scene.geoblender_settings

        row = layout.row()
        row.prop(settings, 'hide_extra')

        row = layout.row()
        row.prop(settings, "plane_size", expand=True)

        row = layout.row()
        row.prop(settings, 'bevel_depth', expand=True)

        row = layout.row()
        row.prop(settings, 'collection_name', expand=True)


###############################################################################

class GeoBlenderMeasurePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_geoblender_measure"
    bl_label = "Measurements"
    bl_category = "GeoBlender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        measurements = context.scene.geoblender_measurements

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("geometry.measure_angle")
        row.prop(measurements, "angle", text="")


###############################################################################

panel_list = [GeoBlenderPropertiesPanel, GeoBlenderMeasurePanel]

###############################################################################

'''
Each Operator should have an attribute called `gb_panel` with the name of the
panel it should be added to. If this attribute isn't set, the operator is not
added to any panel (but can be accessed using F3).
'''

# Stores { 'panel name': [... panel operators ...] }
panel_dictionary = defaultdict(list)

for op in operator_list:
    try:
        panel_dictionary[op.gb_panel].append(op)

    # Do nothing if the `gb_panel` attribute is missing
    except AttributeError:
        pass

for panel_name, panel_ops in panel_dictionary.items():
    if panel_name is not None:
        panel_list.append(operator_panel_factory(panel_name, panel_ops))
