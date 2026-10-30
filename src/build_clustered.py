from pathlib import Path
import numpy as np,trimesh,json,shutil
from shapely.geometry import MultiPoint
from shapely.affinity import translate
P=Path(__file__).resolve().parents[1]/'build'; src=P/'最高15mm版'; out=P/'30颗群落版'
(out/'分件').mkdir(parents=True,exist_ok=True);(out/'预览').mkdir(exist_ok=True)
rng=np.random.default_rng(20261031)
def hull(m):return MultiPoint(m.vertices[:,:2]).convex_hull
def centered(i):
 m=trimesh.load_mesh(src/'单颗'/f'藤壶_{i+1:02}.stl');m.apply_translation(-np.r_[m.bounds[:,:2].mean(axis=0),0]);return m
sizes=[3,4,5,6,6,6]; small=iter(range(10,34)); groups=[[i]+[next(small) for _ in range(n-1)] for i,n in enumerate(sizes)]
objects=[];metadata=[]
for g,ids in enumerate(groups):
 parts=[centered(ids[0])]; hs=[hull(parts[0])]
 for k,i in enumerate(ids[1:]):
  m=centered(i);h=hull(m)
  angle=2*np.pi*k/(len(ids)-1)+rng.uniform(-.15,.15)+g*.71;d=np.array([np.cos(angle),np.sin(angle)])
  lo,hi=0.,65.
  for _ in range(35):
   t=(lo+hi)/2
   if translate(h,*(d*t)).intersects(hs[0]):lo=t
   else:hi=t
  for overlap in [1.4,1.8,2.2,2.6,3.0,3.5,4.0]:
   candidate=m.copy();candidate.apply_translation(np.r_[d*(lo-overlap),0])
   merged=trimesh.boolean.union([parts[0],candidate],engine='manifold')
   pieces=merged.split(only_watertight=False)
   # Fill fully enclosed air pockets formed between overlapping shells.
   # Open shell apertures remain part of the exterior surface.
   solids=[p for p in pieces if p.volume>0]
   if len(solids)==1 and solids[0].is_volume:
    merged=solids[0];break
  else:raise RuntimeError(('cannot connect',g,i))
  parts[0]=merged
 combined=parts[0]
 assert combined.is_volume and len(combined.split())==1,('cluster disconnected',g)
 objects.append(combined);metadata.append(dict(kind='cluster',count=len(ids),original_ids=[x+1 for x in ids]))
 print('cluster',g+1,len(ids),flush=True)
used={i for ids in groups for i in ids}
for i in range(50):
 if i not in used:objects.append(centered(i));metadata.append(dict(kind='single',count=1,original_ids=[i+1]))
placed=[];placedh=[]
for idx,m in enumerate(objects):
 m.apply_transform(trimesh.transformations.rotation_matrix(rng.uniform(0,6.28),[0,0,1]));h=hull(m)
 for attempt in range(20000):
  pos=rng.uniform(4,196,2);hh=translate(h,*pos)
  if min(hh.bounds[:2])<4 or max(hh.bounds[2:])>196:continue
  if any(hh.distance(x)<3 for x in placedh):continue
  m.apply_translation(np.r_[pos,0]);placed.append(m);placedh.append(hh);break
 else:raise RuntimeError('packing failed')
 name=f'{idx+1:02}_'+('群落'+str(metadata[idx]['count'])+'颗' if idx<6 else '独立藤壶')+'.stl'
 m.export(out/'分件'/name);metadata[idx]['file']=name
plate=trimesh.util.concatenate(placed);plate.export(out/'整盘藤壶_30颗群落_最高15mm.stl')
trial=placed[2].copy();trial.apply_translation(-trial.bounds[0]);trial.export(out/'先试打_5颗群落.stl')
loaded=trimesh.load_mesh(out/'整盘藤壶_30颗群落_最高15mm.stl')
assert loaded.is_volume and np.all(loaded.bounds[0]>=0) and np.all(loaded.bounds[1,:2]<=200) and abs(loaded.bounds[1,2]-15)<1e-5
assert len(loaded.split())==26
report=dict(total_barnacles=50,clustered_barnacles=30,cluster_sizes=sizes,independent_barnacles=20,printable_parts=26,maximum_height_mm=float(loaded.bounds[1,2]),bounds_mm=loaded.bounds.tolist(),minimum_part_gap_mm=min(a.distance(b) for i,a in enumerate(placedh) for b in placedh[i+1:]),closed=True,physical_print_tested=False,parts=metadata)
(out/'检查结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
scene=(src/'scene.py').read_text(encoding='utf-8').replace('整盘藤壶_最高15mm.stl','整盘藤壶_30颗群落_最高15mm.stl')
(out/'scene.py').write_text(scene,encoding='utf-8')
shutil.copytree(src/'预览/vendor',out/'预览/vendor',dirs_exist_ok=True)
s=(src/'预览/index.html').read_text(encoding='utf-8').replace('最高15毫米 / 50 颗','30颗相连 / 20颗独立').replace('每颗等比例缩小 · 分布于20厘米区域。','6组群落：3、4、5、6、6、6颗 · 最高15毫米。').replace('50 颗独立藤壶','6组群落 + 20颗独立藤壶').replace('size15','cluster30')
(out/'预览/index.html').write_text(s,encoding='utf-8')
(out/'打印说明.txt').write_text('保持原版50颗造型及最高15毫米，其中30颗组成6组相连群落（3、4、5、6、6、6颗），其余20颗独立。群落壳体在底部侧缘略微重叠并连接，没有共同底板。整盘共26件，200×200毫米范围。请按毫米、100%导入，先打印5颗群落样件。文件检查通过，尚未实物试打。\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='parts'}),flush=True)
