import bpy
import math


def create_and_animate_circles(circle_1_location=(-2, 0, 0), circle_2_location=(2, 0, 0),
                               screw_angle=30, screw_offset=2, animation_frame_start=1,
                               animation_frame_end=60, final_location=(0, 0, 2.1),
                               final_rotation=30, scale_factor=1.2):
    """
    Creates two circles, joins them, adds a screw modifier, duplicates and renames the objects,
    applies transformations, and sets keyframes for animation in Blender.

    Parameters:
    circle_1_location (tuple): Location of the first circle.
    circle_2_location (tuple): Location of the second circle.
    screw_angle (float): Angle for the screw modifier in degrees.
    screw_offset (float): Screw offset for the screw modifier.
    animation_frame_start (int): Start frame for the animation.
    animation_frame_end (int): End frame for the animation.
    final_location (tuple): Final location for the animated object.
    final_rotation (float): Final rotation angle in degrees.
    scale_factor (float): Scale factor for extrusion.
    """
    # Add a circle
    bpy.ops.mesh.primitive_circle_add()
    circle_1 = bpy.context.active_object  # Access the currently active object
    circle_1.name = "Circle_001"  # Name the circle
    circle_1.location = circle_1_location  # Set the location of the circle

    # Duplicate the circle, name it, and set its location
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    circle_1.select_set(True)  # Select the first circle
    bpy.context.view_layer.objects.active = circle_1  # Set it as the active object
    bpy.ops.object.duplicate()
    circle_2 = bpy.context.active_object  # Access the duplicated active object
    circle_2.name = "Circle_002"  # Name the duplicated circle
    circle_2.location = circle_2_location  # Set the location of the duplicated circle

    # Join both circles
    bpy.ops.object.select_all(action="SELECT")  # Select all objects
    bpy.ops.object.join()  # Join the selected objects
    bpy.context.scene.cursor.location = (0, 0, 0)  # Set the 3D cursor to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')  # Set the origin to the cursor

    # Add a screw modifier with specific parameters
    bpy.ops.object.modifier_add(type='SCREW')
    bpy.context.object.modifiers["Screw"].angle = math.radians(screw_angle)
    bpy.context.object.modifiers["Screw"].screw_offset = screw_offset

    # Duplicate the modified object
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    circle_2.select_set(True)  # Select the second circle
    bpy.context.view_layer.objects.active = circle_2  # Set it as the active object
    bpy.ops.object.duplicate()

    # Rename the duplicated object and apply the modifier
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["Circle_002.001"].select_set(True)
    bpy.context.active_object.name = "Stümpfe"
    bpy.ops.object.modifier_apply(modifier="Screw")

    # Switch to edit mode, split vertices, and add faces
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.split()
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode
    bpy.ops.object.shade_flat()  # Set shading to flat

    # Duplicate the original circles
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    circle_2.select_set(True)  # Select the second circle
    bpy.context.view_layer.objects.active = circle_2  # Set it as the active object
    bpy.ops.object.duplicate()

    # Rename the duplicated object and remove the screw modifier
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["Circle_002.001"].select_set(True)
    bpy.context.active_object.name = "PrepGrenze"
    obj = bpy.context.active_object
    if obj.modifiers:
        obj.modifiers.remove(obj.modifiers.get('Screw'))

    # Set keyframes for location and rotation at different frames
    obj = bpy.data.objects.get("PrepGrenze")
    bpy.context.scene.frame_set(animation_frame_start)
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
    bpy.context.scene.frame_set(animation_frame_end)
    if obj:
        obj.location = final_location
    bpy.ops.anim.keyframe_insert_by_name(type="Location")
    if obj:
        obj.rotation_euler = (0, 0, math.radians(final_rotation))
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")

    # Set linear extrapolation for animation curves
    if obj and obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            fcurve.extrapolation = 'LINEAR'

    # Duplicate the animated object
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["PrepGrenze"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["PrepGrenze"]
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = "PrepGrenze Volumen"

    # Scale the duplicated object and extrude vertices
    obj = bpy.data.objects.get("PrepGrenze Volumen")
    bpy.context.scene.frame_set(20)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # Select vertices with x > 0
    """bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for vert in obj.data.vertices:
        vert.select = vert.co.x > 0
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move()
        bpy.ops.transform.resize(value=(1.2, 1.2, 1.2))
        Select
        vertices"""
        """with x < 0
            bpy.ops.object.mode_set(mode='OBJECT')
            for vert in obj.data.vertices:
                vert.select = vert.co.x < 0

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_region_move()
            bpy.ops.transform.resize(value=(1.2, 1.2, 1.2))"""

    #
    """bpy.ops.object.mode_set(mode='OBJECT')  # Switch back to object mode"""


# Call the function with custom parameters
"""create_and_animate_circles(circle_1_location=(-3, 0, 0), circle_2_location=(3, 0, 0),
                           screw_angle=45, screw_offset=3, animation_frame_start=10,
                           animation_frame_end=80, final_location=(0, 0, 3),
                           final_rotation=45, scale_factor=1.5)"""


# Call the function with custom parameters
"""
create_and_animate_circles(circle_1_location=(-3, 0, 0), circle_2_location=(3, 0, 0),
                           screw_angle=45, screw_offset=3, animation_frame_start=10,
                           animation_frame_end=80, final_location=(0, 0, 3),
                           final_rotation=45, scale_factor=1.5)
"""
 bpy.ops.mesh.select_all(action='DESELECT')
 bpy.context.view_layer.objects.active = bpy.data.objects["Circle_001.001"]
 bpy.ops.object.select_all(action='DESELECT')
 bpy.context.view_layer.objects.active = bpy.data.objects["Circle_002.001"]
 bpy.ops.object.select_all(action='DESELECT')
 bpy.context.view_layer.objects.active = bpy.data.objects["Circle_002.002"]
 bpy.ops.object.select_all(action='DESELECT')