
# The next function computes the tangent points tan1 and tan2 where the tangents
# from a point A outside a cicle C intersect C

def tangent_points(tan1, tan2, A, C):

    circle_help= new_circle()
    circle_from_diameter(circle_help, A, B, hide_extra=True)

    # We next compute the intersection points of the two circles

    circle_circle_intersection(tan1, tan2, circle_help, C, hide_extra=True)

    tangent1 = new_line()
    stretch_between_points(tangent1, A, tan1)
    add_abs_bevel(tangent1, self.bevel_depth)

    tangent2 = new_line()
    stretch_between_points(tangent2, A, tan2)
    add_abs_bevel(tangent1, self.bevel_depth)


# The next function computes the tangent lines line1 and line2 
# from a point A outside a cicle C to the circle C

def tangent_lines(line1, line2, A, C):

    tan1=new_empty(hide=hide_extra)
    tan2=new_empty(hide=hide_extra)

    tangent_points(tan1, tan2, A, C):

    tangent1 = new_line()
    stretch_between_points(tangent1, A, tan1)
    add_abs_bevel(tangent1, bevel_depth)

    tangent2 = new_line()
    stretch_between_points(tangent2, A, tan2)
    add_abs_bevel(tangent1, bevel_depth)