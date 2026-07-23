import bpy

from . import utils


def create_and_animate_circles(circle_1_location=(-2, 0, 0),
                               circle_2_location=(2, 0, 0),
                               screw_angle=30,
                               screw_offset=2,
                               animation_frame_start=1,
                               animation_frame_end=60,
                               final_location=(0, 0, 2.1),
                               final_rotation=30,
                               scale_factor=None):
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
    circle_1 = bpy.context.active_object
    circle_1.name = "Circle_001"
    circle_1.location = circle_1_location

    # Duplicate the circle, name it, and set its location
    bpy.ops.object.select_all(action='DESELECT')
    circle_1.select_set(True)
    bpy.context.view_layer.objects.active = circle_1
    bpy.ops.object.duplicate()
    circle_2 = bpy.context.active_object
    circle_2.name = "Circle_002"
    circle_2.location = circle_2_location

    # Join both circles
    for ob in bpy.data.objects:
        ob.select_set(ob in [circle_1, circle_2])
    bpy.ops.object.join()
    bpy.context.scene.cursor.location = (0, 0, 0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # The joined object is now circle_2 (Circle_002)
    source_obj = circle_2

    # Add screw modifier
    utils.add_screw_modifier(source_obj, screw_angle, screw_offset)

    # Create Stümpfe
    utils.create_stuempfe(source_obj)

    # Create PrepGrenze with animation
    utils.create_prep_grenze(source_obj, animation_frame_start, animation_frame_end,
                             final_location, final_rotation)

    # Create PrepGrenze Volumen
    extrude_scale = scale_factor if scale_factor else 1.2
    utils.create_prep_grenze_volumen(extrude_scale)

    # Create PrepGrenze Volumen.größer
    utils.create_prep_grenze_groesser()

    # Create falsche Bewegung
    utils.create_falsche_bewegung(animation_frame_start, animation_frame_end, final_location)

    # Cleanup temporary objects
    utils.cleanup_objects(["Circle_002", "PrepGrenze", "PrepGrenze Volumen", "Stümpfe"])
