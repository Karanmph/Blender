"""
Shared utility functions for Blender helical operations.

This module contains reusable helper functions extracted from helix2_2.py
and Dentalscan_01.py to eliminate code duplication.
"""

import bpy
import math


def add_screw_modifier(obj, angle, offset):
    """
    Add a screw modifier to an object.

    Parameters:
        obj: The Blender object to add the modifier to.
        angle (float): Angle for the screw modifier in degrees.
        offset (float): Screw offset for the screw modifier.
    """
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_add(type='SCREW')
    obj.modifiers["Screw"].angle = math.radians(angle)
    obj.modifiers["Screw"].screw_offset = offset


def create_stuempfe(source_obj):
    """
    Create "Stümpfe" by duplicating the source object and applying the screw modifier.

    Parameters:
        source_obj: The source Blender object with a screw modifier.

    Returns:
        The created "Stümpfe" object.
    """
    bpy.ops.object.select_all(action='DESELECT')
    source_obj.select_set(True)
    bpy.context.view_layer.objects.active = source_obj
    bpy.ops.object.duplicate()

    duplicated = bpy.context.active_object
    bpy.ops.object.select_all(action='DESELECT')
    duplicated.select_set(True)
    bpy.context.view_layer.objects.active = duplicated
    duplicated.name = "Stümpfe"
    bpy.ops.object.modifier_apply(modifier="Screw")

    # Switch to edit mode, split vertices, and add faces
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.split()
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_flat()

    return bpy.data.objects.get("Stümpfe")


def create_prep_grenze(source_obj, frame_start, frame_end, final_loc, final_rot):
    """
    Create "PrepGrenze" by duplicating source, removing screw modifier, and adding animation.

    Parameters:
        source_obj: The source Blender object with a screw modifier.
        frame_start (int): Start frame for the animation.
        frame_end (int): End frame for the animation.
        final_loc (tuple): Final location (x, y, z) for the animated object.
        final_rot (float): Final rotation angle in degrees.

    Returns:
        The created "PrepGrenze" object.
    """
    bpy.ops.object.select_all(action='DESELECT')
    source_obj.select_set(True)
    bpy.context.view_layer.objects.active = source_obj
    bpy.ops.object.duplicate()

    duplicated = bpy.context.active_object
    bpy.ops.object.select_all(action='DESELECT')
    duplicated.select_set(True)
    bpy.context.view_layer.objects.active = duplicated
    duplicated.name = "PrepGrenze"

    # Remove screw modifier
    if duplicated.modifiers:
        screw_mod = duplicated.modifiers.get('Screw')
        if screw_mod:
            duplicated.modifiers.remove(screw_mod)

    # Set keyframes for location and rotation
    obj = bpy.data.objects.get("PrepGrenze")
    bpy.context.scene.frame_set(frame_start)
    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")

    bpy.context.scene.frame_set(frame_end)
    if obj:
        obj.location = final_loc
    bpy.ops.anim.keyframe_insert_by_name(type="Location")

    if obj:
        obj.rotation_euler = (0, 0, math.radians(final_rot))
    bpy.ops.anim.keyframe_insert_by_name(type="Rotation")

    # Set linear extrapolation for animation curves
    if obj and obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            fcurve.extrapolation = 'LINEAR'

    return obj


