mid1 = objects.new_point(hide=hide_extra)
mid2 = objects.new_point(hide=hide_extra)
lines.midpoint(mid1, B, C)
lines.midpoint(mid2, A, B)

pr_plane = objects.new_plane(hide=hide_extra)
core.make_orthogonal_to(pr_plane, mid1, A, B)

constraints.copy_transforms(point, C, transforms='LR')
constraints.locked_track(point, lock='Z', axis='X', target=mid2)
constraints.project_along_axis(
    obj=point, 
    axis='X', 
    target=pr_plane, 
    opposite=True
)

# --------------------------------------------------------------------------- #
#                       ALTITUDE, ORTHOCENTER                                 #
# --------------------------------------------------------------------------- #