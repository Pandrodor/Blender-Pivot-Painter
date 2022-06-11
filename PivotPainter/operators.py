import bpy,bmesh
import random
import mathutils
import math
import numpy as np

class PivotPaintSelection(bpy.types.Operator):
    bl_idname = "operator.pivot_painter"
    bl_label = "PivotPainter"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        print("__________-----___________")

        parent0 = []
        parent1 = []
        parent2 = []

        for nr, this_obj in enumerate(bpy.context.selected_objects):
            this_parent = this_obj.parent
            if this_parent is not None:
                parented_wm = this_obj.matrix_world.copy()
                this_obj.parent = None
                this_obj.matrix_world = parented_wm
                this_obj.parent = this_parent
                this_obj.matrix_parent_inverse = this_parent.matrix_world.inverted()
                if this_parent.parent is not None:
                    parent2.append(this_obj)
                else:
                    parent1.append(this_obj)
                this_parent = None
            else:
                parent0.append(this_obj)

        sorted_objects = np.concatenate((parent0, parent1, parent2))             


        for nr, obj in enumerate(sorted_objects):
            
            obj_parent = obj.parent
            obj.rotation_mode = 'XYZ'
        
            # create a new euler with default axis rotation order
            eul = mathutils.Euler((obj.rotation_euler[0], obj.rotation_euler[1], obj.rotation_euler[2]), 'XYZ')
        
            vec = mathutils.Vector((0.0, 0.0, 1.0))
            vec.rotate(eul)
            
            #flip Direction to drx
            vec[1] = vec[1] * -1.0
        
            print("Pure Vector = " + str(vec))
            print((vec + mathutils.Vector((1.0, 1.0, 1.0))) / 2.0)
        
            if not obj.data.vertex_colors:
               obj.data.vertex_colors.new()
            else:
                for this_vertex_color in obj.data.vertex_colors:
                    obj.data.vertex_colors.remove(this_vertex_color)
                obj.data.vertex_colors.new()
        
            color_layer = obj.data.vertex_colors["Col"]

            VcolAlpha = random.random()
            #if obj_parent is not None:
            #    VcolAlpha = round(math.floor(obj_parent.data.uv_layers[3].data[0].uv[1]), 3)
            i = 0
            for poly in obj.data.polygons:
                for idx in poly.loop_indices:
                    #rgb = [random.random() for i in range(3)]
                    RotationColor = (vec + mathutils.Vector((1.0, 1.0, 1.0))) / 2.0
                    color_layer.data[i].color = mathutils.Vector((RotationColor[0], RotationColor[1], RotationColor[2], VcolAlpha))
                    i += 1
        
        ########## -UV- ##########
    
            while len(obj.data.uv_layers) < 2:
                obj.data.uv_layers.new(name="UVmap_" + str(len(obj.data.uv_layers)))
        
            uvm2 = obj.data.uv_layers.get("LocXY")
            if uvm2 is None:
                obj.data.uv_layers.new(name="LocXY")
                  
            obj.data.uv_layers['LocXY'].active = True

            for face in obj.data.polygons:
                for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                    obj.data.uv_layers.active.data[loop_idx].uv = ( obj.location.x * 100, obj.location.y * 100)
        
            uvm3 = obj.data.uv_layers.get("LocZParentRotZRandom")
            if uvm3 is None:
                obj.data.uv_layers.new(name="LocZParentRotZRandom")
                
            obj.data.uv_layers['LocZParentRotZRandom'].active = True

            if obj_parent is not None:
                # create a new euler with default axis rotation order
                eule = mathutils.Euler((obj_parent.rotation_euler[0], obj_parent.rotation_euler[1], obj_parent.rotation_euler[2]), 'XYZ')
                vect = mathutils.Vector((0, 0, 1))
                vect.rotate(eule)
                #flip Direction to drx
                vect[1] = vect[1] * -1.0
                vect = (vect + mathutils.Vector((1.0, 1.0, 1.0))) / 2.0

            rnd = round(random.random(), 3)
            if obj_parent is not None:
                if obj_parent.parent is not None:
                    rnd = obj_parent.data.uv_layers[3].data[0].uv[1]
                    #rnd = round(math.floor(obj_parent.data.uv_layers[3].data[0].uv[1]), 3)
            #    if obj_parent.parent is None:
            #        rnd = (round(rnd, 3) * 1000) + round(obj_parent.data.uv_layers[3].data[0].uv[1] % 1, 3)
            #    else:
            #        rnd = (round(rnd, 3) * 1000) + round(math.floor(obj_parent.data.uv_layers[3].data[0].uv[1]) * 0.001, 3)
            
            for face in obj.data.polygons:
                for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                    obj.data.uv_layers.active.data[loop_idx].uv = (obj.location.z * 100, rnd)

            if obj_parent is not None:
                uvm4 = obj.data.uv_layers.get("ParentLocXY")
                if uvm4 is None:
                    obj.data.uv_layers.new(name="ParentLocXY")

                obj.data.uv_layers['ParentLocXY'].active = True
         
                for face in obj.data.polygons:
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        obj.data.uv_layers.active.data[loop_idx].uv = (obj_parent.location.x * 100, obj_parent.location.y * 100)


                uvm5 = obj.data.uv_layers.get("ParentLocZParentRotZ")
                if uvm5 is None:
                    obj.data.uv_layers.new(name="ParentLocZParentRotZ")

                obj.data.uv_layers['ParentLocZParentRotZ'].active = True

                for face in obj.data.polygons:
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        obj.data.uv_layers.active.data[loop_idx].uv = (obj_parent.location.z * 100, vect[2])

                uvm6 = obj.data.uv_layers.get("ParentRotXY")
                if uvm6 is None:
                    obj.data.uv_layers.new(name="ParentRotXY")

                obj.data.uv_layers['ParentRotXY'].active = True

                for face in obj.data.polygons:
                    for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                        obj.data.uv_layers.active.data[loop_idx].uv = (vect[0], vect[1])

        return {"FINISHED"}
        