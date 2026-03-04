# FuturX 组件库参考指南 (FuturX Components Library)

在编写 FuturX 页面时，你应该像使用现成的 UI 库那样，优先组合这里提供的组件！
你**不可以**手写普通的包含边框和原生颜色的 `<button>` 或 `<view class="card">`。当你需要用到卡片、按钮时，请直接输出这些组件的代码，假装由于你在辅助开发，这些组件已经被存在 `components/` 目录下。

## 1. 核心按钮: FxButton
用于触发主要或次要行为的通用按钮，包含默认高度和规范的圆角效果。

### 适用场景
所有的主行动（如：发布更新、保存设置），次要行动（如：测试、取消）。

### 参数设计 (Props)
- `type`: 按钮的类型，分为 `primary`（大红底色白字），`outline`（白底红边框红色字）或 `text`（仅文字，默认蓝色链接色`#2397F3`）。默认为 `primary`。
- `size`: 分为 `large` (全屏宽度/高 `88rpx`)、`medium` (宽长居中 / `64rpx`) 和 `small`。
- `disabled`: 禁用状态（灰色底色和不透明度限制）。
- `@click`: 事件。

### 标准实现代码 (`components/FxButton/FxButton.uvue`)
遇到需要创建这个组件的地方，直接使用这套代码：
```uvue
<template>
  <button :class="['fx-btn', `fx-btn--${type}`, `fx-btn--${size}`, { 'fx-btn--disabled': disabled }]" @click="handleClick">
    <text :class="['fx-btn-text', `fx-text--${type}`, { 'fx-text--disabled': disabled }]">
      <slot></slot>
    </text>
  </button>
</template>

<script setup lang="uts">
const props = defineProps({
  type: {
    type: String,
    default: 'primary' // 'primary', 'outline', 'text'
  },
  size: {
    type: String,
    default: 'medium' // 'large', 'medium', 'small'
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emits = defineEmits(['click']);

const handleClick = () => {
  if (!props.disabled) {
    emits('click');
  }
};
</script>

<style scoped>
/* 按钮统一基底 */
.fx-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  border-width: 0;
  border-radius: 999rpx; /* 药丸形状 */
  margin: 0;
  padding: 0 32rpx;
}
/* 主按钮 */
.fx-btn--primary {
  background-color: #FF1D1E;
}
.fx-text--primary {
  color: #FFFFFF;
  font-size: 28rpx;
  font-weight: 500;
}
/* 描边按钮 */
.fx-btn--outline {
  background-color: transparent;
  border: 1rpx solid #FF1D1E;
}
.fx-text--outline {
  color: #FF1D1E;
  font-size: 28rpx;
  font-weight: 500;
}
/* 字体按钮 (蓝色主色链接型) */
.fx-btn--text {
  background-color: transparent;
  padding: 0;
}
.fx-text--text {
  color: #2397F3;
  font-size: 28rpx;
  font-weight: 500;
}
/* 尺寸变化 */
.fx-btn--large {
  height: 88rpx;
  width: 100%;
}
.fx-btn--medium {
  height: 64rpx;
}
.fx-btn--small {
  height: 48rpx;
  padding: 0 16rpx;
}
/* 禁用状态 */
.fx-btn--disabled {
  opacity: 0.5;
  background-color: #E5E5E5;
}
</style>
```

---

## 2. 内容卡片: FxCard
Figma中所有带圆角、包含列表/配置项的主体内容块，统一使用此类卡片进行承载。这能保证内边距和投影样式全局一致。

### 标准实现代码 (`components/FxCard/FxCard.uvue`)
```uvue
<template>
  <view class="fx-card" :style="{ backgroundColor: bgColor, padding: padding }">
    <slot></slot>
  </view>
</template>

<script setup lang="uts">
defineProps({
  bgColor: {
    type: String,
    default: '#FFFFFF'
  },
  padding: {
    type: String,
    default: '32rpx'
  }
});
</script>

<style scoped>
.fx-card {
  border-radius: 18rpx;
  background-color: #FFFFFF;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  margin-bottom: 24rpx;
  display: flex;
  flex-direction: column;
}
</style>
```

---

## 3. 信息项: FxListItem
常见于设置页或任务列表中。包含左侧图标或文本，右侧副文本或状态标签。

