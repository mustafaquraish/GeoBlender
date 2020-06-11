import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_polygon
from GeoBlender.utils.objects import new_point
from GeoBlender.geometry.lines import segment
from GeoBlender.utils.constraints import position_on_curve
from GeoBlender.utils.constraints import copy_location, copy_rotation
from GeoBlender.utils.drivers import add_driver


class Polygon(bpy.types.Operator):
    bl_label = "Polygon"
    bl_idname = "geometry.polygon"
    bl_description = ("Add a regular polygon with given center (point). "
                     " Select a point")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    

    sides_number: bpy.props.IntProperty(
        name="Number of sides:",
        description="Number of sides of the polygon",
        min=0,
        soft_max=20,
        default=3,
    )

    sides_length: bpy.props.FloatProperty(
        name="Length of sides:",
        description="Length of each side of the polygon",
        min=0,
        soft_max=20,
        default=2,
    )

    bevel_depth: bpy.props.FloatProperty(
        name="Bevel depth:",
        description="Thickness of the sides of the polygon",
        min=0,
        soft_max=0.5,
        default=0.2,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Sphere radius:",
        description="Radius of spheres drawn for points",
        soft_min=0.01,
        soft_max=2,
        default=0.3,
    )

    polygon_rotate: bpy.props.FloatProperty(
        name="Rotation:",
        description="Rotate the polygon around its center",
        soft_min=0,
        soft_max=360,
        default=0,
    )

    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) == 1)

    def invoke(self, context, event):
        self.bevel_depth = context.scene.geoblender_settings.bevel_depth
        self.sphere_radius = context.scene.geoblender_settings.sphere_radius
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        polygon = new_polygon(sides=self.sides_number,
                              length=self.sides_length,
                              hide=True)
        add_abs_bevel(polygon, self.bevel_depth)
        polygon.parent = A
        polygon.rotation_euler[2] = self.polygon_rotate

            
        
        vertices = []
        for i in range(int(self.sides_number)):
            s = new_point(radius=self.sphere_radius)
            position_on_curve(s, polygon, position=i / self.sides_number)
            add_driver(
                obj=s,
                prop='location',
                fields='Z',
                expr="0"
            )       
            vertices.append(s)

        for i in range(int(self.sides_number)-1):
            line = new_line()
            segment(line, vertices[i], vertices[i+1])
            add_abs_bevel(line, self.bevel_depth)
            line.name = "Side of polygon"

            line = new_line()
            segment(line, vertices[0], vertices[int(self.sides_number)-1])
            add_abs_bevel(line, self.bevel_depth)
            line.name = "Side of polygon"
            
            


        return {'FINISHED'}
