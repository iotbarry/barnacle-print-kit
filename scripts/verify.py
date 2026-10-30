"""Read exported files, check print geometry and compare with the final originals."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import trimesh
from shapely.geometry import MultiPoint
ROOT=Path(__file__).resolve().parents[1]
folder=Path(sys.argv[1]).resolve()
expected=json.loads((ROOT/'reports/final-stl-sha256.json').read_text(encoding='utf-8'))
files=sorted((folder/'单颗').glob('*.stl'))
assert len(files)==50, f'Expected 50 single files, found {len(files)}'
hulls=[];total_faces=0
for f in files:
    m=trimesh.load_mesh(f)
    assert m.is_watertight and m.is_volume, f.name
    assert len(m.split(only_watertight=False))==1, f.name
    assert abs(m.bounds[0,2])<1e-6, f.name
    assert m.bounds[1,2]<=15.00001, f.name
    hulls.append(MultiPoint(m.vertices[:,:2]).convex_hull)
    total_faces+=len(m.faces)
gap=min(a.distance(b) for i,a in enumerate(hulls) for b in hulls[i+1:])
assert gap>0
plate=trimesh.load_mesh(folder/'整盘藤壶_最高15mm.stl')
assert plate.is_watertight and plate.is_volume
assert len(plate.faces)==total_faces
assert np.all(plate.bounds[0]>=-1e-6)
assert np.all(plate.bounds[1,:2]<=200)
assert abs(plate.bounds[1,2]-15)<1e-5
sample=trimesh.load_mesh(folder/'先试打三颗_15mm.stl')
assert sample.is_volume and len(sample.split())==3
matches={}
for name,record in expected.items():
    f=folder/name
    with f.open('rb') as stream: matches[name]=hashlib.file_digest(stream,'sha256').hexdigest()==record['sha256']
report=dict(count=50,all_single_components_connected=True,closed=True,
    maximum_height_mm=float(plate.bounds[1,2]),bounds_mm=plate.bounds.tolist(),
    minimum_gap_mm=gap,trial_count=3,all_original_stl_hashes_match=all(matches.values()),
    mismatched_files=[k for k,v in matches.items() if not v],physical_print_tested=False)
(folder/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2),flush=True)
assert all(matches.values()), 'Generated files differ from published originals; inspect before release.'