```uvue
<template>
  <view class="fx-list-item" @click="$emit('click')">
    <view class="item-left">
      <slot name="prefix"></slot>
      <text class="item-title">{{ title }}</text>
    </view>
    <view class="item-right">
      <text class="item-sub">{{ subTitle }}</text>
      <slot name="suffix"></slot>
    </view>
  </view>
</template>

<script setup lang="uts">
defineProps({
  title: {
    type: String,
    default: ''
  },
  subTitle: {
    type: String,
    default: ''
  }
});

defineEmits(['click'])
</script>

<style scoped>
.fx-list-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid rgba(0,0,0,0.05); /* 浅色分割线 */
}
.item-left, .item-right {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.item-title {
  color: #151515;
  font-size: 28rpx;
  font-weight: 400;
  margin-left: 16rpx;
}
.item-sub {
  color: #181818;
  opacity: 0.64;
  font-size: 24rpx;
  margin-right: 16rpx;
}
</style>
```

---

## 4. 数据展示网格: FxDataGrid
常用于个人中心“我的数据”、面板首页统计等场景。水平排列 2~4 个数据项。

### 标准实现代码 (`components/FxDataGrid/FxDataGrid.uvue`)
```uvue
<template>
  <view class="fx-data-grid">
    <view class="grid-item" v-for="(item, index) in items" :key="index">
      <text class="item-value">{{ item.value }}</text>
      <text class="item-label">{{ item.label }}</text>
    </view>
  </view>
</template>

<script setup lang="uts">
type GridItem = {
  label: string;
  value: string;
}

defineProps({
  items: {
    type: Array as PropType<GridItem[]>,
    default: () => []
  }
});
</script>

<style scoped>
.fx-data-grid {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 16rpx 0;
}
.grid-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}
.item-value {
  color: #3F3536;
  font-size: 36rpx;
  font-weight: 600;
  margin-bottom: 8rpx;
}
.item-label {
  color: #847678;
  font-size: 24rpx;
  font-weight: 400;
}
</style>
```

当你用 FuturX 技能时，在生成的页面 (`.uvue`) 文件里遇到任何按钮、卡片或信息行，直接以上述现成组件的 `<fx-...>` 语法配合！并在未提供组件时把具体实现附上。

---

## 5. 底部导航栏: FxTabBar
标准底部导航，支持四个标签：训练、对话、工具、我的。

### 标准实现代码 (`components/FxTabBar/FxTabBar.uvue`)
```uvue
<template>
  <view class="tab-bar">
    <view class="tab-item" @click="switchTab('train')">
      <view :class="['tab-icon-wrap', activeTab === 'train' ? 'tab-icon-active' : '']">
        <image class="tab-icon" :src="activeTab === 'train' ? '/static/icons/tab-train-active.svg' : '/static/icons/tab-train.svg'" mode="aspectFit" />
      </view>
      <text :class="['tab-label', activeTab === 'train' ? 'tab-label-active' : '']">训练</text>
    </view>
    <view class="tab-item" @click="switchTab('chat')">
      <view :class="['tab-icon-wrap', activeTab === 'chat' ? 'tab-icon-active' : '']">
        <image class="tab-icon" :src="activeTab === 'chat' ? '/static/icons/tab-chat-active.svg' : '/static/icons/tab-chat.svg'" mode="aspectFit" />
      </view>
      <text :class="['tab-label', activeTab === 'chat' ? 'tab-label-active' : '']">对话</text>
    </view>
    <view class="tab-item" @click="switchTab('tools')">
      <view :class="['tab-icon-wrap', activeTab === 'tools' ? 'tab-icon-active' : '']">
        <image class="tab-icon" :src="activeTab === 'tools' ? '/static/icons/tab-tools-active.svg' : '/static/icons/tab-tools.svg'" mode="aspectFit" />
      </view>
      <text :class="['tab-label', activeTab === 'tools' ? 'tab-label-active' : '']">工具</text>
    </view>
    <view class="tab-item" @click="switchTab('profile')">
      <view :class="['tab-icon-wrap', activeTab === 'profile' ? 'tab-icon-active' : '']">
        <image class="tab-icon" :src="activeTab === 'profile' ? '/static/icons/tab-profile-active.svg' : '/static/icons/tab-profile.svg'" mode="aspectFit" />
      </view>
      <text :class="['tab-label', activeTab === 'profile' ? 'tab-label-active' : '']">我的</text>
    </view>
  </view>
</template>

<script setup lang="uts">
import { ref } from 'vue';

const emits = defineEmits(['change']);

const activeTab = ref<string>('train');

const switchTab = (tab: string) => {
  activeTab.value = tab;
  emits('change', tab);
};
</script>

<style scoped>
.tab-bar {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  height: 98rpx;
  background-color: #FFFFFF;
  border-top: 1rpx solid rgba(17, 0, 0, 0.04);
  padding-bottom: 16rpx;
}
.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
}
.tab-icon-wrap {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999rpx;
}
.tab-icon-active {
  background-color: #EB483F;
  width: 64rpx;
  height: 48rpx;
  border-radius: 999rpx;
}
.tab-icon {
  width: 48rpx;
  height: 48rpx;
}
.tab-label {
  margin-top: 4rpx;
  font-size: 22rpx;
  font-weight: 500;
  color: rgba(109, 55, 58, 0.6);
  letter-spacing: -0.6rpx;
  text-align: center;
}
.tab-label-active {
  color: #EB483F;
}
</style>
```

