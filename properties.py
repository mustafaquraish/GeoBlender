import bpy


class GeoBlenderSettings(bpy.types.PropertyGroup):
    hide_extra: bpy.props.BoolProperty(
        name="Hide Extra Objects:",
        description="Hide extra objects needed used by addon",
        default=True,
        options={'HIDDEN'},
    )

    shade_smooth: bpy.props.BoolProperty(
        name="Shade Smooth:",
        description="Shade objects smooth",
        default=True,
        options={'HIDDEN'},
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth:",
        description="Thickness of curves",
        soft_min=0.0,
        soft_max=0.5,
        default=0.2,
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

    length: bpy.props.FloatProperty(
        name="Length:",
        description="Length of lines",
        min=0,
        soft_max=300,
        default=100,
    )

    circle_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of sphere",
        soft_min=0.01,
        soft_max=200,
        default=5,
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
        description="Use spheres for points instead of empties",
        default=True,
        options={'HIDDEN'},
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
        options={'HIDDEN'},
    )

    sphere_subdivisions: bpy.props.IntProperty(
        name="Segments:",
        description="Segments to use for the spheres for points",
        min=1,
        max=100,
        default=32,
        options={'HIDDEN'},
    )


class GeoBlenderMeasurements(bpy.types.PropertyGroup):
    
    length: bpy.props.FloatProperty(
        name="Length",
        description="Length measurement",
        default=0.0,
        options={'HIDDEN'},
    )

    angle: bpy.props.FloatProperty(
        name="Angle",
        description="Angle measurement",
        default=0.0,
        options={'HIDDEN'},
    )

    area: bpy.props.FloatProperty(
        name="Area",
        description="Area measurement",
        default=0.0,
        options={'HIDDEN'},
    )

    radius: bpy.props.FloatProperty(
        name="Radius",
        description="Radius measurement",
        default=0.0,
        options={'HIDDEN'},
    )
