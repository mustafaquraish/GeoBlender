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
    - Add a field called `gb_panel` with a string representing the name of the Panel it should be added to. If a panel with this name doesn't already exist it will be created. If this is not done, it will not be added to any panel.
    ```python
    class YourOperator(bpy.types.Operator):
        ...
        gb_panel = 'Triangle Constructions'    
        ...
    ```
    - Add a `poll()` method:
    ```python
    class YourOperator(bpy.types.Operator):
        ...

        @classmethod
        def poll(cls, context):
            ...
            return (True / False)
        
        ...
    ```
    This method essentially checks the selected objects through `context` to see if this operator can be run or not. It is responsible for enabling and disabling the button in the panel.
11. Your operator should now be available in the corresponding panel in Blender.
