import bpy
# from enum import Enum
from collections import defaultdict
from .operators import operator_list

'''
TODO: Add Enum support to make avoid new panels for typos...
Previous attempt commented out. Getting bl_rna errors.
'''


###############################################################################

'''
class PanelTypes(Enum):
    Constructions2D = '2D Constructions'
    Constructions3D = '2D Constructions'
    ConstructionsTriangle = 'Triangle Constructions'
    PlanarIntersections = 'Planar Intersections'
    Hidden = None       # This won't add the operator to any panel
'''

###############################################################################


def make_operator_panel(label, ops):
    '''
    Makes an additional GeoBlender panel with the given label and list of ops.
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


class GeoBlenderProperties(bpy.types.Panel):
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

panel_list = [GeoBlenderProperties]

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
        '''
        # If gb_panel is set as one of the predefined Panels
        if op.gb_panel in PanelTypes:
            panel_dictionary[op.gb_panel.value].append(op)
        else:
            raise Exception('GeoBlender Panel Type not recognized. Use one of '
                            'the predefined types or make your own in '
                            '`interface.py`')
        '''
    # Do nothing if the `gb_panel` attribute is missing
    except AttributeError:
        pass

for panel_name, panel_ops in panel_dictionary.items():
    if panel_name is not None:
        panel_list.append(make_operator_panel(panel_name, panel_ops))
