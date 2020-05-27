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
    circle_of_inversion. The origin of the inversion should be
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


def inversion_cicle_not_on(inverted_circle, inverted_center, circle,
    circle_of_inversion, hide_extra = True):
    '''
    Places a circle (inverted_circle), with center the inverted_center, 
    to the inversion of a given circle (circle). The inversion is defined
    by the circle_of_inversion. The origin of the inversion should not be
    constrained on the circle. The active object is the circle_of_inversion. 
    '''
    connecting_line = new_line(hide=hide_extra)
    segment(connecting_line, circle_of_inversion, circle)

    inter1 = new_empty(hide=hide_extra)
    inter2 = new_empty(hide=hide_extra)
    line_circle_intersections(inter1, inter2, connecting_line, circle) 
    # inter1 and inter2 have the orientation of the circle

    inter1_inverted = new_empty(hide=hide_extra)
    inter2_inverted = new_empty(hide=hide_extra)

    inversion_point(inter1_inverted, inter1, circle_of_inversion)
    inversion_point(inter2_inverted, inter2, circle_of_inversion)

    circle_from_diameter(inverted_circle, inter1_inverted, inter2_inverted)
    midpoint(inverted_center, inter1_inverted, inter2_inverted)

    def inversion_line_on(inverted_line, line, circle_of_inversion,
        hide_extra = True):
        a_start = new_empty(hide=hide_extra)
        position_on_curve(a_start, line, 0)
        copy_rotation(a_start,circle_of_inversion)

        a_end = new_empty(hide=hide_extra)
        position_on_curve(a_end, line, 1)
        copy_rotation(a_end,circle_of_inversion)

        full_line(interted_line,a_start, a_end)
        '''
        Places a line (inverted_circle) to the inversion defined by the 
        circle_of_inversion. The origin of the inversion should be
        constrained on the line. The active object is the circle_of_inversion. 
        
        a_start = new_empty(hide=hide_extra)
        position_on_curve(a_start, line, 0)
        copy_rotation(a_start,circle_of_inversion)

        a_end = new_empty(hide=hide_extra)
        position_on_curve(a_end, line, 1)
        copy_rotation(a_end,circle_of_inversion)

        b_start = new_empty(hide=hide_extra)
        b_end = new_empty(hide=hide_extra)

        inversion_point(b_start, a_start, circle_of_inversion)
        inversion_point(b_end, a_end, circle_of_inversion)

        segment(inverted_line, b_start, b_end)

        #this construction works if the center of inversion is not between  a start and a end.
         if the center is between the line then the inversion is the full line
                if it is, then inversion is a full line!
        '''

    def inversion_line_not_on(inverted_line, line, circle_of_inversion
        hide_extra = True):
        '''
    Places a circle (inverted_line) to the inversion of a line (line) defined 
    by the circle_of_inversion. The origin of the inversion should not be
    constrained on the line. The active object is the circle_of_inversion. 
    '''
    proje = new_empty(hide=hide_extra)
    inverted_point = new_empty(hide=hide_extra)


    orthogonal_projection(proje, circle of inversion, line)
    inversion_point(inverted_point, proje, circle_of_inversion)
    circle_from_diameter(interted_line, circle_of_inversion, inverted_point)
   

        
    