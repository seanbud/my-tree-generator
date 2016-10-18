import bpy
from bpy.props import IntProperty, FloatProperty
from bpy.types import Operator  

import mathutils
from mathutils import Vector
from math import radians




class AddMyTree(bpy.types.Operator):
	bl_idname  = "mesh.gen_tree"  
	bl_label = "Generate Tree"  
	bl_options = {'REGISTER', 'UNDO', 'PRESET'}

	niterations = IntProperty(  
		name = "iterations",
		default = 1, 
		min = 1,  
		max = 20 )  

	seed = FloatProperty(name="seed")  

	angle = FloatProperty(  
		name  = 'angle',  
		default  = radians(200),  
		subtype = 'ANGLE',  
		description = "size in degrees of angle operators" )  

	def buildTree(self):
		start = Vector((0,0,0))
		start_dir = Vector((0,0,1))
		angle_dir = Vector((self.angle/3.14,0,1))
		angle_dir2 = Vector((-self.angle/3.14,0,1))
		angle_dir3 = Vector((0,self.angle/3.14,1))
		angle_dir4 = Vector((0,-self.angle/3.14,1))
		nodelist = []

		#add a branch each iteration. incriment start position.
		for i in range(self.niterations):
			if(i % 3 == 2):
				add_branch(start, start_dir, 0.35, 0.35)
				apply_subdivision()

				add_branch(start, Vector((0.64,0,0.64)), 0.18, 0.8)
				add_branch(start, Vector((-0.64,0,0.64)), 0.18, 0.8)

				for vec in nodelist:
					add_branch(vec, angle_dir, 0.2, 0.8)
					add_branch(vec, angle_dir2, 0.2, 0.8)
					add_branch(vec, angle_dir3, 0.2, 0.5)
					add_branch(vec, angle_dir4, 0.2, 0.5)

				nodelist = [start + angle_dir, start + angle_dir2]
				if(i%6== 2):
					nodelist.append(start + angle_dir3)
					nodelist.append(start + angle_dir4)
					nodelist.append(start)

			else:
				add_branch(start, start_dir, 0.2, 0.5)
				start += start_dir/2;

	def execute(self, context):  
		delete_all()
		center_cursor()
		self.buildTree()
		join_all_parts()
		apply_wave(self.seed)
		apply_cast(self.niterations)
		return {'FINISHED'}

def add_object_button(self, context):  
	self.layout.operator(  
		AddMyTree.bl_idname,  
		text=AddMyTree.__doc__,  
		icon='PLUGIN')

def register():
	bpy.utils.register_class(AddMyTree)
	bpy.types.INFO_MT_add.append(add_object_button)  
	  
if __name__ == "__main__":  
	register()



""" HELPER FUNCTIONS BELOW """

def add_branch(start, direc, radius, length):
	"""
	:param Vector start:
	:param Vector direc:
	:param float radius:
	:rtype: bpy.types.Object
	"""
	bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, vertices=5,location=start, rotation=direc)
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.context.active_object.location += direc*length/2
	return bpy.context.active_object

def delete_all():
	for item in bpy.context.scene.objects:
		bpy.context.scene.objects.unlink(item)

	for item in bpy.data.objects:
		bpy.data.objects.remove(item)

	for item in bpy.data.meshes:
		bpy.data.meshes.remove(item)

	for item in bpy.data.materials:
		bpy.data.materials.remove(item)

def apply_subdivision():
	bpy.ops.object.modifier_add(type='SUBSURF')  
	bpy.context.active_object.modifiers[0].levels = 1 


def join_all_parts():
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.join()

def apply_wave(offset):
	bpy.ops.object.modifier_add(type='WAVE')
	bpy.context.active_object.modifiers[0].use_normal = True 
	bpy.context.active_object.modifiers[0].time_offset = offset

def apply_cast(niterations):
	bpy.context.active_object.location = Vector((0,0,niterations/10 + 2*niterations/10 ))
	bpy.ops.object.modifier_add(type='CAST')
	if (niterations > 15):
		bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.5, vertices=5,location=Vector((0,0,0.75)))

def center_cursor():
	bpy.ops.view3d.snap_cursor_to_center() 