当你用 FuturX 技能时，在生成的页面 (`.uvue`) 文件里遇到需要生成底部导航的使用此组件，让用户手动把 Skill 中的 `assets/icons` 拷贝过去。

---

## 6. 对话气泡: FxChatBubble
用于 AI 和用户的对话消息展示。

### 标准实现代码 (`components/FxChatBubble/FxChatBubble.uvue`)
```uvue
<template>
  <view :class="['chat-bubble-container', isSelf ? 'chat-right' : 'chat-left']">
    <!-- 对方头像 -->
    <image v-if="!isSelf" class="avatar" :src="avatarUrl" mode="aspectFill" />
    
    <view class="msg-content">
      <view class="msg-header" v-if="!isSelf">
        <text class="msg-name">{{ name }}</text>
      </view>
      <view :class="['bubble', isSelf ? 'bubble-self' : 'bubble-other']">
        <text :class="['bubble-text', isSelf ? 'bubble-text-self' : 'bubble-text-other']">{{ content }}</text>
      </view>
      <!-- 底部时间和操作栏 -->
      <view class="msg-footer" v-if="!isSelf">
        <slot name="actions"></slot>
        <text class="msg-time">{{ time }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="uts">
defineProps({
  isSelf: { type: Boolean, default: false },
  content: { type: String, default: '' },
  name: { type: String, default: '' },
  avatarUrl: { type: String, default: '' },
  time: { type: String, default: '' }
});
</script>

<style scoped>
.chat-bubble-container {
  display: flex;
  flex-direction: row;
  margin-bottom: 32rpx;
  width: 100%;
}
.chat-right {
  justify-content: flex-end;
}
.chat-left {
  justify-content: flex-start;
}
.avatar {
  width: 40rpx;
  height: 40rpx;
  border-radius: 8rpx;
  margin-right: 16rpx;
}
.msg-content {
  display: flex;
  flex-direction: column;
  max-width: 70%;
}
.chat-right .msg-content {
  align-items: flex-end;
}
.msg-header {
  margin-bottom: 8rpx;
}
.msg-name {
  font-size: 26rpx;
  color: #3F3536;
  font-weight: 600;
}
.bubble {
  padding: 24rpx 32rpx;
  border-radius: 20rpx;
}
.bubble-self {
  background-color: #EB483F;
  border-bottom-right-radius: 4rpx; /* 自己发的气泡特点 */
}
.bubble-other {
  background-color: transparent;
  padding: 0;
}
.bubble-text {
  font-size: 30rpx;
  line-height: 1.5;
}
.bubble-text-self {
  color: #FFFFFF;
}
.bubble-text-other {
  color: #3F3536;
}
.msg-footer {
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 16rpx;
}
.msg-time {
  font-size: 24rpx;
  color: #847678;
  margin-left: 16rpx;
}
</style>
```

---

## 7. 语音输入底部操作栏: FxVoiceInput
沉浸式的底部声音/文字输入框。带有圆角白色透明包裹和居中的提示字眼，两边可带有功能图标。

### 标准实现代码 (`components/FxVoiceInput/FxVoiceInput.uvue`)
```uvue
<template>
  <view class="voice-input-container">
    <view class="voice-input-box">
      <view class="icon-btn left-icon">
        <slot name="left"></slot>
      </view>
      <text class="input-placeholder">按住 说话</text>
      <view class="icon-btn right-icon">
        <slot name="right"></slot>
      </view>
    </view>
  </view>
</template>

<style scoped>
.voice-input-container {
  width: 100%;
  padding: 16rpx 32rpx;
  background-color: transparent;
}
.voice-input-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 108rpx;
  border-radius: 54rpx;
  background-color: rgba(252, 252, 252, 0.9);
  box-shadow: 0 4rpx 32rpx 0 rgba(58, 35, 8, 0.05);
  border: 1rpx solid rgba(255, 255, 255, 0.5);
  padding: 0 32rpx;
}
.icon-btn {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}
.input-placeholder {
  color: #3F3536;
  font-size: 30rpx;
  font-weight: 500;
}
</style>
```
