import bpy

from . import utils


def modify_existing_object(obj_name="BeideKreise", obj_name_location=(0, 0, 0), screw_angle=30, screw_offset=2,
                           animation_frame_start=1, animation_frame_end=60,
                           final_location=(0, 0, 2.1), final_rotation=30,
                           scale_factor=1.2):
    """
    Modifies an existing object in Blender, adds a screw modifier, duplicates and renames the object,
    applies transformations, and sets keyframes for animation.

    Parameters:
    obj_name (str): Name of the existing object to modify.
    obj_name_location (tuple): Location to set for the existing object.
    screw_angle (float): Angle for the screw modifier in degrees.
    screw_offset (float): Screw offset for the screw modifier.
    animation_frame_start (int): Start frame for the animation.
    animation_frame_end (int): End frame for the animation.
    final_location (tuple): Final location for the animated object.
    final_rotation (float): Final rotation angle in degrees.
    scale_factor (float): Scale factor for extrusion.
    """
    # Get the existing object by name
    source_obj = bpy.data.objects.get(obj_name)
    if not source_obj:
        print(f"Object '{obj_name}' not found in the scene.")
        return

    # Set the location of the existing object
    source_obj.location = obj_name_location

    # Add screw modifier
    utils.add_screw_modifier(source_obj, screw_angle, screw_offset)

    # Create Stümpfe
    utils.create_stuempfe(source_obj)

    # Create PrepGrenze with animation
    utils.create_prep_grenze(source_obj, animation_frame_start, animation_frame_end,
                             final_location, final_rotation)

    # Create PrepGrenze Volumen
    utils.create_prep_grenze_volumen(scale_factor)

    # Create PrepGrenze Volumen.größer
    utils.create_prep_grenze_groesser()

    # Create falsche Bewegung
    utils.create_falsche_bewegung(animation_frame_start, animation_frame_end, final_location)

    # Cleanup temporary objects (includes the original BeideKreise)
    utils.cleanup_objects([obj_name, "PrepGrenze", "PrepGrenze Volumen", "Stümpfe"])