def create_prep_grenze_volumen(scale_factor=1.2):
    """
    Create "PrepGrenze Volumen" by duplicating PrepGrenze, extruding, and adding boolean.

    Parameters:
        scale_factor (float): Scale factor for extrusion (default 1.2).

    Returns:
        The created "PrepGrenze Volumen" object.
    """
    # Duplicate PrepGrenze
    bpy.ops.object.select_all(action="DESELECT")
    prep_grenze = bpy.data.objects.get("PrepGrenze")
    if prep_grenze:
        prep_grenze.select_set(True)
        bpy.context.view_layer.objects.active = prep_grenze
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = "PrepGrenze Volumen"

    obj = bpy.data.objects.get("PrepGrenze Volumen")
    bpy.context.scene.frame_set(20)

    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj

    # Extrude and scale vertices with x > 0
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for vert in bpy.context.object.data.vertices:
        if vert.co.x > 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move()
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

    # Extrude and scale vertices with x < 0
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for vert in bpy.context.object.data.vertices:
        if vert.co.x < 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move()
    bpy.ops.transform.resize(value=(scale_factor, scale_factor, scale_factor))

    # Extrude all and translate along Z
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0)})
    bpy.ops.transform.translate(value=(0, 0, 0.1))
    bpy.ops.object.mode_set(mode="OBJECT")

    # Add Boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
    stuempfe = bpy.data.objects.get("Stümpfe")
    if stuempfe:
        bpy.context.object.modifiers["Boolean"].object = stuempfe

    # Create and assign material
    obj = bpy.context.object
    if not obj.material_slots:
        obj.data.materials.append(bpy.data.materials.new(name="Viewport Color Material"))

    material = obj.active_material
    if material:
        material.diffuse_color = (1, 0.0485976, 0.0529361, 1)

    bpy.context.object.modifiers["Boolean"].show_viewport = True

    return obj


def create_prep_grenze_groesser():
    """
    Create "PrepGrenze Volumen.größer" by duplicating PrepGrenze Volumen and scaling circles.

    Returns:
        The created "PrepGrenze Volumen.größer" object.
    """
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("PrepGrenze Volumen")
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()

        duplicated_obj = bpy.context.active_object
        duplicated_obj.name = "PrepGrenze Volumen.größer"
        bpy.ops.object.mode_set(mode="EDIT")

    # Scale vertices with x > 0
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for vert in bpy.context.object.data.vertices:
        if vert.co.x > 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.1, 1.1, 1.1))

    # Scale vertices with x < 0
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    for vert in bpy.context.object.data.vertices:
        if vert.co.x < 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.1, 1.1, 1.1))
    bpy.ops.object.mode_set(mode='OBJECT')

    # Hide boolean modifier in viewport
    bpy.context.object.modifiers["Boolean"].show_viewport = False

    return bpy.data.objects.get("PrepGrenze Volumen.größer")


def create_falsche_bewegung(frame_start, frame_end, final_loc):
    """
    Create "PrepGrenze Volumen.falsche Bewegung" with animation.

    Parameters:
        frame_start (int): Start frame for the animation.
        frame_end (int): End frame for the animation.
        final_loc (tuple): Final location (x, y, z) for the animation.

    Returns:
        The created object or None if creation failed.
    """
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()

        duplicated_obj = bpy.context.active_object
        duplicated_obj.name = "PrepGrenze Volumen.falsche Bewegung"

    bpy.ops.object.select_all(action='DESELECT')
    obj_name = "PrepGrenze Volumen.falsche Bewegung"
    if obj_name in bpy.data.objects:
        obj = bpy.data.objects[obj_name]
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Set initial keyframe
        bpy.context.scene.frame_set(frame_start)
        obj.location = (0, 0, 0)
        obj.keyframe_insert(data_path="location")

        # Set final keyframe
        bpy.context.scene.frame_set(frame_end)
        obj.location = final_loc
        obj.keyframe_insert(data_path="location")

        # Ensure no rotation
        obj.rotation_euler = (0, 0, 0)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame_start)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame_end)

        # Set linear interpolation
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for keyframe_point in fcurve.keyframe_points:
                    keyframe_point.interpolation = 'LINEAR'

        return obj

    return None


def cleanup_objects(object_names):
    """
    Delete specified objects from the scene.

    Parameters:
        object_names (list): List of object names to delete.
    """
    bpy.ops.object.select_all(action='DESELECT')

    for obj_name in object_names:
        if obj_name in bpy.data.objects:
            obj = bpy.data.objects[obj_name]
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.delete()
