'''
This should accept two objects A (active) and B.

1. It should set keyframes 0 at frame=1, 1 at frame=frame_end for the offset factor for
 follow path constraint on B (it must already pre-exist to 
work). *****DONE****

2. It should set a basic particles system for A (actually for a plane child of A)
 to track its trajectory (locus) from frame
1 to frame frame_end. Here are same important settings for A. 



Emmitter: Plane child of A.
hide viewport and render for plane
uncheck show emitter
display as: rendered (viewport display)
scale 1
scale randomness 0


Particle: a point (new point)
HIDE ORIGINAL point (simply hide render and viewport;particles will show)
Number= frame_end (1 per frame)
lifetime = frame_end+1
emit from face (hence the plane)
no physics
no gravity
no forces
no velocity
no random order


****
1. frame_end should be a local property (operator panel)
2. the operator should set the frame to frame_end so we can immediately see the result 
(not sure if blender will compute the full particle system)?
3. linear interpolation (uniform spacing)

'''