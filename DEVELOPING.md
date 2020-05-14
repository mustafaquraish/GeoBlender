# How to start with development on this add-on

1. Clone this repo locally.
    - If you're not familiar with the `git` command-line interface, download [GitHub Desktop](https://desktop.github.com/)
    - Log in and authenticate
    - File -> Clone Repository, select GeoBlender (or use: https://github.com/mustafaquraish/GeoBlender/)
    
2. Download [Visual Studio Code](https://code.visualstudio.com/) (**highly recommended**)

3. On the left side of Visual Studio Code, click the Extensions button (4 squares)

4. Search for 'Blender' and install the 'Blender Development' extension.
    - I also recommend installing the 'Python' extension to help with development.

5. Go to the VSCode Preferences (Settings), search for and enable the following options:
    - Blender: Allow Modify External Python
    - Blender > Addon: Reload on Save
    
6. Open the GeoBlender directory you cloned from Github in VSCode. (File -> Open)

7. Make sure Blender is closed first. Then, go to VSCode, Press `Ctrl+Shift+P`. Type in `Blender: Start` (or select it from the drop down) and press Enter.
    - The first time you run this it may prompt you to find the Blender executable file(s). Subsequent times, you will need to select it.
    - This is so that you can develop and test on multiple versions on Blender installed on your computer.

8. Blender should start up, and the add-on will be enabled if there were no errors in the code. 
    - Errors will show up in the terminal inside VSCode. Some may show up in the `Python Console` in Blender.
    - In VSCode terminal, gray messages = all good. Red messages = error.
    
9. Start working on the addon! Everytime you save, VSCode will save the file and re-start the add-on in Blender.
    - Make sure you look at the files `utils/constraints.py`, `utils/drivers.py`, `utils/geometry.py` and `utils/objects.py`.
    - An example of using drivers can be found in `operators/scratch.py`
    - Go over some of the operators in the directory and make sure you understand the general workflow of how everything is set up

10. When you make a new operator (in a new file in the `operators` directory), here's what you need to make sure you do:
    - If you've copied another operator as a template, make sure you change the class name and `bl_idname`, `bl_label`, ...
    - If you don't want to deal with manual imports of each function, you can start off with:
        ```python
        from ..utils.objects import *
        from ..utils.constraints import *
        from ..utils.geometry import *
        from ..utils.drivers import *
        ```
       to import everything, even though I highly recommend it and will need to be fixed eventually.
    - Go to `__init__.py` and import the class you made. It will look like:
        ```
        from .operators.FILENAME.py import OPERATORCLASSNAME
        ```
        use the existing imports as an example.
    - Add the same line to `interface.py` at the top.
    - Finally, in `interface.py`, find the correct panel's class in which you want to insert the operator, and then add the name of the class into the `operators` list inside it. For example, if `OPERATORCLASSNAME` should be added in the `2D Constructions` Panel:
        ```python
        class GeoBlender2DConstructions(bpy.types.Panel):
            bl_idname = "OBJECT_PT_geoblender_2d_construtions"
            bl_label = "2D Constructions"
            bl_category = "GeoBlender"
            bl_space_type = "VIEW_3D"
            bl_region_type = "UI"
            bl_options = {'DEFAULT_CLOSED'}

            def draw(self, context):
                layout = self.layout
                layout.use_property_split = True

                operators = [
                    CreateInscribedCircle,
                    EmptyAtCircumcenter,
                    CreateRadicalAxis,
                    CreateCircumcircle,
                    CreateEulerCircle,
                    CreateEulerLine,
                    CreateLineSegment,
                    CreateLine,
                    ReflectAboutPoint,
                    
                    OPERATORCLASSNAME,  <<<<< # THIS IS WHAT YOU SHOULD ADD
                ]

                for op in operators:
                    row = layout.row()
                    row.operator(op.bl_idname)
        ```

11. Your operator should now be available in the corresponding panel in Blender.
