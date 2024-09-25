import bpy
from math import radians
from helix2 import create_and_animate_circles


# Panel UI Class
class CreateAndAnimateCirclesPanel(bpy.types.Panel):
    bl_label = "Create and Animate Circles"
    bl_idname = "VIEW3D_PT_create_and_animate_circles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helical Bridge'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.create_and_animate_circles_props

        # Add input fields for each property
        layout.prop(props, "circle_1_location")
        layout.prop(props, "circle_2_location")
        layout.prop(props, "screw_angle")
        layout.prop(props, "screw_offset")
        layout.prop(props, "animation_frame_start")
        layout.prop(props, "animation_frame_end")
        layout.prop(props, "final_location")
        layout.prop(props, "final_rotation")
        layout.prop(props, "scale_factor")

        # Add the button to execute the operator
        layout.operator("wm.create_and_animate_circles", text="Create and Animate")


# Property Group Class
class CreateAndAnimateCirclesProperties(bpy.types.PropertyGroup):
    circle_1_location: bpy.props.FloatVectorProperty(
        name="Circle 1 Location",
        description="Location of the first circle",
        default=(-2, 0, 0),
        subtype='XYZ'
        )

    circle_2_location: bpy.props.FloatVectorProperty(
        name="Circle 2 Location",
        description="Location of the second circle",
        default=(2, 0, 0),
        subtype='XYZ'
        )

    screw_angle: bpy.props.FloatProperty(
        name="Screw Angle",
        description="Angle for the screw modifier in degrees",
        default=30,
        min=0,
        max=360,
        )

    screw_offset: bpy.props.FloatProperty(
        name="Screw Offset",
        description="Screw offset for the screw modifier",
        default=2,
        min=0,
        max=10,
        )

    animation_frame_start: bpy.props.IntProperty(
        name="Animation Start Frame",
        description="Start frame for the animation",
        default=1,
        min=1,
        )

    animation_frame_end: bpy.props.IntProperty(
        name="Animation End Frame",
        description="End frame for the animation",
        default=60,
        min=1,
        )

    final_location: bpy.props.FloatVectorProperty(
        name="Final Location",
        description="Final location for the animated object",
        default=(0, 0, 2.1),
        subtype='XYZ'
        )

    final_rotation: bpy.props.FloatProperty(
        name="Final Rotation",
        description="Final rotation angle in degrees",
        default=30,
        )

    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        description="Scale factor for extrusion",
        default=1.2,
        min=0.1,
        max=5.0,
        )


# Operator Class
class CreateAndAnimateCirclesOperator(bpy.types.Operator):
    bl_idname = "wm.create_and_animate_circles"
    bl_label = "Create and Animate Circles"

    def execute(self, context):
        props = context.scene.create_and_animate_circles_props

        # Call the function with the properties from the UI
        create_and_animate_circles(
            circle_1_location=props.circle_1_location,
            circle_2_location=props.circle_2_location,
            screw_angle=props.screw_angle,
            screw_offset=props.screw_offset,
            animation_frame_start=props.animation_frame_start,
            animation_frame_end=props.animation_frame_end,
            final_location=props.final_location,
            final_rotation=props.final_rotation,
            scale_factor=props.scale_factor
            )

        return {'FINISHED'}


# Register and Unregister Functions
def register():
    bpy.utils.register_class(CreateAndAnimateCirclesPanel)
    bpy.utils.register_class(CreateAndAnimateCirclesProperties)
    bpy.utils.register_class(CreateAndAnimateCirclesOperator)

    bpy.types.Scene.create_and_animate_circles_props = bpy.props.PointerProperty(
        type=CreateAndAnimateCirclesProperties
        )


def unregister():
    bpy.utils.unregister_class(CreateAndAnimateCirclesPanel)
    bpy.utils.unregister_class(CreateAndAnimateCirclesProperties)
    bpy.utils.unregister_class(CreateAndAnimateCirclesOperator)

    del bpy.types.Scene.create_and_animate_circles_props


if __name__ == "__main__":
    register()
