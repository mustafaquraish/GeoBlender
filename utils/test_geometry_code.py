from .constraints import copy_location
from .constraints import damped_track, locked_track
from .constraints import project_along_axis, project_nearest
from .drivers import add_driver, add_driver_distance
from .objects import new_empty, new_plane




# Next is code for line perpendicular to another line from a given point. from mustafa's altitude.
#modified to contain the case we are given a line and a point instead of three points.

def execute(self, context):

    if (len(context.selected_objects) == 3):

        (A, B, C) = context.selected_objects[-3:]
        active = context.active_object

        others = [A, B, C]
        others.remove(active)

        pr_plane = new_plane(hide=self.hide_extra)
        pr_plane.name = "projection plane"
        make_orthogonal_to(pr_plane, others[0], others[1], active, axis='Z')

        projection_point = new_empty()
        projection_point.name = "projection point"
        copy_location(projection_point, active)
        project_nearest(projection_point, target=pr_plane)

        return {'FINISHED'}


##in case we are given a line and a point. then we simply need to take two 
#different points on the line and repeat the above

    elif (len(context.selected_objects) == 2):

        line = context.selected_objects[-2:-1]
        point = context.selected_objects[-1:]
            
        online1 = new_empty(hide=hide_extra)
        online1.name = "online 1"

        online2 = new_empty(hide=hide_extra)
        online2.name = "online 2"

        position_on_curve(online1, line , position=0, influence=1)
        position_on_curve(online2, line , position=1, influence=1)

        pr_plane = new_plane(hide=self.hide_extra)
        pr_plane.name = "projection plane"
        make_orthogonal_to(pr_plane, online1, online2, point, axis='Z')
                
        projection_point = new_empty()
        projection_point.name = "projection point"
        copy_location(projection_point, point)
        project_nearest(projection_point, target=pr_plane)

        
        return {'FINISHED'}


#next things to do: tangent at a point on a circle. Line parallel to another line through a given point. 