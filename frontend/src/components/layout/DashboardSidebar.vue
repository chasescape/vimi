<template>
    <!-- 仅在外层侧边栏显示指示条 -->
    <div
      v-if="isRoot"
      class="absolute left-0 w-1 h-8 bg-blue-600 rounded-r transition-all duration-300"
      :style="indicatorStyle"
    ></div>
  <div class="relative h-full overflow-y-auto" ref="sidebarContainer">
    <div 
      v-for="(item, index) in items" 
      :key="index"
      class="group"
      :data-route="item.route"
      :ref="el => registerItem(el, item.route)"
    >
      <!-- 菜单项结构保持不变 -->
      <div
        :class="[
          'px-4 py-3 cursor-pointer transition-all relative',
          activeRoute === item.route ? 'text-blue-600 bg-blue-50' : 'hover:bg-gray-100'
        ]"
        @click="handleItemClick(item)"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <el-icon v-if="item.icon" :size="20" :class="activeRoute === item.route ? 'text-blue-600' : 'text-black'">
              <component :is="item.icon" />
            </el-icon>
            <span class="text-sm font-medium text-black">{{ item.title }}</span>
          </div>
          <el-icon
            v-if="item.children?.length"
            :size="14"
            :class="[
              'transform transition-transform text-black',
              expandedPaths.includes(item.route) ? 'rotate-90' : ''
            ]"
          >
            <ArrowRight />
          </el-icon>
        </div>
      </div>

      <div
        v-if="item.children?.length"
        :class="[
          'overflow-hidden transition-all ml-4 border-l-2 border-gray-200',
          expandedPaths.includes(item.route) ? 'max-h-96' : 'max-h-0'
        ]"
      >
        <DashboardSidebar
          :items="item.children"
          :active-route="activeRoute"
          @navigate="handleChildNavigate"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, provide, inject, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from '@element-plus/icons-vue'

// 新增状态管理
const activeElementPath = inject('active-element-path', ref<string[]>([]))
provide('active-element-path', activeElementPath)

interface MenuItem {
  title: string;
  icon?: any;
  route?: string;
  children?: MenuItem[];
}

// 新增属性
const props = defineProps({
  items: {
    type: Array as () => MenuItem[],
    required: true
  },
  activeRoute: {
    type: String,
    required: true
  },
  isRoot: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()
const sidebarContainer = ref<HTMLElement | null>(null)
const expandedPaths = ref<string[]>([])
const indicatorStyle = ref({ transform: 'translateY(0)' })

const updateIndicatorPosition = async () => {
  await nextTick()
  const activeElement = document.querySelector(`[data-route="${props.activeRoute}"]`)
  if (activeElement && sidebarContainer.value) {
    const containerTop = sidebarContainer.value.getBoundingClientRect().top
    const elementTop = activeElement.getBoundingClientRect().top
    indicatorStyle.value = {
      transform: `translateY(${elementTop - containerTop}px)`
    }
  }
}

watch(() => props.activeRoute, updateIndicatorPosition, { immediate: true })

// 新增展开状态追踪
const expandedSet = inject('expanded-set', ref(new Set<string>()))
provide('expanded-set', expandedSet)

// 新增：获取当前路由的所有父级路径
const getParentRoutes = (items: any[], targetRoute: string, path: string[] = []): string[] => {
  for (const item of items) {
    if (item.route === targetRoute) return [...path, item.route]
    if (item.children) {
      const found = getParentRoutes(item.children, targetRoute, [...path, item.route])
      if (found.length) return found
    }
  }
  return []
}

// 修改：增强路由监听
watch(() => props.activeRoute, (newRoute) => {
  // 自动展开所有父级菜单
  const parentRoutes = getParentRoutes(props.items, newRoute)
  expandedPaths.value = [...new Set([...expandedPaths.value, ...parentRoutes])]
  
  updateIndicatorPosition()
}, { immediate: true })

// 修改：处理菜单点击逻辑
const handleItemClick = async (item: any) => {
  if (item.children?.length) {
    // 如果当前路由属于该菜单的子项，则禁止折叠
    const isActiveParent = getParentRoutes(props.items, props.activeRoute).includes(item.route)
    if (isActiveParent) return
    
    const index = expandedPaths.value.indexOf(item.route)
    index === -1 ? expandedPaths.value.push(item.route) : expandedPaths.value.splice(index, 1)
    
    await new Promise(resolve => setTimeout(resolve, 300))
    calculatePosition()
  } else {
    router.push(item.route)
  }
}

// 优化后的位置计算
const calculatePosition = async () => {
  await nextTick()
  const activeItem = itemElements.value.find(i => i.route === props.activeRoute)
  
  if (!activeItem?.el || !sidebarContainer.value) return

  // 检查所有父级是否展开
  let parent = activeItem.el.parentElement
  while (parent && parent !== sidebarContainer.value) {
    const parentRoute = parent.dataset.route
    if (parentRoute && !expandedSet.value.has(parentRoute)) {
      return // 如果父级未展开则跳过计算
    }
    parent = parent.parentElement
  }

  const containerRect = sidebarContainer.value.getBoundingClientRect()
  const itemRect = activeItem.el.getBoundingClientRect()
  const relativeTop = itemRect.top - containerRect.top

  indicatorStyle.value = {
    transform: `translateY(${relativeTop}px)`,
    height: `${activeItem.el.clientHeight}px`
  }
}


// 增强的MutationObserver配置
const observer = new MutationObserver((mutations) => {
  if (mutations.some(m => m.type === 'childList')) {
    calculatePosition()
  }
})

onMounted(() => {
  if (sidebarContainer.value) {
    observer.observe(sidebarContainer.value, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['style'] // 监听折叠动画
    })
  }
})

onBeforeUnmount(() => {
  observer.disconnect()
})

const handleChildNavigate = (route: string) => {
  router.push(route)
}

// 新增DOM元素注册
const itemElements = ref<{route: string, el: HTMLElement}[]>([])
const registerItem = (el: HTMLElement, route: string) => {
  if (el) itemElements.value.push({ route, el })
}

// 获取元素层级路径
const getElementPath = (el: HTMLElement): string[] => {
  const path: string[] = []
  let current: HTMLElement | null = el
  
  while (current && current !== sidebarContainer.value) {
    const route = current.dataset.route
    if (route) path.unshift(route)
    current = current.parentElement
  }
  
  return path
}

// // 使用MutationObserver监听DOM变化
// const observer = new MutationObserver(calculatePosition)
// onMounted(() => {
//   if (sidebarContainer.value) {
//     observer.observe(sidebarContainer.value, {
//       childList: true,
//       subtree: true
//     })
//   }
// })
</script>

<style scoped>
/* 自定义滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2d3748;
}

/* 激活状态的菜单项样式 */
.router-link-active {
  @apply text-blue-600 bg-blue-50;
}

/* 菜单项悬停效果 */
.group:hover > div {
  @apply bg-gray-100;
}
</style>