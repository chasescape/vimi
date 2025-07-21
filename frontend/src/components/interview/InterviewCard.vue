<template>
  <div 
    class="card-item bg-white rounded-lg shadow-md p-4 w-64 transition-all duration-300 cursor-pointer hover:bg-blue-50"
    @click="handleClick"
  >
    <img 
      :src="item.cover"
      class="w-full h-32 object-cover rounded-lg mb-4"
      alt="面试封面"
    />
    <h4 class="font-medium mb-2">{{ item.title }}</h4>
    <div class="flex items-center text-sm text-gray-500">
      <el-icon class="mr-2"><Calendar /></el-icon>
      <span>{{ formattedTime }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Calendar } from '@element-plus/icons-vue'
import { defineProps, computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const formattedTime = computed(() => 
  props.item.time.split('T')[1].slice(0,5)
)

const handleClick = () => {
  window.open(`/candidate/interview-page?title=${props.item.title}`)
}
</script>

<style scoped>
.card-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.1);
}
</style>