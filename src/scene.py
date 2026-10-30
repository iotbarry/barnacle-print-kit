import bpy, math, json
from pathlib import Path
from mathutils import Vector
P=Path(__file__).parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.001
def mat(name,color,roughness):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=roughness
 return m
shell=mat('Warm chalk shell',(.72,.67,.56),.82)
bpy.ops.wm.stl_import(filepath=str(P/'整盘藤壶_200mm.stl'));model=bpy.context.object;model.name='Reconstructed printable barnacles';model.data.materials.append(shell)
for p in model.data.polygons:p.use_smooth=True
bpy.ops.export_scene.gltf(filepath=str(P/'预览'/'barnacles.glb'),use_selection=True,export_format='GLB')
bedmat=mat('Dark removable print bed',(.027,.034,.04),.85)
bpy.ops.mesh.primitive_cube_add(size=1,location=(100,100,-1.2));bed=bpy.context.object;bed.name='Preview only - not printed';bed.dimensions=(204,204,2.4);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bed.data.materials.append(bedmat)
bevel=bed.modifiers.new('Soft bed edge','BEVEL');bevel.width=2;bevel.segments=3
gridmat=mat('Grid',(.12,.15,.17),.85)
for axis in range(2):
 for k in range(0,201,20):
  bpy.ops.mesh.primitive_cube_add(size=1,location=(k if axis==0 else 100,100 if axis==0 else k,.025));o=bpy.context.object;o.dimensions=(.13,200,.03) if axis==0 else (200,.13,.03);o.data.materials.append(gridmat)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(310,-300,370));cam=bpy.context.object;aim(cam,(100,100,5));cam.data.type='ORTHO';cam.data.ortho_scale=285;scene.camera=cam
for loc,power,size in [((20,-60,250),900000,120),((220,130,200),450000,100),((-100,200,140),350000,90)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(100,100,0))
scene.world.color=(.10,.10,.10);scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=1500;scene.render.resolution_y=1500;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
bpy.ops.wm.save_as_mainfile(filepath=str(P/'藤壶整盘.blend'))
scene.render.filepath=str(P/'整盘效果.png');bpy.ops.render.render(write_still=True)
cam.location=(130,-55,75);aim(cam,(60,45,10));cam.data.ortho_scale=83
scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.render.filepath=str(P/'细节效果.png');bpy.ops.render.render(write_still=True)
