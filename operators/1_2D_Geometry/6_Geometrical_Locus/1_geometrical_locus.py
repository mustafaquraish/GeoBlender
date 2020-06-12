import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point
from GeoBlender.geometry.lines import segment


class Locus(bpy.types.Operator):
    bl_label = "Geometrical Locus"
    bl_idname = "geometry.locus"
    bl_description = ("Add the locus of a (free) point determined by the motion of another " 
                     "point (source) along a curve. Select two points. The free point "
                     "should be active")
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.


    frame_end: bpy.props.IntProperty(
        name="Frame end:",
        description="Last frame of motion of source point",
        min=0,
        soft_max=1000,
        default=150,
    )

    sphere_radius: bpy.props.FloatProperty(
        name="Radius of Particle:",
        description="Radius of particles for the locus",
        soft_min=0.01,
        soft_max=2,
        default=0.5,
    )

    part_number: bpy.props.IntProperty(
        name="Particles number:",
        description="Number of particles to create along locus",
        min=0,
        soft_max=1000,
        default=150,
    )

    @classmethod
    def poll(cls, context):
         return (len(context.selected_objects) == 2 and
                context.object is not None)

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        A = context.active_object
        others = context.selected_objects[-2:]
        others.remove(A)
        B = others[0]



        
        B.constraints["Follow Path"].offset_factor = 0
        B.constraints["Follow Path"].keyframe_insert(data_path='offset_factor', frame=1)

        B.constraints["Follow Path"].offset_factor = 1
        B.constraints["Follow Path"].keyframe_insert(data_path='offset_factor', 
                                                    frame=self.frame_end)
        fcurves = B.animation_data.action.fcurves
        for fcurve in fcurves:
            for kf in fcurve.keyframe_points:
                kf.interpolation = 'LINEAR'




        plane = new_plane(size=1, location=(0, 0, 0), hide=False)
        plane.parent = A
        

        particle = new_point(radius=self.sphere_radius)
        particle.name ="Particle"
        bpy.data.objects["Particle"].hide_render = True


        bpy.context.view_layer.objects.active = plane

        bpy.ops.object.particle_system_add()
        bpy.data.particles[-1].name = "Particles for locus"
        bpy.data.particles["Particles for locus"].type = 'EMITTER'
        bpy.data.particles["Particles for locus"].count = self.part_number
        bpy.data.particles["Particles for locus"].frame_start = 1
        bpy.data.particles["Particles for locus"].frame_end = self.frame_end
        bpy.data.particles["Particles for locus"].lifetime = self.frame_end + 1
        bpy.data.particles["Particles for locus"].lifetime_random = 0
        bpy.data.particles["Particles for locus"].emit_from = 'FACE'
        bpy.data.particles["Particles for locus"].distribution = 'JIT'
        bpy.data.particles["Particles for locus"].use_emit_random = False
        bpy.data.particles["Particles for locus"].userjit = 1
        bpy.data.particles["Particles for locus"].normal_factor = 0
        bpy.data.particles["Particles for locus"].physics_type = 'NEWTON'
        bpy.data.particles["Particles for locus"].render_type = 'OBJECT'
        bpy.data.particles["Particles for locus"].particle_size = 1
        bpy.data.particles["Particles for locus"].size_random = 0
        bpy.data.particles["Particles for locus"].effector_weights.gravity = 0
        bpy.data.particles["Particles for locus"].effector_weights.all = 0


        bpy.context.object.show_instancer_for_render = False
        bpy.data.particles["Particles for locus"].instance_object = bpy.data.objects["Particle"]
        bpy.context.object.show_instancer_for_viewport = False

        bpy.ops.ptcache.bake_all(bake=True)


        bpy.context.scene.frame_set(self.frame_end)
        bpy.context.scene.frame_end = self.frame_end      

        return {'FINISHED'}