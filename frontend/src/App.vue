<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const route = useRoute()

// 需要缓存的组件名称列表
const keepAliveComponents = computed(() => {
  if (route.meta.keepAlive) {
    return [route.name as string]
  }
  return []
})
</script>

<template>
  <el-config-provider :locale="zhCn">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <keep-alive :include="keepAliveComponents">
          <component :is="Component" />
        </keep-alive>
      </transition>
    </router-view>
  </el-config-provider>
</template>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  height: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
