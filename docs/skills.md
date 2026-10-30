# Skills 与工具清单

Skill 是给助手的工作指引，不等于一个独立三维模型。本页整理实际作用和边界；没有把“可用”写成“使用过”。

| 名称 | 使用情况 | 输入与输出 | 在本项目中的边界 |
| --- | --- | --- | --- |
| imagegen | 实际使用 | 文字提示 → 单颗透明参考图、整盘概念图 | 生成二维图片，未直接生成最终打印几何 |
| computer-use:computer-use | 实际使用 | 浏览器页面 → 搜索、下载、预览交互检查 | 用于操作和检查网页，不负责造型 |
| forgecad | 早期评估 | 阅读建模指引，评估路线 | 最终有机壳片没有采用 ForgeCAD 建模 |
| SolidWorks 等其他可用 skill | 未用于最终作品 | 无 | 不能列为已使用 |

## imagegen 的复用方式

在支持图像生成的助手中使用 `prompts/` 中原文；先生成没有背景干扰的单颗，再生成群落概念。实际指引来自 Codex 内置 `imagegen/SKILL.md`。生成结果只能作为外观参考；必须另行建模、导出和检查。是否可用取决于使用者环境，不随本仓库安装。

## computer-use 的复用方式

实际指引来自 Codex 插件中的 `computer-use/SKILL.md`。用于查看真实页面、下载参考、打开本地预览，并检查旋转、俯视、细节和底板显隐。它需要相应桌面/浏览器权限。仅执行 JavaScript 或成功返回 HTTP，不能替代目视检查模型。

## 普通软件与服务（不是 skill）

- Python 3.12 + NumPy：生成可重复的尺寸、纹理和摆放参数。
- trimesh + manifold3d：生成、组合、导出与检查封闭形状。
- Shapely：检查平面轮廓间距。
- Blender 4.5.9：实际模型渲染、保存可编辑场景、导出网页模型；通过脚本调用，没有使用所谓“Blender skill”。
- Three.js：本地交互预览；保留其原 MIT 许可证。
- Microsoft TRELLIS.2：实际尝试的图生三维服务，导出未成功；不依赖它重建最终作品。

## 为什么不直接附上第三方 SKILL.md 全文

仓库提供具体操作步骤、提示词和项目代码，但不将安装环境里的整套插件指令冒充本项目原创内容。工具安装和官方文档请从其来源获取：[Codex skills](https://github.com/openai/skills)、[Blender](https://www.blender.org/)、[trimesh](https://github.com/mikedh/trimesh)、[Three.js](https://threejs.org/)、[TRELLIS.2 Space](https://huggingface.co/spaces/microsoft/TRELLIS.2)。本项目没有另外编造一个“历史上使用过的藤壶 skill”。
