# GeoBlender: A 3D geometry plugin for blender
---

The purpose of this plugin is to make it much easier to apply mathematical and geometric transformations on objects which are not easily done in Blender natively. Examples of such operations are:

- Creating a plane / circle that goes through any given 3 points
- Find circumcenter / barycenter / incenter / inscribed circle for a given triangle
- Bisectors, Medians, Midpoints (without drivers)
- and more to come in the future.

---

Along with this, here we develop a miniature framework to help write code to easily perform all of these geometric transformations, and provides a layer on top of Blender to remove a lot of the unnecessary boilerplate code needed to add constraints, drivers, etc. directly through Python.
