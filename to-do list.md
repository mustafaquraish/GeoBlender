***2D constructions***

>>>BASIC CONSTRUCTIONS

>>PLANE
add a plane (default XY plane for plane geometry.)

>>POINTS
add a point on the plane (clearly on the XY plane, so Z coordinate should be driven by 0)
        >>>Constrainted additions for points:
    Add a point on a line (say a point on the altitude. The point needs to be added on this line and must be constraint to move only on that line (like in geogebra; very important for dynamic constructions)
    Add a point on a circle (same as above)
    [easiest for the above is to have lines, rays, segments and circles defined as curves and then use the follow path constraint with fixed position on.]
add a point in 3D [we can also have an option for adding a point without the driver, or just leave it to the user to delete the driver]


>>LINES
add a segment
add a line
add a ray
create a triangle given three points (maybe with the option to include the angle arcs of its 3 angles)
add a vector AB, given the points A,B

>>CIRCLES
add a circle through 3 points
add a circle given the center point and another point (on the circle)
add a circle given the center point and the value for the radius (can it be the distance of two points-compass in geogebra, yes select two points which will give us the radius by simply driving the radius by the distance of the two selected points)
add a semicircle given the diameter
add a circular arc given the center, a point on the arc and the angle

>>ANGLES
add an angle arc for an angle BAC defined by three points A,B,C.
add an angle arc for an angle BAC given the points B, A, and the size of the angle (this should also create the point C and have as option whether we want the arc or not)

-----------------------------------------------------------------------------------

>>INTERSECTIONS (2D)

line with line (can be segments, rays, lines, intersection point does not have to be on the segment to be computed)
line and circle (0,1,2) points of intersection
circle and circle (0,1,2) points of intersection


------------------------------------------------------------------------------------

>>>SPECIAL CONSTRUCTIONS

>>Points
add the midpoint of two points (or of a segment)
add a point on a segment with given ration (inside/outside the segment)
add a point with given distance from a given point in a given direction (the direction should be given by a line) [can the distance be given by the user as the distance of two points in the scene? if not, then the use can do this operator on their own by the above constructions and intersections]
add projection of a point on a line (just the projection here)
--geometric locus is a very nice function, but not sure how to properly and pedagogically do it in blender: maybe we can just many many many vertices and then the curve connecting them (or only the vertices by sampling)--

>>Lines
add a line orthogonal to another line through a point
add a line parallel to another line through a point
add bisector of an angle
add perpendicular bisector of a segment


>>Circles
add tangents to a circle from a given point
add polar of a point to a circle
add radical axis of two circles
Apollonius circles (a whole panel; many cases, many solutions, but very interesting; circle tangential to three objects (points, lines, circles))

---------------------------------------------------------------------------------------

>>TRANSFORMATIONS (inputs of transformations, maybe to be given the option to transform multiple points at once, if possible)

>>>Translation (Origin Point, vector-distance,direction-)
Move a point a given distance in a given direction from a given point (already done above)

>>>Rotation (Center point, angle)
Rotate a point a given angle from a given center point

>>>Reflection (point or line)
Reflection of a point relative to another point
Reflection of a point relative to a line

>>> Homothesia (aka dilation) (Origin, ratio)
Dilate a point given the center and the signed ration 

>>> Inversion (Origin, power)
Invert a point relative to the center and the give (positive) power
Inversion of a full line (relative to a point on it, or not on it: two cases)
Inversion of a full circle (relative to a point on it, or not on it: two cases)
------------------------------------------------------------------------------------

>>MEASUREMENTS
measure length of a segment (there is an addon that gives the length of a curve in the UI so it should be possible to return results to the use in the UI)
measure the size of an angle
measure the area of a triangle


-----------------------------------------------------------------------------------

>>TEXT
labels
LaTeX

------------------------------------------------------------------------------------------





###############################################################################################

NOTES, REMARKS, FUTURE DIRECTIONS


maybe also ellipse and parabola and hyperbola, conics
and Their tangents (easy using align normal of shrinkrwrap; robust can be used for any curve)

3D constructions



