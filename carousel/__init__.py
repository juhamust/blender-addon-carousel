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


if "bpy" in locals():
    import importlib
    import carousel

    importlib.reload(carousel)
else:
    from carousel.operator import AddOperator
    from carousel.panel import CarouselPanel

import bpy  # type: ignore


def register():
    bpy.utils.register_class(AddOperator)
    bpy.utils.register_class(CarouselPanel)


def unregister():
    bpy.utils.unregister_class(AddOperator)
    bpy.utils.unregister_class(CarouselPanel)
