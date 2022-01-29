import bpy, os
from .data import ICECS_DT_data

class ICECameraSwicher_OT_AddRefImage(bpy.types.Operator):
    bl_idname = "icecs.addrefimage"
    bl_label = "Add reference image"
    bl_options = {"REGISTER", 'UNDO'}

    directory: bpy.props.StringProperty(name="Directory", maxlen= 1024, default= "")
    files: bpy.props.CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    )

    def execute(self, context:bpy.types.Context):
        for file in self.files:
            cam = bpy.data.cameras.new("IceCS")
            cam.show_background_images = True
            bg = cam.background_images.new()
            bg.image = bpy.data.images.load(os.path.join(self.directory, file.name))

            cam_obj = bpy.data.objects.new("IceCS", cam)
            context.scene.collection.objects.link(cam_obj)

        return {'FINISHED'}

    def invoke(self, context:bpy.context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ICECameraSwicher_OT_SwitchTo(bpy.types.Operator):
    bl_idname = "icecs.switchto"
    bl_label = "Switch to camera"
    bl_options = {"REGISTER", 'UNDO'}

    cameraName: bpy.props.StringProperty(name="cameraName", default="")

    def execute(self, context:bpy.types.Context):
        if self.cameraName == '':
            self.report({'ERROR'}, "No camera name specified.")
            return {"CANCELLED"}

        cam_obj = context.blend_data.objects.get(self.cameraName)
        if cam_obj is None:
            self.report({'ERROR'}, "Cannot find \"%s\" camera specified."%self.cameraName)
            return {"CANCELLED"}
        assert(cam_obj.type == 'CAMERA')
        camera = cam_obj.data

        # Store settings
        if not context.region_data.view_perspective == 'CAMERA':
            ICECS_DT_data.updateData(context)

        # Set active camera
        context.scene.camera = cam_obj
        context.region_data.view_perspective = 'CAMERA'

        if camera.show_background_images == False or len(camera.background_images) == 0 or camera.background_images[0].image == None:
            return {"FINISHED"}

        # Correct
        width, height = camera.background_images[0].image.size
        context.scene.render.resolution_x = width
        context.scene.render.resolution_y = height

        return {"FINISHED"}

class ICECameraSwicher_OT_Recover(bpy.types.Operator):
    bl_idname = "icecs.recover"
    bl_label = "Recover scene to original"
    bl_options = {"REGISTER"}

    def modal(self, context:bpy.types.Context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}
        
        data = ICECS_DT_data.getOrNewProperty(context.scene)
        if not data.TimerEnable:
            wm = context.window_manager
            wm.event_timer_remove(self.timer)
            print("timer disable")
            return {'FINISHED'}

        isCamera = False
        for view_perspective in [ x.spaces[0].region_3d.view_perspective for x in context.screen.areas if x.type == 'VIEW_3D' and x.spaces[0].region_3d ]:
            if view_perspective == 'CAMERA':
                isCamera = True
                break

        if self.isCamera == isCamera: # no change
            return {'PASS_THROUGH'}

        self.isCamera = isCamera
        if self.isCamera: # nothing to do in camera mode
            return {'PASS_THROUGH'}

        ICECS_DT_data.recoverData(context)

        return {'PASS_THROUGH'}

    def execute(self, context:bpy.types.Context):
        wm = context.window_manager
        self.isCamera = False
        self.timer = wm.event_timer_add(3, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

CLASSES = [
    ICECameraSwicher_OT_AddRefImage,
    ICECameraSwicher_OT_SwitchTo,
    ICECameraSwicher_OT_Recover
]