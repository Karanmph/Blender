import bpy
import math




def modify_existing_object(obj_name="BeideKreise", obj_name_location=(0, 0, 0), screw_angle=30, screw_offset=2,
                           animation_frame_start=1, animation_frame_end=60,
                           final_location=(0, 0, 1.2), final_rotation=30,
                           scale_factor=1.2):
    """
    Modifies an existing object in Blender, adds a screw modifier, duplicates and renames the object,
    applies transformations, and sets keyframes for animation.

    Parameters:
    obj_name (str): Name of the existing object to modify.
    screw_angle (float): Angle for the screw modifier in degrees.
    screw_offset (float): Screw offset for the screw modifier.
    animation_frame_start (int): Start frame for the animation.
    animation_frame_end (int): End frame for the animation.
    final_location (tuple): Final location for the animated object.
    final_rotation (float): Final rotation angle in degrees.
    scale_factor (float): Scale factor for extrusion.
    """

    # Get the existing object by name
    obj = bpy.data.objects.get(obj_name)
    # Set the location of the existing object
    obj.location = obj_name_location

    # Continue with the rest of the operations
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Add a screw modifier with specific parameters
    bpy.ops.object.modifier_add(type='SCREW')
    obj.modifiers["Screw"].angle = math.radians(screw_angle)
    obj.modifiers["Screw"].screw_offset = screw_offset
    # Duplicate the modified object
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    obj.select_set(True)  # Select the second circle
    bpy.context.view_layer.objects.active = obj  # Set it as the active object
    bpy.ops.object.duplicate()

    # Rename the duplicated object and apply the modifier
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["BeideKreise.001"].select_set(True)
    bpy.context.active_object.name = "Stümpfe"
    bpy.ops.object.modifier_apply(modifier="Screw")
    # Switch to edit mode, split vertices, and add faces
    # Duplicate the original circles
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    obj.select_set(True)  # Select the second circle
    bpy.context.view_layer.objects.active = obj  # Set it as the active object
    bpy.ops.object.duplicate()
    # Rename the duplicated object and remove the screw modifier
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["BeideKreise.001"].select_set(True)
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

    # Duplicate the animated object and rename it
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["PrepGrenze"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["PrepGrenze"]
    bpy.ops.object.duplicate()
    bpy.context.active_object.name = "PrepGrenze Volumen"
    # Scale the duplicated object and extrude vertices at frame set 20
    obj = bpy.data.objects.get("PrepGrenze Volumen")
    bpy.context.scene.frame_set(20)
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select vertices with x > 0
    for vert in bpy.context.object.data.vertices:
        if vert.co.x > 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    # Extrude selected vertices
    bpy.ops.mesh.extrude_region_move()

    # Scale extruded region
    bpy.ops.transform.resize(value=(1.2, 1.2, 1.2))
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select vertices with x < 0
    for vert in bpy.context.object.data.vertices:
        if vert.co.x < 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')

    # Extrude selected vertices
    bpy.ops.mesh.extrude_region_move()

    # Scale extruded region
    bpy.ops.transform.resize(value=(1.2, 1.2, 1.2))
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0)})
    # Now Movement the extruded region along the Z axis
    bpy.ops.transform.translate(value=(0, 0, 0.1))
    bpy.ops.object.mode_set(mode="OBJECT")
    # Add Boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Stümpfe"]
    # Create a material if one does not already exist
    obj = bpy.context.object
    if not obj.material_slots:
        obj.data.materials.append(bpy.data.materials.new(name="Viewport Color Material"))
    # Get the material
    material = obj.active_material

    # Change the viewport color of the material
    material.diffuse_color = (1, 0.0485976, 0.0529361, 1)  # RGBA, A ist der Alpha-Wert
    # Show_viewport
    bpy.context.object.modifiers["Boolean"].show_viewport = True
    # Hide Stümpfe

    # Duplicate the modified object
    bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
    # Select 'PrepGrenze Volumen'
    obj = bpy.data.objects.get("PrepGrenze Volumen")
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Duplicate the selected object
        bpy.ops.object.duplicate()

        # Rename the duplicated object
        duplicated_obj = bpy.context.active_object
        duplicated_obj.name = "PrepGrenze Volumen.größer"
        bpy.ops.object.mode_set(mode="EDIT")
    # Scale each Cricle of Duplicated_PrepGrenze_Volumen
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select vertices with x > 0
    for vert in bpy.context.object.data.vertices:
        if vert.co.x > 0:
            vert.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.1, 1.1, 1.1))
    # Scale another Circle
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj and obj.type == "MESH":
        bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="VERT")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select vertices with x < 0
    for vert in bpy.context.object.data.vertices:
        if vert.co.x < 0:
            vert.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.1, 1.1, 1.1))
    bpy.ops.object.mode_set(mode='OBJECT')
    # Show viewport
    bpy.context.object.modifiers["Boolean"].show_viewport = False

    # Duplicate and create the Falsche Bewegung
    obj = bpy.data.objects.get("PrepGrenze Volumen.größer")
    if obj:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Duplicate the selected object
        bpy.ops.object.duplicate()

        # Rename the duplicated object
        duplicated_obj = bpy.context.active_object
        duplicated_obj.name = "PrepGrenze Volumen.falsche Bewegung"
    # Falsche Bewegung
    # Ensure the final duplicated object "PrepGrenze Volumen.falsche Bewegung" is selected and active
    bpy.ops.object.select_all(action='DESELECT')
    obj_name = "PrepGrenze Volumen.falsche Bewegung"
    if obj_name in bpy.data.objects:
        obj = bpy.data.objects[obj_name]
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Set the initial keyframe at frame 10 for the location (0, 0, 0)
        bpy.context.scene.frame_set(animation_frame_start)
        obj.location = (0, 0, 0)  # Origin at start
        obj.keyframe_insert(data_path="location")

        # Set the final keyframe at frame 80 for the location (0, 0, 3)
        bpy.context.scene.frame_set(animation_frame_end)
        obj.location = final_location  # Final location
        obj.keyframe_insert(data_path="location")

        # Ensure there is no rotation throughout the animation
        obj.rotation_euler = (0, 0, 0)
        obj.keyframe_insert(data_path="rotation_euler", frame=animation_frame_start)
        obj.keyframe_insert(data_path="rotation_euler", frame=animation_frame_end)

        # Set linear interpolation for all fcurves
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe_point in fcurve.keyframe_points:
                keyframe_point.interpolation = 'LINEAR'
        # List of object names to delete
        object_names = ["BeideKreise", "Circle_002", "PrepGrenze", "PrepGrenze Volumen", "Stümpfe"]

        # Deselect all objects first to ensure a clean selection
        bpy.ops.object.select_all(action='DESELECT')

        # Loop through each object name in the list
        for obj_name in object_names:
            # Check if the object exists in the scene
            if obj_name in bpy.data.objects:
                # Get the object
                obj = bpy.data.objects[obj_name]

                # Set the active object to our target
                bpy.context.view_layer.objects.active = obj

                # Select the object
                obj.select_set(True)

                # Delete all selected objects
                bpy.ops.object.delete()


# Call the function with custom parameters
modify_existing_object(obj_name="BeideKreise", obj_name_location=(2, 0, 0), screw_angle=45, screw_offset=3,
                       animation_frame_start=1, animation_frame_end=80,
                       final_location=(0, 0, 3), final_rotation=45,
                       scale_factor=1.5)