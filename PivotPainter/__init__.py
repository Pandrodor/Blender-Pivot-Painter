import bpy
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

bl_info = {
    "name" : "PivotPainter",
    "author" : "Malte Szellas",
    "description" : "",
    "version": (1, 2),
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

from . import auto_load

auto_load.init()

def pivot_painter_menue_draw(self, context):
    self.layout.operator('operator.pivot_painter')

def register():
    auto_load.register()
    bpy.types.VIEW3D_MT_object.append(pivot_painter_menue_draw)

def unregister():
    auto_load.unregister()
    bpy.types.VIEW3D_MT_object.remove(pivot_painter_menue_draw)