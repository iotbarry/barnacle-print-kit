# 在本地重新制作

## 环境

原执行环境为 Windows、Python 3.12、Blender 4.5.9。依赖版本记录在 requirements.txt。建议独立环境安装，不修改系统已有依赖。

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python scripts/rebuild.py
.venv/Scripts/python scripts/verify.py build/最高15mm版
```

生成结果写入 `build/最高15mm版/`。脚本复制原始算法到 build 中执行，保留原文件名和两个制作阶段；不会更改发布的模型。固定随机种子和依赖有助于复现，不同平台的几何库可能改变顶点顺序或浮点结果；如文件指纹不一致，不能直接认定完全相同，需重新比较几何。

## 渲染和可编辑场景

完成生成后运行（将 blender 换成自己的程序路径）：

```powershell
blender -b -t 8 --python build/最高15mm版/scene.py
python -m http.server 8879 --bind 127.0.0.1 --directory build/最高15mm版
```

打开 http://127.0.0.1:8879/预览/ 。Blender 会写入整盘和细节 PNG、可编辑 blend、网页 GLB。渲染底板只用于展示；打印请使用 STL。blend 中保存的是实际模型网格和场景，重新改变造型参数请编辑 Python 源文件。

## 直接检查发布文件

从 Releases 下载完整打印包并解压，然后运行：

```powershell
.venv/Scripts/python scripts/verify.py 解压后的目录
```

检查逐颗闭合、正体积、底面、整盘读回尺寸、50 颗数量、平面间距、三颗样件及原始 STL 文件指纹。发布报告在 reports 中。物理打印结果不在这些检查范围内。

## 只查看网页预览

下载独立网页预览包，解压后在该目录运行 `python -m http.server 8879 --bind 127.0.0.1`，打开 http://127.0.0.1:8879/ 。不要直接双击 HTML；浏览器通常会限制本地模型读取。
