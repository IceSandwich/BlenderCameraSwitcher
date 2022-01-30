# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

from .panel import CLASSES as PANEL_CLASSES
from .operation import CLASSES as OPERATION_CLASSES
from .data import CLASSES as DATA_CLASSES


bl_info = {
    "name" : "CameraSwitcher",
    "author" : "IceSandwich",
    "description" : "A simple camera switcher for blender",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > Properties > Camera Switcher",
    "warning" : "This addon is still in develop. Use at your own risk.",
    "category" : "3D View",
    "wiki_url" : "https://github.com/IceSandwich/CameraSwitcher",
    "tracker_url":  "https://github.com/IceSandwich/CameraSwitcher/issues"
}

classes = [ *DATA_CLASSES, *OPERATION_CLASSES, *PANEL_CLASSES ]

@bpy.app.handlers.persistent
def load_post(scene:bpy.types.Scene):
    scene = bpy.context.scene
    if hasattr(scene, 'IceCS_data') and scene.IceCS_data is not None:
        scene.IceCS_data.TimerEnable = scene.IceCS_data.TimerEnable # start timer, invoke update func
    return False

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        if hasattr(cls, 'setupProperty'):
            cls.setupProperty(True)

    # Don't use it in test mode.
    # https://blender.stackexchange.com/questions/110454/load-post-handler-is-run-twice
    bpy.app.handlers.load_post.append(load_post)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        if hasattr(cls, 'setupProperty'):
            cls.setupProperty(False)