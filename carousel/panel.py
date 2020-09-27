import bpy  # type: ignore
from bpy.types import Panel  # type: ignore


class CarouselPanel(Panel):
    bl_idname = "carousel_panel"
    bl_label = "Carousel"
    bl_context = "objectmode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Create"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        print("test", scene)

        row = layout.row()
        row.operator("object.carousel_add", text="Carousel add")
