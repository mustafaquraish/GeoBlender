# Before we can invert points, lines and circles, the user will have to 
# introduce the circle_of_inversion. The origin of this circle is the origin
# of inversion and the squared of the radius is the power of the inversion.

def inversion_point(inverted_point, point,
    circle_of_inversion, hide_extra = True):
    '''
    Places a point (inverted_point) to the inversion defined by the 
    circle_of_inversion (see also comments above). The active object 
    is the circle_of_inversion.
    '''
    copy_rotation(inverted_point, point)
    add_driver(
        obj=inverted_point,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('transform', circle_of_inversion, 'scale', 'X'),
            'r': ('distance', point, circle_of_inversion),
            'o1': ('transform', circle_of_inversion, 'location', '-'),
            'o2': ('transform', point, 'location', '-'),
        },
        expr='gb_inversion_expres(d, r, o1, o2)'
    )


def inversion_cicle_yes_on(inverted_circle, circle,
    circle_of_inversion, hide_extra = True):
    '''
    Places a line (inverted_circle) to the inversion defined by the 
    circle_of_inversion The origin of the inversion should be
    constrained on the circle. The active object is the circle_of_inversion. 
    '''
    connecting_line = new_line(hide=hide_extra)
    segment(connecting_line, circle_of_inversion, circle)

    inversion_inter = new_empty(hide=hide_extra)
    copy_rotation(inversion_inter, circle_of_inversion)

    antipodal = new_empty(hide=hide_extra)
    add_driver(
            obj=antipodal,
            prop='location',
            fields='XYZ',
            vars_def={
                'o': ('transform', circle_of_inversion, 'location', '-'),
                'a': ('transform', circle, 'location', '-'),
            },
            expr='o + (a-o)*2'
        )

    add_driver(
        obj=inversion_inter,
        prop='location',
        fields='XYZ',
        vars_def={
            'd': ('transform', circle_of_inversion, 'scale', 'X'),
            'r': ('transform', circle, 'scale', 'X'),
            'o1': ('transform', circle_of_inversion, 'location', '-'),
            'o2': ('transform', antipodal, 'location', '-'),
        },
        expr='gb_inversion_expres(d, r, o1, o2)'
    )
    orthogonal_line(inverted_circle, inversion_inter, connecting_line)


def inversion_cicle_not_on(inverted_circle, circle,
    circle_of_inversion, hide_extra = True):
    '''
    Places a circle (inverted_circle) to the inversion the inversion defined
    by the circle_of_inversion. The origin of the inversion should not be
    constrained on the circle. The active object is the circle_of_inversion. 
    '''
1. find connecting line
2. find two intersections of 1 with circle_of_inversion
3. apply inversion of these two points.
4. obtain the circle of diameter the above points. 

FINISH FUNCTION!!!!!!!!!