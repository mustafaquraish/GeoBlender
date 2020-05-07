import bpy
from ..utils.objects import *
from ..utils.geometry import *
from ..utils.drivers import add_driver
from ..utils.constraints import *

class Scratch(bpy.types.Operator):
    bl_label = "Scratch Operator"
    bl_idname = "geometry.scratch_test"
    bl_description = "Add an empty in the middle of objects"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    hide: bpy.props.BoolProperty(
        name="Hide:", 
        description="hide", 
        default=True,
    )

    def execute(self, context):
        
        if (len(context.selected_objects) != 3):
            return {'CANCELLED'}

        (A, B, C) = context.selected_objects[-3:]
        add_driver(
            obj=A,
            prop='scale',
            fields='XZ',
            vars_def={
                'x': (B, 'scale', 'X'),
                'y': (B, 'scale', 'Y'),
                'z': (C, 'rotation', 'W'),
                'c': (C, 'location', '-')
            },
            expr='sqrt(x**2 + y**2) + z'
        )

        return {'FINISHED'}
