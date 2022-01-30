import bpy

class ICECS_DT_data(bpy.types.PropertyGroup):
    ResX: bpy.props.IntProperty("Resolution X", default=1920)
    ResY: bpy.props.IntProperty("Resolution Y", default=1080)
    CameraObjName: bpy.props.StringProperty("Camera Obj Name")
    CameraName: bpy.props.StringProperty("Camera Name")
    Lock: bpy.props.BoolProperty("Lock for data", default=False)

    def timerFunc(self, context:bpy.types.Context):
        if self.TimerEnable:
            print("start timer")
            bpy.ops.icecs.recover() # start timer
        else:
            print("stop timer") # stop by timer

    TimerEnable: bpy.props.BoolProperty("Use timer", update=timerFunc, default=False)

    @classmethod
    def setupProperty(cls, is_setup:bool):
        from bpy.types import Scene as scene
        if is_setup:
            scene.IceCS_data = bpy.props.PointerProperty(type=ICECS_DT_data)
            print("Property IceCS_data defined")
        else:
            scene.IceCS_data = None
            print("Property IceCS_data uninstalled")
        
    @classmethod
    def getOrNewProperty(cls, scene:bpy.types.Scene):
        if not hasattr(scene, 'IceCS_data') or scene.IceCS_data is None:
            scene.IceCS_data = bpy.props.PointerProperty(type=ICECS_DT_data)
        return scene.IceCS_data

    @classmethod
    def updateData(cls, context:bpy.types.Context, autoLock:bool = False):
        data:ICECS_DT_data = cls.getOrNewProperty(context.scene)
        if data.Lock:
            print("access locked camera data")
            return
        if autoLock:
            data.Lock = True
        data.ResX = context.scene.render.resolution_x
        data.ResY = context.scene.render.resolution_y
        data.CameraObjName = context.scene.camera.name if context.scene.camera else ""
        data.CameraName = context.scene.camera.data.name if context.scene.camera else ""
        print("update to %d, %d, %s / %s"%(data.ResX, data.ResY, data.CameraObjName, data.CameraName))

    @classmethod
    def recoverData(cls, context:bpy.types.Context, autoLock:bool = False):
        data:ICECS_DT_data = context.scene.IceCS_data
        context.scene.render.resolution_x = data.ResX
        context.scene.render.resolution_y = data.ResY
        context.scene.camera = context.blend_data.objects.get(data.CameraObjName)

        if context.scene.camera:
            print("recover to %d, %d, %s"%(data.ResX, data.ResY, data.CameraObjName))
        else:
            for x in context.blend_data.objects:
                if x.type == 'CAMERA' and x.data.name == data.CameraName:
                    context.scene.camera = x
                    print("recover to %d, %d, %s (from %s)"%(data.ResX, data.ResY, x.name, data.CameraName))
                    break

        if autoLock:
            data.Lock = False

CLASSES = [
    ICECS_DT_data
]
