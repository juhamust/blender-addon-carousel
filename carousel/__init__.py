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

if "operator" not in locals():
    from carousel import operator, panel
else:
    import importlib
    from carousel import operator, panel

    operator = importlib.reload(operator)
    panel = importlib.reload(panel)


def register():
    print("Register carousel addon")
    bpy.utils.register_class(operator.AddOperator)  # type: ignore
    bpy.utils.register_class(panel.CarouselPanel)  # type: ignore


def unregister():
    print("Unregister carousel addon")
    bpy.utils.unregister_class(operator.AddOperator)  # type: ignore
    bpy.utils.unregister_class(panel.CarouselPanel)  # type: ignore
