# trip-plan-builder（出行方案生成器）

> 遵循 [Agent Skills](https://agentskills.io/specification) 开放规范的技能包：把零散的出行/聚会信息，交给 Agent 生成一份**自包含、可离线、可分享**的单页 HTML 行动方案。

给它地点、时间、人数和素材偏好，它会按一套固定规则产出美观、层次清晰、便于沿途查看与转发的方案网页，并可配套可交互路线地图。适用于同学会、校友聚会、家庭出游、团队团建等场景。

**当前版本**：1.0.0 · **License**：MIT

## ✨ 能做什么

- **一次成型**：内置生成前提问（住宿片区/价位、餐厅菜系/人均、喜欢逛的景点）与十条生成规则，减少反复修改。
- **单文件自包含**：图片全部以 data URI 内嵌，离线可看、转发不丢图；同时产出 `.html` 与 `.mhtml`。
- **完整设计系统**：深蓝渐变头部、主题诗卡片、时间轴、图片组（1 大 + 3 小）、双路线卡、跨城交通章、全程一览表、打卡地一览、深浅主题切换、导航高亮、点图放大。
- **双场景**：「双日上午双路线」与「一日游（当日游玩 + 聚餐）」。
- **素材可核验**：内置小红书 / 大众点评 / 携程 / 飞猪的取图查价经验与登录协作流程。
- **热点增色**：结合出行城市当期热点，自然融入诗文、正文、图片、地图与汇总表。

## 🔌 平台兼容性

本技能遵循开放的 Agent Skills 规范（一个含 `SKILL.md` 的文件夹），**核心内容跨平台通用**，可直接被下列 Agent 加载。

平台差异只在"外围工具"，不影响规则本身：

| 平台 | 支持情况 | 安装方式 | 需要适配的部分 |
|---|---|---|---|
| **Claude Code** | ✅ 支持 | `npx skills add … -a claude-code` | 浏览器调试用该环境自带工具即可 |
| **OpenCode** | ✅ 支持 | `npx skills add … -a opencode` | 无，且兼容 `.claude/skills/` 目录 |
| **Codex / Cursor 等 70+** | ✅ 支持 | `npx skills add … -a <agent>` | 同上 |
| **WorkBuddy** | ✅ 原生支持 | git 命令（见下方） | 无（本技能在 WorkBuddy 中开发验证） |
| **DeepSeek Harness (dsh)** | ✅ 支持 | git 命令（见下方） | 需 `dsh` 环境；**chat.deepseek.com 网页版不支持技能** |

> `npx skills` 的 agent 列表目前不含 WorkBuddy 与 DeepSeek，这两个平台用第二条命令安装；其余 75+ Agent 一律走 `npx skills`。

> 技能中提到的 Chrome DevTools CLI 路径、文件预览工具、腾讯地图代理占位符是 **WorkBuddy 环境的具体写法**。在其它 Agent 中，让 Agent 用它自己可用的浏览器/地图工具完成同样步骤即可——规则与产物标准不变。

## 📦 安装

前置条件：**Node.js 22.20+**（`npx skills` 需要）。安装后新开一个会话即可触发。

### 方式一：npx skills 一行命令安装（推荐）

用 [skills CLI](https://github.com/vercel-labs/skills) 直接从本仓库安装，支持 75+ 种 Agent（含 Claude Code、OpenCode、Codex、Cursor 等）。

```bash
# 安装到当前项目（默认），同时装给 Claude Code 与 OpenCode
npx -y skills@latest add <owner>/<repo> --skill trip-plan-builder -a claude-code -a opencode -y

# 安装到全局（所有项目可用）
npx -y skills@latest add <owner>/<repo> --skill trip-plan-builder -a claude-code -a opencode -g -y

# 本地路径安装（发布前测试，或不想用 GitHub 时）
npx -y skills@latest add /path/to/trip-plan-builder --skill trip-plan-builder -a claude-code -g -y
```

把 `<owner>/<repo>` 换成你的 GitHub 仓库（如 `yourname/trip-plan-builder`）。安装前可先预览：

```bash
npx -y skills@latest add <owner>/<repo> --list          # 列出仓库里的 skill
npx -y skills@latest add <owner>/<repo> -s trip-plan-builder --copy -y   # 复制而非软链
```

其它常用：`npx skills list` 查看已装、`npx skills update trip-plan-builder` 更新、`npx skills remove trip-plan-builder` 卸载。

**发布前测试**：仓库未建立时，可先用本地路径安装（见上面第三条命令）；CLI 会校验本地目录并识别出 `trip-plan-builder`。命令输出的 `path` 即实际安装位置。

### 方式二：CLI 暂不支持的平台（WorkBuddy / DeepSeek Harness）

`npx skills` 的 agent 列表里目前没有 WorkBuddy 与 DeepSeek，用下面命令安装（仍是命令，无需手动拖目录）：

**WorkBuddy**（装到用户级，所有项目可用）

```bash
git clone <本仓库地址> /tmp/tpb && mkdir -p ~/.workbuddy/skills && cp -R /tmp/tpb/trip-plan-builder ~/.workbuddy/skills/ && rm -rf /tmp/tpb
```

项目级：把目标目录换成 `<项目目录>/.workbuddy/skills/`。

**DeepSeek Harness（dsh）**

> DeepSeek 网页聊天 box 不支持技能，只有开源的 DeepSeek Harness 支持。

```bash
git clone <本仓库地址> /tmp/tpb && mkdir -p ~/.dsh/skills && cp -R /tmp/tpb/trip-plan-builder ~/.dsh/skills/ && rm -rf /tmp/tpb
```

项目级换成 `.dsh/skills/`。技能目录会被自动监听，无需重启；可用 `/trip-plan-builder` 手动触发。

### 方式三：让 Agent 自己装（兜底，任何平台）

复制下面这段提示词发给你的 Agent：

```text
请帮我安装一个 Agent Skill。

名称：trip-plan-builder
来源：<粘贴本仓库地址，或上传的 zip 文件，或 SKILL.md 内容>

要求：
1. 先做安全审查：读一遍 SKILL.md 和 scripts/ 里的脚本，告诉我它做什么、会不会动我的文件或隐私，值不值得装。
2. 优先用 `npx -y skills@latest add <来源> --skill trip-plan-builder -y` 安装；若本平台不在 skills CLI 支持列表，就装到本平台对应的 skills 目录（目录名必须是 trip-plan-builder，保留 SKILL.md / references / scripts / assets 完整结构）。
3. 安装后验证目录结构与 SKILL.md 的 frontmatter 是否合法。
4. 告诉我安装路径，以及如何在本平台触发它。
```

## 🚀 使用

装好后，直接用自然语言描述需求即可，例如：

> 用出行方案生成器做一个 12 月广州两日同学聚会方案，4 人来穗 + 广州 3 人，天河聚餐住宿，第一天逛珠江新城，第二天两条备选路线。

Agent 会先问三件事，再把答案落到具体选择：

1. **住宿倾向**：片区 + 价位（如天河、¥400–700/晚）
2. **餐厅倾向**：菜系 + 人均（如粤菜、¥100–150）
3. **喜欢逛的景点**：类型或具体点

也可以手动触发：WorkBuddy 中 `@skill:trip-plan-builder`，Claude Code / DeepSeek Harness 中 `/trip-plan-builder`。

> `scripts/` 里的脚本由 Agent 按需调用，**你不需要手动运行**。

## ⚠️ 重要注意事项

### 1. 遇到需要登录的平台，必须人工配合

这是技能的**最高优先级约束**，优先于其它所有流程：

- 涉及 **小红书、携程、飞猪、大众点评** 等可能要求登录的平台时，Agent 应先暂停，明确提示你登录，并主动打开各平台的登录入口。
- **在你明确确认"已登录"之前，Agent 不会抓取任何依赖登录态的内容**，也不会擅自改用其它来源顶替。
- 你确认后，Agent 会**自行验证登录态**（读页面标识），验证通过才继续；分次登录也可以，通过的平台先用。
- **只有你明确说"不登录，用公开信息即可"**，才会改用公开搜索或开放图库，并如实标注来源。

### 2. 其它

- **图片必须自包含**：外链图片在离线/转发时会丢失，务必转 data URI。
- **不要裁图**：用模糊填充保留完整画面，不为缩小而裁边。
- **价格与场次易变**：酒店/门票价格、灯光秀与预约均以出行日官方信息为准，方案中标注"以当日为准"。
- **热点要核实时间**：热点须与出行日期有交集，已结束的活动不写入。
- **跨城市复用要防机械移植**：旧城市的地标/人物/事件不能带进新方案，逐处核实。
- **改完必验证并同步 MHTML**：避免两份文件不一致。

## 🧰 环境依赖（由 Agent 负责）

安装后无需人工预装依赖。Agent 会在开工前自检并在缺失时处理：

| 依赖 | 用途 | Agent 的处理方式 |
|---|---|---|
| Python 3 + Pillow | 图片比例归一化、MHTML 打包 | 检测 `import PIL`，缺失时提示并尝试 `pip install pillow` |
| 浏览器自动化工具 | 平台登录/取图、渲染验证、截图 | 用所在平台的浏览器工具（WorkBuddy 用 Chrome DevTools CLI） |
| 腾讯地图 JS API（可选） | 可交互路线地图 | 仅生成地图页时需要；无 Key 时可只出图例与示意图 |

若所在环境完全无法联网取图，Agent 应明确告知并改用开放图库兜底，不得假装是平台实拍。

## 📁 目录结构

```
trip-plan-builder/
├── SKILL.md                    # 技能入口：触发条件、流程、最高优先级约束
├── assets/
│   └── plan-template.html      # HTML 骨架 + 完整 CSS（占位符与三项交互脚本）
├── references/
│   ├── design-rules.md         # 生成十条规则 + 使用前提问
│   ├── workflow.md             # 制作流程、组件规范、文案与排版
│   ├── login-flow.md           # 登录平台协作流程（URL / 验证判据 / 话术）
│   ├── sourcing.md             # 素材与价格搜集：小红书/点评/携程/飞猪
│   ├── hotspots.md             # 结合城市热点
│   ├── collaboration.md        # 逐批素材、口吻、逐条修改
│   ├── content.md              # 主题诗、标语、一览表写法
│   ├── map.md                  # 腾讯地图路线页与三处一致性
│   ├── one-day.md              # 一日游裁剪
│   └── pitfalls.md             # 踩坑清单 + 浏览器验证清单
└── scripts/
    ├── normalize_images.py     # 图片比例归一化 + data URI
    └── mhtml_pack.py           # HTML → MHTML
```

## 📄 License

[MIT](LICENSE) © 2026
