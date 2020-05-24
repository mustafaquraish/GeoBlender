import bpy


class GeoBlenderSettings(bpy.types.PropertyGroup):
    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed used by addon",
        default=True,
        options={'HIDDEN'},
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Bevel depth for curves",
        soft_min=0.0,
        soft_max=0.5,
        default=0.0,
        options={'HIDDEN'},
    )

    plane_size: bpy.props.FloatProperty(
        name="Plane size:",
        description="Size of planes used for intersection testing",
        soft_min=100,
        soft_max=1000,
        default=300,
        options={'HIDDEN'},
    )

    collection_name: bpy.props.StringProperty(
        name="Collection:",
        description="Extra objects needed for operators will be put here",
        default="GeoBlender Extras",
        options={'HIDDEN'},
    )


class GeoBlenderMeasurements(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(
        name="Measured angle",
        description="Bevel depth for curves",
        default=0.0,
        options={'HIDDEN'},
    )