# GeoBlender: A 3D geometry plugin for Blender
---

<img src="https://imgur.com/QbJPH2R.jpg" width="250" height="250"/>

The purpose of this plugin is to make it much easier to apply mathematical and geometric transformations on objects which are not easily done in Blender natively. Examples of such operations are:

- Creating a plane / circle that goes through any given 3 points
- Finding circumcenters / barycenters / incenters / inscribed circles for given triangles
- Bisectors, Medians, Midpoints, Altitudes 
- and more to come in the future.

---

## Backlog

### Design / interface:
- Documentation
- Add driver to `bevel_depth` for curves to divide by current scale
- Figure out how to do imports in a nicer way in `__init__.py` and `interface.py` to comply with PEP8. Possible fix to this is to add a `register()` and `unregister()` function to the `.py` files for each of the individual operators. This would make the imports cleaner.
    - This is what Blender's default add-ons seem to do, so likely a good design choice and worth investing some time to do it eventually.
    - Also probably split `interface.py` into multiple files for each of the panels. It's getting really messy... Maybe even automate it.

### Operators:
- Dynamic arc between lines to denote angle
- If possible, ellipse through focii and curve point
- Parallel line through point

---

## How to use

- Click *Clone or Download* above on the right, and then *Download ZIP*
- In Blender, go to *Edit > Preferences > Add-ons > Install...*, and then select the downloaded zip file. 
- If it is not already, enable the GeoBlender add-on
- A *GeoBlender* panel should now be available in the panels section of the right side of the viewport. Alternatively, press F3 to search for the operators needed.

---

Along with this, here we develop a miniature framework to help write code to easily perform all of these geometric transformations, and provides a layer on top of Blender to remove a lot of the unnecessary boilerplate code needed to add constraints, drivers, etc. directly through Python.
