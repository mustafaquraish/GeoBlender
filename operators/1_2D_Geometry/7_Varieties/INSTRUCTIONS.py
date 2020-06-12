'''
This should accept two objects A (active, varient) and a point B(follow path).


Let n be the numbers of snapshots to create.

1. B should be already constrained on a curve. Make its offset_factor take n uniform values

2. For each of the values in B, we need to create a (live) copy of A and apply visual transform
and remove all drivers and constraints. And put these copies in a separate new collection. Given
the bevel option for the new copies:

# Option to change bevel
if (isinstance(A.data, bpy.types.Curve)):
    add_abs_bevel(dupli_A, self.bevel_depth)



'''