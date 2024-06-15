bl_info = {
    "name": "Helical Bridge Animator",
    "blender": (2, 92, 0),  # Update with the minimum Blender version you support
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Your Name",
    "description": "Animate circles in a helical structure for bridge design."
}

import bpy
from helix1 import create_and_animate_circles

class CreateAndAnimateCirclesPanel(bpy.types.Panel):
    bl_label = "Create and Animate Circles"
    bl_idname = "OBJECT_PT_create_and_animate_circles"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Helical Bridge'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        create_and_animate_props = context.scene.create_and_animate_props
        layout.prop(create_and_animate_props, "circle_1_location")
        layout.prop(create_and_animate_props, "circle_2_location")
        layout.prop(create_and_animate_props, "screw_angle")
        layout.prop(create_and_animate_props, "screw_offset")
        layout.prop(create_and_animate_props, "animation_frame_start")
        layout.prop(create_and_animate_props, "animation_frame_end")
        layout.prop(create_and_animate_props, "final_location")
        layout.prop(create_and_animate_props, "final_rotation")
        layout.prop(create_and_animate_props, "scale_factor")
        layout.operator("wm.create_and_animate_circles")

class CreateAndAnimateCirclesProperties(bpy.types.PropertyGroup):
    circle_1_location: bpy.props.FloatVectorProperty(
        name="Circle 1 Location", description="Location of the first circle", default=(-2, 0, 0))
    circle_2_location: bpy.props.FloatVectorProperty(
        name="Circle 2 Location", description="Location of the second circle", default=(2, 0, 0))
    screw_angle: bpy.props.FloatProperty(
        name="Screw Angle", description="Angle for the screw modifier in degrees", default=30)
    screw_offset: bpy.props.FloatProperty(
        name="Screw Offset", description="Screw offset for the screw modifier", default=2)
    animation_frame_start: bpy.props.IntProperty(
        name="Animation Frame Start", description="Start frame for the animation", default=1)
    animation_frame_end: bpy.props.IntProperty(
        name="Animation Frame End", description="End frame for the animation", default=60)
    final_location: bpy.props.FloatVectorProperty(
        name="Final Location", description="Final location for the animated object", default=(0, 0, 2.1))
    final_rotation: bpy.props.FloatProperty(
        name="Final Rotation", description="Final rotation angle in degrees", default=30)
    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor", description="Scale factor for extrusion", default=1.2)

class CreateAndAnimateCirclesOperator(bpy.types.Operator):
    bl_idname = "wm.create_and_animate_circles"
    bl_label = "Create and Animate Circles"

    def execute(self, context):
        props = context.scene.create_and_animate_props
        create_and_animate_circles(
            circle_1_location=props.circle_1_location,
            circle_2_location=props.circle_2_location,
            screw_angle=props.screw_angle,
            screw_offset=props.screw_offset,
            animation_frame_start=props.animation_frame_start,
            animation_frame_end=props.animation_frame_end,
            final_location=props.final_location,
            final_rotation=props.final_rotation,
            scale_factor=props.scale_factor)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CreateAndAnimateCirclesPanel)
    bpy.utils.register_class(CreateAndAnimateCirclesProperties)
    bpy.utils.register_class(CreateAndAnimateCirclesOperator)
    bpy.types.Scene.create_and_animate_props = bpy.props.PointerProperty(type=CreateAndAnimateCirclesProperties)

def unregister():
    bpy.utils.unregister_class(CreateAndAnimateCirclesPanel)
    bpy.utils.unregister_class(CreateAndAnimateCirclesProperties)
    bpy.utils.unregister_class(CreateAndAnimateCirclesOperator)
    del bpy.types.Scene.create_and_animate_props

if __name__ == "__main__":
    register()