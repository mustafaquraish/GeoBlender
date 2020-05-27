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

    use_spheres: bpy.props.BoolProperty(
        name="Spheres for points:",
        description="Use (ico)spheres for points instead of empties",
        default=True,
        options={'HIDDEN'},
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.1,
        options={'HIDDEN'},
    )

    sphere_subdivisions: bpy.props.IntProperty(
        name="Subdivisions:",
        description="Subdivisions to use for the spheres for points",
        min=1,
        max=10,
        default=2,
        options={'HIDDEN'},
    )


class GeoBlenderMeasurements(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(
        name="Measured angle",
        description="Bevel depth for curves",
        default=0.0,
        options={'HIDDEN'},
    )
