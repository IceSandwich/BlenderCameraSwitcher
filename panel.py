import bpy
from .data import ICECS_DT_data

class ICECS_PT_CameraManager(bpy.types.Panel):
    bl_label = "Camera Manager"
    bl_idname = "ICECS_PT_CameraManager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Camera Switcher"
    
    def draw(self, context:bpy.types.Context):
        layout = self.layout
        scene = context.scene

        layout.operator("icecs.addrefimage", icon="OUTLINER_OB_IMAGE")
        layout.prop(ICECS_DT_data.getOrNewProperty(scene), "TimerEnable", text="Auto update")

        layout.separator()

        for x in context.blend_data.objects:
            if x.type == 'CAMERA':
                layout.operator("icecs.switchto", text=x.name, icon="OUTLINER_OB_CAMERA").cameraName = x.name

class ICECS_PT_CameraQuickOperation(bpy.types.Panel):
    bl_label = "Camera Quick Operation"
    bl_idname = "ICECS_PT_CameraQuickOperation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Camera Switcher"

    def draw(self, context:bpy.types.Context):
        layout = self.layout
        scene = context.scene

        layout.prop(context.space_data, "lock_camera", toggle=1, icon="DECORATE_LOCKED")
        layout.separator()

        area = context.area
        if area.type == 'VIEW_3D' and area.spaces[0].region_3d and area.spaces[0].region_3d.view_perspective == 'CAMERA':
            camera = context.scene.camera.data
            layout.prop(camera, "lens")
            if len(camera.background_images) > 0:
                layout.prop(camera.background_images[0], "alpha")
                layout.prop(camera.background_images[0], "display_depth")
            layout.separator()

CLASSES = [
    ICECS_PT_CameraManager,
    ICECS_PT_CameraQuickOperation
]