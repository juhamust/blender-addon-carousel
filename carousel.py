"""
Module for creating carousel of meshes
"""
import math
import random
from typing import Any, Dict, List, Set
import bpy  # type: ignore

try:
    from typing import TypedDict  # >=3.8
except ImportError:
    TypedDict = lambda *args, **kwargs: Any

C = bpy.context
D = bpy.data
O = bpy.ops

bl_info = {
    "name": "Carousel",
    "author": "Juha Mustonen",
    "description": "Generate carousel",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "Operator search",
    "warning": "",
    "category": "Mesh",
}

CarouselParent = TypedDict(
    "CarouselParent",
    {
        "name": str,
    },
)

CarouselChild = TypedDict(
    "CarouselChild",
    {
        "name": str,
    },
)

Carousel = TypedDict(
    "Carousel",
    {"parent": CarouselParent, "children": List[CarouselChild]},
)


AnimStep = TypedDict(
    "AnimStep",
    {
        "frame": int,
        "angle": float,
    },
)

BluePrint = TypedDict("BluePrint", {"name": str, "animation_steps": List[AnimStep]})


class CarouselOperator(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "mesh.carousel"
    bl_label = "Carousel Operator"
    bl_description = "Generate carousel"

    object_type: bpy.props.EnumProperty(
        items=[
            ("cube", "Cube", "Simple cube"),
            ("grease", "Grease", "Grease pane"),
        ],
        name="Object type",
        description="",
        default="cube",
    )

    object_count: bpy.props.IntProperty(
        name="Objects",
        description="Object count",
        default=8,
        min=1,
        soft_max=10,
    )

    circle_radius: bpy.props.IntProperty(
        name="Radius",
        description="Circle radius",
        default=8,
        min=1,
        soft_max=5,
    )

    circle_count: bpy.props.IntProperty(
        name="Count",
        description="Circle count",
        default=1,
        min=1,
        soft_max=50,
    )

    def get_object_location(self, radius=10, angle=0, z=0):
        """
        Returns the object location on circle
        """
        return (
            radius * math.sin(math.radians(angle)),
            radius * math.cos(math.radians(angle)),
            z,
        )

    def generate_carousel(
        self, name: str, object_count: int = 10, radius: int = 10, z: int = 0
    ) -> Carousel:
        """
        Generate circle with objects
        """
        parent_name = f"{name}-parent"
        carousel: Carousel = {"parent": {"name": parent_name}, "children": []}

        # Create collection and add it to scene
        coll = D.collections.new(name=name)
        C.scene.collection.children.link(coll)

        # Create parent, name it and put into collection
        O.mesh.primitive_cube_add(size=1, align="WORLD", location=(0, 0, z))
        parent = C.active_object
        parent.name = parent_name
        coll.objects.link(parent)
        self._unlink_world(parent)

        # Create object in full circle
        for o in range(object_count):
            # Get item location and angle on the circle
            angle = (360 / object_count) * o
            location = self.get_object_location(radius=radius, angle=angle, z=z)

            # Dynamically call the add function
            getattr(self, f"_add_{self.object_type}")(location, math.radians(angle))
            obj = C.active_object
            obj.name = f"{name}-child-{o}"

            # Put object into custom collection and remove from scene collection
            coll.objects.link(obj)
            self._unlink_world(obj)
            obj.parent = parent

        return carousel

    def animate_carousel(
        self, carousel: Carousel, animation_steps: List[AnimStep]
    ) -> None:
        C.view_layer.objects.active = None

        parent = D.objects[carousel["parent"]["name"]]
        parent.select_set(True)
        C.view_layer.objects.active = parent

        override = C.copy()
        override["active_object"] = parent
        override["selected_objects"] = [parent]

        steps_info = [f"{step['frame']} / {step['angle']}" for step in animation_steps]
        self.log(f"STEPS: {', '.join(steps_info)}")

        for step in animation_steps:
            self.report({"INFO"}, f"Add step {step['frame']}")
            C.scene.frame_set(step["frame"])
            parent.rotation_euler = (0, 0, math.radians(step["angle"]))
            O.anim.keyframe_insert_menu(override, type="Rotation")

    def invoke(self, context, event):
        return self.execute(context)

    def execute(self, context):
        """
        Addons entrypoint
        """
        self.log(f"Generating {self.circle_count} circles")

        blueprints: List[BluePrint] = [
            {
                "name": "Carousel-1",
                "animation_steps": self._get_steps(self.object_count),
            },
            {
                "name": "Carousel-2",
                "animation_steps": self._get_steps(self.object_count),
            },
            {
                "name": "Carousel-3",
                "animation_steps": self._get_steps(self.object_count),
            },
        ]

        for num, blueprint in enumerate(blueprints):
            carousel = self.generate_carousel(
                blueprint["name"],
                object_count=self.object_count,
                radius=self.circle_radius,
                z=num + 1,
            )
            self.animate_carousel(carousel, blueprint["animation_steps"])

        return {"FINISHED"}

    def log(self, msg: str, level: str = "info") -> None:
        set_level: Set[str] = {level.upper()}
        self.report(set_level, msg)

    def _unlink_world(self, object):
        try:
            D.scenes["Scene"].collection.objects.unlink(object)
        except:
            pass

    def _get_steps(self, object_count: int) -> List[AnimStep]:
        steps: List[AnimStep] = []
        # Generate object indexes in random order
        indexes: List[int] = list(range(object_count))
        random.shuffle(indexes)
        step_size = 20
        one_angle = 360.0 / object_count

        for num, index in enumerate(indexes):
            steps.append(
                {
                    "frame": num * step_size,
                    "angle": index * one_angle,
                }
            )

        return steps

    def _add_cube(self, location, angle):
        O.mesh.primitive_cube_add(
            size=2,
            enter_editmode=False,
            align="WORLD",
            location=location,
            rotation=(0, 0, -angle),
        )

    def _add_grease(self, location, angle):
        O.object.gpencil_add(
            align="WORLD",
            location=location,
            scale=(1, 1, 1),
            rotation=(0, 0, -angle),
            type="EMPTY",
        )


def register():
    bpy.utils.register_class(CarouselOperator)


def unregister():
    bpy.utils.unregister_class(CarouselOperator)
