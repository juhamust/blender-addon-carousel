bl_info = {
    "name": "Carousel",
    "author": "Juha Mustonen",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Create Tab",
    "description": "Create carousel",
    "warning": "",
    "category": "Add Object",
}

import bpy  # type: ignore
from carousel.carousel import OBJECT_OT_Carousel


def register():
    bpy.utils.register_class(OBJECT_OT_Carousel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Carousel)
