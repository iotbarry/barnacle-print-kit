"""Reproduce the two original modeling stages without changing published files."""
from pathlib import Path
import shutil, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
work = ROOT / 'build'
original = work / '壳片重建打印版'
original.mkdir(parents=True, exist_ok=True)
if list((original / '单颗').glob('*.stl')):
    raise SystemExit('Existing generated models found. Use a clean build directory to avoid mixing runs.')
shutil.copy2(ROOT/'src/build_original.py', original/'build.py')
shutil.copy2(ROOT/'src/scene.py', original/'scene.py')
shutil.copytree(ROOT/'viewer', original/'预览', dirs_exist_ok=True)
shutil.copy2(ROOT/'src/scale_15mm.py', work/'scale_15mm.py')
for script in [original/'build.py', work/'scale_15mm.py']:
    subprocess.run([sys.executable, str(script)], check=True)
subprocess.run([sys.executable, str(ROOT/'scripts/verify.py'), str(work/'最高15mm版')], check=True)
