# 前端架构说明 (Architecture Specs)

## 核心技术栈
在 FuturX 的 `futurmind_training_app` 中，**只能且仅能使用 UniApp X 的规范**。

### 1. 文件类型
- 不能产出任何 `.vue` 扩展名的文件。
- 全部组件和页面文件必须是 `.uvue` 后缀。

### 2. Vue 和 UTS 语法限制
- 每个文件中必须使用标准的 `<template>`, `<style>`, 且唯一的 `<script setup lang="uts">` 或 `<script lang="uts">`。
- **UTS (Uni TypeScript)** 是基于 TypeScript 的严格模式，禁止把任何变量任意打成 `any`，必须要明确类型。
- 绝不使用网页 DOM 标签（如 `<div>`, `<span>`, `<p>`, `<a>`，`<img>` 等）。必须全盘转化为原生支持的跨端标签：
  - 容器 = `<view>`, `<scroll-view>`
  - 文本 = `<text>`
  - 图片为主 = `<image src="..."/>`
  - 按钮可直接使用自定义 `<fx-button>` 或原生的 `<button>`

### 3. 数据层与生命周期
- 页面加载请直接使用 `@dcloudio/uni-app` 提供的原生生命周期如 `onLoad`, `onShow`, `onReady`。
- Vue 响应式数据必须由 `ref` 或 `reactive` 包装，导入：`import { ref, reactive } from 'vue'`。

### 4. 样式布局法则 (Styles & CSS)
由于底层并非 Webview，而是编译到原生 iOS / Android 的渲染引擎，**禁止出现不支持的原生 CSS 属性**。
- **排版必须基于 Flexbox:** 原生只能很好的识别 `display: flex;`。
- 不需要写任何厂商前缀 (如 `-webkit-`)。
- 当你需要为子组件预留空隙或边距，推荐使用 `margin` 和 `padding`，直接使用 `rpx` (Responsive Picker) 作为长度单位，不可使用 `rem`, `em`, `vh` 等。
- 圆角、阴影可以按照规范使用 `border-radius: 18rpx;` 或者是 `#FF1D1E` 等色值，但不支持过于复杂的滤镜 (`filter`) 或伪元素 (`::before`, `::after`)，必须使用真实的 `<view>` 叠加实现 UI。

###示例结构：
```uvue
<template>
  <view class="container">
    <text class="title">这是标题</text>
  </view>
</template>

<script setup lang="uts">
import { ref } from 'vue';

const titleText = ref<string>('这是标题');
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  background-color: #F8F9FA;
  padding: 30rpx;
}
.title {
  font-size: 32rpx;
  color: #151515;
  font-family: 'PingFang SC';
}
</style>
```
