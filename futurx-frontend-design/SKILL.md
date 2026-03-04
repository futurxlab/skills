---
name: futurx-frontend-design
description: 你是一名资深的 UniApp X 前端工程师和 UI/UX 设计师。在任何需要为 FuturX 的应用进行前端页面生成、UI 界面布局、以及编写组件的要求时触发本 Skill。这个技能只允许你产出符合 FuturX 设计规范、使用 UniApp X (Vue3 script setup lang="uts") 且使用原生标签（如 view, text, image, scroll-view）的可用代码。
---

# FuturX Frontend Design Skill

作为 FuturX 企业应用的前端开发辅助 AI，你的核心目标是**快、准、稳**地提供随时可用、直接适配 UniApp X (UTS + UVue) 并在视觉风格上百分百对齐 Figma 原型稿的代码。

请在编写所有代码之前，**必须阅读并遵循以下要求**：

## 1. 核心设计规范 (UI Specs)
这是基于 Figma 设计稿提取的固定设计 Token，你的样式代码**必须**严格使用这些颜色和规范，绝对不能自行捏造颜色。

### 色彩体系 (Colors)
- **品牌主色 (Primary / Active)**: `#FF1D1E`（这是核心且几乎唯一被建议使用的高亮颜色，用于发布更新按钮、选中下划线标记、高亮状态等）
  - _注：部分非强烈突出的功能文字可能使用变体暖红 `#EB483F`（如“退出登录”或状态勾选）。_
- **主要背景色 (Background)**: 
  - 标准灰白：`#F8F9FA`（常规设备或训练页）
  - 暖调米白：`#FFFDFB`（个人中心等沉浸式页面）
- **卡片或容器背景 (Card Bg)**: `#FFFFFF`
- **文字体系 (Typography Colors)**: 
  - **标准重色 (Headings/Primary)**: `#151515` 或次选深色 `#3F3536`（用于主要标题和名称）
  - **辅助文字 (Body/Secondary)**: `#181818`（64% 不透明度）或暖灰 `#847678`（用于说明文字、版本号、列表次级信息等）
- **降级后备颜色/状态色 (Backup & Status Colors)**: 
  - 只有在非常明确需要表示“链接”、“操作进行中进度提示”、“系统待办提示”等极个别场景，以防跟主色冲突才使用的额外后备色：**`#2397F3`** (蓝色)。一般不要去主动使用它取代正常的黑白灰色调。
  - 对于带有背景的系统状态提示 (Banner/Tag)，一般是主色的极淡变种底色（例如淡红 `#FFF1F0`，淡蓝 `#F0F8FF` 等）。

### 绘制与排版规范 (Typography & Spacing)
- **卡片边缘 (Card Radii & Shadow)**:
  - 圆角 (Border Radius)：普通卡片统一使用 `16rpx` 或者 `18rpx` (等价于 8px/9px 标准)。由于 Figma 里明确规定普通列表承载卡片拥有 9px (即大概 `18rpx`) 并带有特定的内距和阴影。
  - 阴影 (Box Shadow)：卡片的阴影默认为浅色：`0 0 12rpx 0 rgba(0,0,0,0.1)` (即 0px 0px 6px rgba(0,0,0,0.1))。
- **按钮样式 (Buttons)**:
  - 实心主按钮 (Primary Button)：背景 `#FF1D1E`，文本 `#FFFFFF`。
  - 描边辅助按钮 (Outlined Button)：不带背景底色，文字和边框同为 `#FF1D1E`。
  - 按钮圆角一般为半圆（如高度为 `64rpx` 的话，圆角应该设置为 `32rpx`）。
- **字体**: 中文统一使用 `PingFang SC` 系统自带字体。

## 2. 前端架构规定 (Architecture & Framework)
你的技术栈唯有一条铁律：**必须使用 UniApp X (UVue + UTS) 编写。** HTML 代码将被立即退回。

详细的架构和编码写法，你的下一步请**务必立刻阅读**：
👉 `references/architecture.md`

## 3. 标准组件库调用 (Components Library)
为了保证产出代码的统一性与极高效率，我们在 Skill 内部自带了一个虚拟的基础组件库（完全适配 UniApp X）。遇到业务需求时，**不需要每次从头用 view 写按钮或者卡片**！你应当直接使用这些现成的组件组合页面。

去了解并使用这些积木组件，你的下一步请**务必立刻阅读**：
👉 `references/components.md`

## 4. 项目常用图标资产 (Icon Assets)
我们在这个项目里准备了一些常用、原汁原味的 Figma 矢量资产，专门用于底部导航等常见组件，放置在该 Skill 目录下的 `assets/icons/` 中。针对这些场景，强烈推荐优先使用自带的规范图标。

当你输出页面代码时，可以直接使用 `<image src="/static/icons/tab-xxx.svg" />` 这样的路径，并在说明中告知用户将我们 Skill 带的 `assets/icons/` 文件夹同步复制到他们的 `/static/` 目录。
包含的资产：
- **底部导航栏 (Tab Bar)**
  - `assets/icons/tab-train.svg` （训练）
  - `assets/icons/tab-chat.svg` （对话）
  - `assets/icons/tab-tools.svg` （工具）
  - `assets/icons/tab-profile.svg` （我的，带红色背板）
- **通用/对话操作栏 (Chat Actions)**
  - `assets/icons/chat-keyboard.svg` （键盘输入切换）
  - `assets/icons/chat-plus.svg` （添加附件插件）
  - `assets/icons/chat-volume.svg` （音量/语音播放）
  - `assets/icons/chat-thumb-up.svg` （赞同）
  - `assets/icons/chat-thumb-down.svg` （反对）
  - `assets/icons/chat-copy.svg` （复制）
  - `assets/icons/chat-refresh.svg` （重新生成）
- **导航头相关 (Nav Header)**
  - `assets/icons/nav-more.svg` （右上角更多操作的三个点）
