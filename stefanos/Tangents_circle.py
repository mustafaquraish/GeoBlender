def tangent_points_to_circle(tan1, tan2, A, C, hide_extra=True):
    # This function computes the tangent points tan1 and tan2 where the tangents
    # from a point A outside a cicle C intersect C

    circle_help = new_circle()
    circle_from_diameter(circle_help, A, B, hide_extra=True)

    # We next compute the intersection points of the two circles

    circle_circle_intersection(tan1, tan2, circle_help, C, hide_extra=True)


def tangent_lines_to_circle(line1, line2, A, C, hide_extra=True):

    # This function computes the tangent lines line1 and line2
    # from a point A outside a cicle C to the circle C

    tan1 = new_empty(hide=hide_extra)
    tan2 = new_empty(hide=hide_extra)

    tangent_points_to_circle(tan1, tan2, A, C)

    stretch_between_points(line1, A, tan1)
    stretch_between_points(line2, A, tan2)


def tangent_line_to_circle(line1, A, C, hide_extra=True):

    # This function computes the tangent line line1
    # from a point A on a cicle C to the circle C

    radius = new_line(hide=hide_extra)
    stretch_between_points(radius, A, C, axis='Z')
    orthogonal_line(A, radius, length)
