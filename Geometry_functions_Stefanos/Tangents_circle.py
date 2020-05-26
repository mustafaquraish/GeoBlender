


def tangent_points(tan1, tan2, A, C, hide_extra=True):
    # This function computes the tangent points tan1 and tan2 where the tangents
    # from a point A outside a cicle C intersect C

    circle_help= new_circle()
    circle_from_diameter(circle_help, A, B, hide_extra=True)

    # We next compute the intersection points of the two circles

    circle_circle_intersection(tan1, tan2, circle_help, C, hide_extra=True)

    tangent1 = new_line()
    stretch_between_points(tangent1, A, tan1)
    add_abs_bevel(tangent1, bevel_depth)

    tangent2 = new_line()
    stretch_between_points(tangent2, A, tan2)
    add_abs_bevel(tangent1, bevel_depth)



def tangent_lines(line1, line2, A, C, hide_extra=True):

    # This function computes the tangent lines line1 and line2 
    # from a point A outside a cicle C to the circle C

    tan1=new_empty(hide=hide_extra)
    tan2=new_empty(hide=hide_extra)

    tangent_points(tan1, tan2, A, C):

    stretch_between_points(line1, A, tan1)
    # add_abs_bevel(tangent1, bevel_depth) ##needed here?##

    stretch_between_points(line2, A, tan2)
    # add_abs_bevel(tangent1, bevel_depth)


def tangent_line(line1, A, C, hide_extra=True):

    # This function computes the tangent line line1  
    # from a point A on a cicle C to the circle C

    radius = new_line(hide=hide_extra)
    stretch_between_points(radius, A, C, axis='Z')

    orthogonal_line(A, radius, length)