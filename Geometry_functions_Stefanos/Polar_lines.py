def polar(line, circle, A, hide_extra=True):
    '''
    This function constructs the polar of the point A (active)
    relative to the circle and returns it as the line argument.
    '''

    foot_polar = new_empty(hide=hide_extra)

    #we want (circle-foot)*(circle-A)=(radius)**2 and on the same ray.
    #after constructing this, we have then get the polar very easily
    #easy with drivers. construct the vector CircleA, normalize it and scale it. done.


    line1 = new_line(hide=hide_extra)
    segment(line1, circle, A)

    #? line = orthogonal_line(foot_polar, line1)