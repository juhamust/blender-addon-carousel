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
    from carousel import operators, panels
else:
    import importlib
    from carousel import operators, panels

    operators = importlib.reload(operators)
    panels = importlib.reload(panels)


def register():
    print("Register carousel addon")
    bpy.utils.register_class(operators.AddOperator)  # type: ignore
    bpy.utils.register_class(panels.CarouselPanel)  # type: ignore


def unregister():
    print("Unregister carousel addon")
    bpy.utils.unregister_class(operators.AddOperator)  # type: ignore
    bpy.utils.unregister_class(panels.CarouselPanel)  # type: ignore
