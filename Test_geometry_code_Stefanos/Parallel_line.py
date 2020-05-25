# create function for the projection operator, then use it to get the parallel. 
# care must be taken in case the altitude code of mustafa is such that the point is ON the line. in that case
#it is not unique, but rather we need a plane. Since the axis of the line is the Z axis, then we can very 
#easily get that plane by simply copies the rotation. for the stretch function of mustafa maybe we should not 
#just do damped track but also track the Z axis to make sure it has the correct orientation relative to the plane
#(say the X axis of the curve is on the plane). 