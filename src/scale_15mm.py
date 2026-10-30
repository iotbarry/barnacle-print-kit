from pathlib import Path
import trimesh,numpy as np,json,shutil
from shapely.geometry import MultiPoint
P=Path(__file__).parent;src=P/'壳片重建打印版';out=P/'最高15mm版'
(out/'单颗').mkdir(parents=True,exist_ok=True);(out/'预览').mkdir(exist_ok=True)
files=sorted((src/'单颗').glob('*.stl'))
height=max(trimesh.load_mesh(f).bounds[1,2] for f in files);factor=15/height
meshes=[];hulls=[]
for f in files:
 m=trimesh.load_mesh(f);original=m.vertices.copy();center=np.r_[m.bounds[:,:2].mean(axis=0),0.]
 m.vertices=(m.vertices-center)*factor+center
 assert np.allclose(m.vertices,(original-center)*factor+center)
 assert m.is_volume and abs(m.bounds[0,2])<1e-6
 m.export(out/'单颗'/f.name);meshes.append(m);hulls.append(MultiPoint(m.vertices[:,:2]).convex_hull)
plate=trimesh.util.concatenate(meshes);plate.export(out/'整盘藤壶_最高15mm.stl')
samples=[]
for idx,x in zip([0,8,-1],[2,35,60]):
 m=meshes[idx].copy();m.apply_translation(-m.bounds[0]);m.apply_translation([x,2,0]);samples.append(m)
trimesh.util.concatenate(samples).export(out/'先试打三颗_15mm.stl')
# Verify actual exported files and the height rather than relying on source dimensions.
loaded=trimesh.load_mesh(out/'整盘藤壶_最高15mm.stl')
assert loaded.is_volume and abs(loaded.bounds[1,2]-15)<1e-5
assert np.all(loaded.bounds[0,:2]>=0) and np.all(loaded.bounds[1,:2]<=200)
gap=min(a.distance(b) for i,a in enumerate(hulls) for b in hulls[i+1:]);assert gap>0
report=dict(count=len(meshes),scale_factor=factor,maximum_height_mm=float(loaded.bounds[1,2]),bounds_mm=loaded.bounds.tolist(),minimum_gap_mm=gap,uniform_xyz_scale=True,positions_preserved=True,closed=True,physical_print_tested=False)
(out/'尺寸检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
s=(src/'scene.py').read_text(encoding='utf-8').replace('整盘藤壶_200mm.stl','整盘藤壶_最高15mm.stl')
(out/'scene.py').write_text(s,encoding='utf-8')
shutil.copytree(src/'预览/vendor',out/'预览/vendor',dirs_exist_ok=True)
s=(src/'预览/index.html').read_text(encoding='utf-8').replace('壳片重建 / 50 颗','最高15毫米 / 50 颗').replace('最高 2.98 厘米','最高 15 毫米').replace('rebuild1','size15').replace('独立平底 · 不规则壳片 · 内侧小壳片。','每颗等比例缩小 · 分布于20厘米区域。')
(out/'预览/index.html').write_text(s,encoding='utf-8')
(out/'打印说明.txt').write_text('50颗藤壶沿长、宽、高三个方向等比例缩小至原来的约50.34%，最高15毫米。每颗在整盘中的中心位置保持不变，仍分布在200×200毫米范围内，没有共同底板。\n请按毫米、100%大小导入文件。先试打三颗，确认缩小后的薄边和纹理是否适合你的喷嘴。文件已检查，尚未实物试打。\n',encoding='utf-8')
print(report,flush=True)
