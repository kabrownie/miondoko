bl_info = {
    "name": "Mixamo to Rigify Retargeter",
    "blender": (3, 0, 0),
    "category": "Animation",
    "description": "Retarget Mixamo animations to Rigify rigs",
}

import bpy

class RetargetMixamoToRigifyOperator(bpy.types.Operator):
    """Retarget Mixamo animation to Rigify rig"""
    bl_idname = "animation.retarget_mixamo_to_rigify"
    bl_label = "Retarget Mixamo to Rigify"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mixamo_rig = context.scene.mixamo_rig
        rigify_rig = context.scene.rigify_rig

        if not mixamo_rig or not rigify_rig:
            self.report({'ERROR'}, "Please specify both Mixamo and Rigify rigs")
            return {'CANCELLED'}

        # Mapping dictionary: Mixamo -> Rigify
        bone_mapping = {
            "Hips": "root",
            "Spine": "spine",
            "Chest": "spine.003",
            "Neck": "spine.006",
            "Head": "spine.007",
            "LeftUpLeg": "thigh.L",
            "LeftLeg": "shin.L",
            "LeftFoot": "foot.L",
            "RightUpLeg": "thigh.R",
            "RightLeg": "shin.R",
            "RightFoot": "foot.R",
            "LeftArm": "upper_arm.L",
            "LeftForeArm": "forearm.L",
            "LeftHand": "hand.L",
            "RightArm": "upper_arm.R",
            "RightForeArm": "forearm.R",
            "RightHand": "hand.R",
        }

        # Retargeting process
        for mixamo_bone, rigify_bone in bone_mapping.items():
            if mixamo_bone in mixamo_rig.pose.bones and rigify_bone in rigify_rig.pose.bones:
                mixamo_bone_pose = mixamo_rig.pose.bones[mixamo_bone]
                rigify_bone_pose = rigify_rig.pose.bones[rigify_bone]

                # Copy transformations
                rigify_bone_pose.location = mixamo_bone_pose.location
                rigify_bone_pose.rotation_quaternion = mixamo_bone_pose.rotation_quaternion
                rigify_bone_pose.scale = mixamo_bone_pose.scale

        # Bake animation to Rigify rig
        bpy.ops.nla.bake(
            frame_start=context.scene.frame_start,
            frame_end=context.scene.frame_end,
            only_selected=True,
            visual_keying=True,
            clear_constraints=True,
            bake_types={'POSE'},
        )

        self.report({'INFO'}, "Animation retargeted successfully!")
        return {'FINISHED'}

class RetargetMixamoToRigifyPanel(bpy.types.Panel):
    """Panel for the addon"""
    bl_label = "Mixamo to Rigify Retargeter"
    bl_idname = "VIEW3D_PT_mixamo_to_rigify"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Retarget'

    def draw(self, context):
        layout = self.layout
        layout.prop_search(context.scene, "mixamo_rig", bpy.data, "objects", text="Mixamo Rig")
        layout.prop_search(context.scene, "rigify_rig", bpy.data, "objects", text="Rigify Rig")
        layout.operator("animation.retarget_mixamo_to_rigify")

def register():
    bpy.utils.register_class(RetargetMixamoToRigifyOperator)
    bpy.utils.register_class(RetargetMixamoToRigifyPanel)
    bpy.types.Scene.mixamo_rig = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.rigify_rig = bpy.props.PointerProperty(type=bpy.types.Object)

def unregister():
    bpy.utils.unregister_class(RetargetMixamoToRigifyOperator)
    bpy.utils.unregister_class(RetargetMixamoToRigifyPanel)
    del bpy.types.Scene.mixamo_rig
    del bpy.types.Scene.rigify_rig

if __name__ == "__main__":
    register()
