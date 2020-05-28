import bpy
from collections import defaultdict
from .operators import operator_list


'''
Each Operator should have an attribute called `gb_panel` with the name of the
panel it should be added to. If this attribute isn't set, the operator is not
added to any panel (but can be accessed using F3).
'''


###############################################################################


def operator_panel_factory(label, panel_dict, parent=None):
    '''
    Makes an additional GeoBlender panel with the given label and list of ops,
    and returns the class to be registered. If we want the new panel to be
    a sub-panel of a parent, it must be passed in.
    '''

    class_name = label.lower().replace(' ', '_')

    class OperatorPanel(bpy.types.Panel):
        if parent is not None:
            bl_parent_id = parent.bl_idname
            bl_idname = f"{parent.bl_idname}_{class_name}"
        else:
            bl_idname = f"OBJECT_PT_geoblender_{class_name}"

        bl_label = label
        bl_category = "GeoBlender"
        bl_space_type = "VIEW_3D"
        bl_region_type = "UI"
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            layout = self.layout
            layout.use_property_split = True

            for op in panel_dict['operators']:
                row = layout.row()
                row.operator(op.bl_idname)

    created_panels = [OperatorPanel]
    for subpanel_name, subpanel_dict in panel_dict['subpanels'].items():
        new_subpanels = operator_panel_factory(
            subpanel_name,
            subpanel_dict,
            parent=OperatorPanel
        )
        created_panels += new_subpanels

    return created_panels


###############################################################################


class GeoBlenderPropertiesPanel(bpy.types.Panel):
    '''
    This panel stores the Default properties for the operators. When making a
    new operator, these values are used by default for the local operator
    properties. This panel also allows you to choose the default collection
    for the extra object created by the addon.
    '''
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

        layout.row().separator()

        row = layout.row()
        row.prop(settings, 'use_spheres', expand=True)

        if settings.use_spheres:
            row = layout.row()
            row.prop(settings, 'sphere_radius', expand=True)

            row = layout.row()
            row.prop(settings, 'sphere_subdivisions', expand=True)


###############################################################################

class GeoBlenderMeasurePanel(bpy.types.Panel):
    '''
    This panel is to allow measurements and display their values at the point
    of measurement in the UI itself. This will need to be changed manually
    to add more measurement operators.
    '''
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
This structure below is best explained by an example. For instance, the
following menu structure:

            -> 2D Constructions
                -> Circle Constructions
                    - Create Inscribed Circle Operator
                    - Create Euler Circle Operator
            -> 3D Constructions
                - Plane through Points Operator

will be represented in the top level dictionary (below) as follows:

            top_level_panel_dict = {
                'operators' = [],
                'subpanels' = {
                    '2D Constructions': {
                        'operators' = [],
                        'subpanels' = {
                            'Circle Constructions': {
                                'operators' = [ CreateInscribedCircle,
                                                CreateEulerCircle,
                                            ],
                                'subpanels' = {}
                            }
                        }
                    },
                    '3D Constructions': {
                        'operators' = [ PlaneThroughPoints ],
                        'subpanels' = {}
                    }
                }
            }
'''

# Start off with a default dictionary containing no operators or panels
top_level_panel_dict = {
    'operators': [],
    'subpanels': {}
}

for op in operator_list:
    try:
        # Get a list containing the panel hierarchy for the operator
        panel_loc = op.gb_panel
        panel_hierarchy = panel_loc.split(">")
        panel_hierarchy = [p.strip() for p in panel_hierarchy]

        # Find the correct subpanel dict to actually insert the operator
        current_dict = top_level_panel_dict
        for panel_name in panel_hierarchy:
            if panel_name not in current_dict['subpanels']:
                current_dict['subpanels'][panel_name] = {}
                current_dict['subpanels'][panel_name]['operators'] = []
                current_dict['subpanels'][panel_name]['subpanels'] = {}
            current_dict = current_dict['subpanels'][panel_name]

        # Add the op. to the relevant subpanel's operator list
        current_dict['operators'].append(op)

    # Do nothing if the `gb_panel` attribute is missing
    except AttributeError:
        pass


for panel_name, panel_dict in top_level_panel_dict['subpanels'].items():
    panel_list += operator_panel_factory(panel_name, panel_dict)
