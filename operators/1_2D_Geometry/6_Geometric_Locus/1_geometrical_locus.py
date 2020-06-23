import bpy
from GeoBlender.utils.objects import new_line, add_abs_bevel, new_plane
from GeoBlender.utils.objects import new_point, add_particle_system, set_hidden
from GeoBlender.geometry.lines import segment


class Locus(bpy.types.Operator):
    bl_label = "Geometrical locus"
    bl_idname = "geometry.locus"
    bl_description = ("Add the locus of a (free) point determined by the "
                      "motion of another point (source) along a curve. Select "
                      "two points. The free point should be active")
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

        follow_constraint = B.constraints["Follow Path"]

        follow_constraint.offset_factor = 0
        follow_constraint.keyframe_insert(data_path='offset_factor', frame=1)

        follow_constraint.offset_factor = 1
        follow_constraint.keyframe_insert(data_path='offset_factor',
                                          frame=self.frame_end)
        
        # Make sure the interpolation is linear
        fcurve = B.animation_data.action.fcurves[0]
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'

        # Create plane for particle system
        plane = new_plane(size=1, location=(0, 0, 0), hide=False)
        plane.show_instancer_for_render = False
        plane.show_instancer_for_viewport = False
        plane.parent = A

        # Create a point to be used as the instance object
        particle = new_point(radius=self.sphere_radius)
        particle.name = "Particle"
        particle.hide_render = True

        # Create and configure the particle system
        particle_system = add_particle_system(
            obj=plane,

            # The custom `add_particle_system` function takes in the settings
            name="Particles for locus",
            type='EMITTER',
            count=self.part_number,
            frame_start=1,
            frame_end=self.frame_end,
            lifetime=self.frame_end,
            lifetime_random=0,
            emit_from='FACE',
            distribution='JIT',
            use_emit_random=False,
            userjit=1,
            normal_factor=0,
            physics_type='NEWTON',
            render_type='OBJECT',
            particle_size=1,
            size_random=0,
            instance_object=particle
        )

        # These nested values can't be passed in as kwargs, so set manually
        particle_system.effector_weights.gravity = 0
        particle_system.effector_weights.all = 0

        bpy.ops.ptcache.bake_all(bake=True)

        context.scene.frame_set(self.frame_end)
        context.scene.frame_end = self.frame_end

        return {'FINISHED'}
