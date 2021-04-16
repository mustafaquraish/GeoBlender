import os
import bpy
import shutil
import requests
from pathlib import Path
from GeoBlender.utils import objects

HOMEDIR = str(Path.home())
SVGNAME = "_latexinput_temp.svg"
SVGPATH = os.path.join(HOMEDIR, SVGNAME)

COLLECTION_NAME = "Latex"


def latex2svg(latexcode):
    # url = "http://latex.codecogs.com/svg.latex?"
    url = "https://math.now.sh/"
    params = {
        'from': latexcode
    }
    request = requests.get(url, params=params)
    open(SVGPATH, 'wb').write(request.content)


def add_to_collection(obj):
    # Make a new collection for extra objects if needed.
    if COLLECTION_NAME not in bpy.data.collections:
        collection = bpy.data.collections.new(COLLECTION_NAME)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[COLLECTION_NAME]

    old_collections = obj.users_collection  # get old collection
    collection.objects.link(obj)    # put obj in extras collection
    for coll in old_collections:
        coll.objects.unlink(obj)    # unlink from old collection
        bpy.data.collections.remove(coll)  # Delete old collection


@objects.preserve_selection
def import_latex(latexcode):

    latex2svg(latexcode)

    start_objs = bpy.data.objects[:]
    bpy.ops.import_curve.svg(filepath=SVGPATH)
    new_curves = [o for o in bpy.data.objects if o not in start_objs]

    if new_curves == []:
        mc = bpy.data.collections.get(SVGNAME)
        bpy.data.collections.remove(mc)
        return None

    label = objects.join_objects(new_curves)
    add_to_collection(label)

    # Move the object to center of text, and move object to world origin
    objects.move_origin_center(label)
    label.location = (0, 0, 0)
    label.scale *= 2000

    # Select the object and apply the scale
    bpy.ops.object.select_all(action='DESELECT')
    label.select_set(True)
    bpy.context.view_layer.objects.active = label
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    return label


if __name__ == "__main__":
    latex2svg("f(x)")
