from pathlib import Path
import numpy as np,trimesh,json
from shapely.geometry import MultiPoint
from shapely.affinity import translate
P=Path(__file__).parent
(P/'单颗').mkdir(exist_ok=True)
rng=np.random.default_rng(71243)
def make(seed,R,H):
 q=np.random.default_rng(seed);N=384;L=68
 a=np.arange(N)*2*np.pi/N
 edges=np.r_[0,np.cumsum(q.uniform(.8,1.2,6))];edges*=2*np.pi/edges[-1]
 j=np.minimum(np.searchsorted(edges,a,side='right')-1,5);u=(a-edges[j])/(edges[j+1]-edges[j])
 heights=q.uniform(.78,1.,6);ap=q.uniform(.49,.64,6);skew=q.uniform(-.06,.06,6)
 top=H*(heights[j]-.09*np.sin(np.pi*u)**2+.035*np.sin(5*a+.7))
 # Unequal overlapping plate outlines; the cavity has a printable floor.
 vertices=[]
 for inner in [False,True]:
  for k in range(L+1):
   t=k/L;z=(.95+(top-.95)*t) if inner else top*t
   plate=1+.055*np.cos(2*np.pi*u)+skew[j]
   radius=R*((1-t)*plate+t*ap[j])+R*.075*np.sin(np.pi*t)
   radius+=R*.025*np.sin(3*a+.7)*(1-t*.5)
   if inner:radius-=max(1.0,R*.10)+.12*np.sin(7*a)
   else:
    # Different ridge spacing and erosion on every shell plate.
    rib=np.zeros(N)
    for c,amp,w,bend in zip(centers,amps,widths,bends):
     d=np.arctan2(np.sin(a-c-bend*t),np.cos(a-c-bend*t));rib+=amp*np.exp(-(d/w)**2)
    seam=np.exp(-(np.minimum(u,1-u)/.035)**2)
    radius+=(rib-.40*seam)*np.sin(np.pi*t/2)
    radius+=(.065*np.sin(43*a+3*np.sin(z*.8))+ .045*np.sin(79*a+z*1.7)+.025*np.sin(z*8+3*np.sin(11*a)))*min(1,t*8)
   x=radius*np.cos(a)+.08*H*t*t;y=radius*np.sin(a)-.04*H*t
   vertices.extend(np.c_[x,y,z])
 V=np.array(vertices);F=[];offset=(L+1)*N
 for side in range(2):
  off=side*offset
  for k in range(L):
   for n in range(N):
    b=(n+1)%N;quad=[off+k*N+n,off+k*N+b,off+(k+1)*N+b,off+(k+1)*N+n]
    tris=[[quad[0],quad[1],quad[2]],[quad[0],quad[2],quad[3]]]
    F.extend(tris if side==0 else [x[::-1] for x in tris])
 for n in range(N):
  b=(n+1)%N;o=L*N;i=offset+L*N
  F.extend([[o+n,o+b,i+b],[o+n,i+b,i+n]])
 # Solid floor closes each surface independently.
 V=np.vstack([V,[0,0,0],[0,0,.95]]);cb=len(V)-2;ct=len(V)-1
 for n in range(N):
  b=(n+1)%N;F.extend([[cb,b,n],[ct,offset+n,offset+b]])
 m=trimesh.Trimesh(V,F,process=True);m.fix_normals();assert m.is_volume
 # Two recessed lid plates grow from the floor, making one connected printable part.
 parts=[m]
 if seed%5!=0:
  for s in [-1,1]:
   verts=np.array([[s*.07*R,-.36*R,.65],[s*.48*R,-.16*R,.65],[s*.34*R,.36*R,.65],[s*.055*R,.36*R,.65],[s*.10*R,.07*R,H*.84],[s*.30*R,.12*R,H*.65]])
   parts.append(trimesh.convex.convex_hull(verts))
 m=trimesh.boolean.union(parts,engine='manifold') if len(parts)>1 else m
 assert m.is_volume
 m.apply_transform(trimesh.transformations.rotation_matrix(q.uniform(0,6.28),[0,0,1]));return m
meshes=[];hulls=[]
sizes=[(24,29.8),(21,25),(18,22),(17,19),(16,17),(15,19),(14,14),(13,17),(12,12),(12,15)]
sizes+=list(zip(rng.uniform(4.5,11,40),rng.uniform(5,12,40)))
for i,(R,H) in enumerate(sizes):
 q=np.random.default_rng(71243+i*39)
 centers=q.uniform(0,2*np.pi,42);amps=q.uniform(.20,.75,42)*min(1,R/12);widths=q.uniform(.014,.033,42);bends=q.uniform(-.08,.08,42)
 m=make(71243+i*39,R,H);h=MultiPoint(m.vertices[:,:2]).convex_hull
 for t in range(12000):
  pos=rng.uniform(2,198,2);hh=translate(h,*pos)
  if hh.bounds[0]<2 or hh.bounds[1]<2 or hh.bounds[2]>198 or hh.bounds[3]>198:continue
  if any(hh.distance(x)<1.6 for x in hulls):continue
  m.apply_translation([*pos,0]);meshes.append(m);hulls.append(hh);break
 else:continue
 m.export(P/'单颗'/f'藤壶_{len(meshes):02}.stl')
 print('built',len(meshes),flush=True)
scale=29.8/max(m.bounds[1,2] for m in meshes)
for idx,m in enumerate(meshes):
 m.vertices[:,2]*=scale;m.export(P/'单颗'/f'藤壶_{idx+1:02}.stl')
plate=trimesh.util.concatenate(meshes);plate.export(P/'整盘藤壶_200mm.stl')
samples=[]
for idx,x in zip([0,8,-1],[2,65,100]):
 m=meshes[idx].copy();m.apply_translation(-m.bounds[0]);m.apply_translation([x,2,0]);samples.append(m)
trimesh.util.concatenate(samples).export(P/'先试打三颗.stl')
(P/'尺寸.json').write_text(json.dumps(dict(count=len(meshes),bounds=plate.bounds.tolist(),closed=all(x.is_volume for x in meshes),min_gap=min(a.distance(b) for i,a in enumerate(hulls) for b in hulls[i+1:])),indent=2),encoding='utf-8')
