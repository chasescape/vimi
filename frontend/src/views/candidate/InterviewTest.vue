<template>
  <div class="interview-test-container p-6">
    <!-- 面试准备阶段 -->
    <div v-if="!isInterviewStarted" class="preparation-stage">
      <el-card class="mb-6">
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">面试准备</h2>
            <el-button type="primary" @click="startInterview" :disabled="!isReady">
              开始面试
            </el-button>
          </div>
        </template>

        <div class="preparation-steps">
          <!-- 设备检测 -->
          <div class="step-item mb-6">
            <h3 class="text-lg font-medium mb-4">1. 设备检测</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <el-card 
                v-for="device in devices" 
                :key="device.type"
                :class="{ 'border-green-500': device.status === 'success' }"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <el-icon :size="24" :class="device.status === 'success' ? 'text-green-500' : 'text-gray-400'">
                      <component :is="device.icon" />
                    </el-icon>
                    <span class="ml-2">{{ device.name }}</span>
                  </div>
                  <el-button 
                    :type="device.status === 'success' ? 'success' : 'primary'"
                    size="small"
                    @click="testDevice(device.type)"
                  >
                    {{ device.status === 'success' ? '已通过' : '测试' }}
                  </el-button>
                </div>
              </el-card>
            </div>
          </div>

          <!-- 面试设置 -->
          <div class="step-item mb-6">
            <h3 class="text-lg font-medium mb-4">2. 面试设置</h3>
            <el-form :model="interviewSettings" label-width="120px">
              <el-form-item label="面试岗位">
                <el-select v-model="interviewSettings.position" style="width: 100%">
                  <el-option
                    v-for="pos in positions"
                    :key="pos.value"
                    :label="pos.label"
                    :value="pos.value"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="面试时长">
                <el-select v-model="interviewSettings.duration" style="width: 100%">
                  <el-option label="15分钟" value="15" />
                  <el-option label="30分钟" value="30" />
                  <el-option label="45分钟" value="45" />
                  <el-option label="60分钟" value="60" />
                </el-select>
              </el-form-item>

              <el-form-item label="面试难度">
                <el-rate
                  v-model="interviewSettings.difficulty"
                  :max="3"
                  :texts="['入门', '进阶', '专家']"
                  show-text
                />
              </el-form-item>
            </el-form>
          </div>

          <!-- 注意事项 -->
          <div class="step-item">
            <h3 class="text-lg font-medium mb-4">3. 注意事项</h3>
            <el-alert
              v-for="(tip, index) in tips"
              :key="index"
              :title="tip"
              type="info"
              :closable="false"
              class="mb-2"
            />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 面试进行阶段 -->
    <div v-else class="interview-stage">
      <el-card class="mb-6">
        <template #header>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">模拟面试</h2>
            <div class="flex items-center gap-4">
              <span class="text-red-500">{{ formatTime(remainingTime) }}</span>
              <el-button type="danger" @click="endInterview">结束面试</el-button>
            </div>
          </div>
        </template>

        <div class="interview-content">
          <!-- 视频区域 -->
          <div class="video-container mb-6">
            <div class="grid grid-cols-2 gap-4">
              <div class="video-box bg-gray-100 rounded-lg aspect-video">
                <video ref="localVideo" autoplay muted playsinline></video>
              </div>
              <div class="video-box bg-gray-100 rounded-lg aspect-video">
                <video ref="remoteVideo" autoplay playsinline></video>
              </div>
            </div>
          </div>

          <!-- 问答区域 -->
          <div class="qa-container">
            <div class="question-box mb-4 p-4 bg-blue-50 rounded-lg">
              <h4 class="font-medium mb-2">当前问题：</h4>
              <p>{{ currentQuestion }}</p>
            </div>

            <div class="answer-box">
              <el-input
                v-model="currentAnswer"
                type="textarea"
                :rows="4"
                placeholder="请说出您的答案..."
                :disabled="true"
              />
              <div class="flex justify-end mt-4">
                <el-button type="primary" @click="submitAnswer">提交答案</el-button>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 设备测试对话框 -->
    <el-dialog
      v-model="showDeviceTest"
      :title="currentDevice?.name + '测试'"
      width="500px"
    >
      <div class="device-test-content">
        <div v-if="currentDevice?.type === 'camera'" class="camera-test">
          <video ref="testVideo" autoplay muted playsinline class="w-full rounded-lg"></video>
        </div>
        <div v-else-if="currentDevice?.type === 'microphone'" class="mic-test">
          <el-progress :percentage="audioLevel" :format="() => audioLevel + 'dB'" />
        </div>
        <div v-else-if="currentDevice?.type === 'speaker'" class="speaker-test">
          <el-button type="primary" @click="playTestSound">
            播放测试音频
          </el-button>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeviceTest = false">取消</el-button>
          <el-button type="primary" @click="confirmDeviceTest">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Microphone,
  VideoCamera,
  VideoPlay
} from '@element-plus/icons-vue'

// 设备状态
const devices = ref([
  { type: 'camera', name: '摄像头', icon: VideoCamera, status: 'pending' },
  { type: 'microphone', name: '麦克风', icon: Microphone, status: 'pending' },
  { type: 'speaker', name: '扬声器', icon: VideoPlay, status: 'pending' }
])

// 面试设置
const interviewSettings = ref({
  position: '',
  duration: '30',
  difficulty: 1
})

// 岗位选项
const positions = [
  { value: 'frontend', label: '前端开发工程师' },
  { value: 'backend', label: '后端开发工程师' },
  { value: 'fullstack', label: '全栈开发工程师' },
  { value: 'android', label: 'Android开发工程师' },
  { value: 'ios', label: 'iOS开发工程师' }
]

// 注意事项
const tips = [
  '请确保网络连接稳定，建议使用有线网络',
  '面试过程中请保持安静的环境',
  '请注意仪容仪表，保持专业形象',
  '回答问题时请言简意赅，突出重点'
]

// 设备测试相关
const showDeviceTest = ref(false)
const currentDevice = ref(null)
const testVideo = ref(null)
const audioLevel = ref(0)
let audioContext = null
let audioStream = null

// 面试状态
const isInterviewStarted = ref(false)
const remainingTime = ref(0)
const currentQuestion = ref('请简单介绍一下你自己')
const currentAnswer = ref('')
let timer = null

// 视频相关
const localVideo = ref(null)
const remoteVideo = ref(null)
let localStream = null

// 计算是否准备就绪
const isReady = computed(() => {
  return devices.value.every(d => d.status === 'success') &&
         interviewSettings.value.position &&
         interviewSettings.value.duration
})

// 测试设备
const testDevice = async (type) => {
  currentDevice.value = devices.value.find(d => d.type === type)
  showDeviceTest.value = true

  try {
    if (type === 'camera') {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      testVideo.value.srcObject = stream
      localStream = stream
    } else if (type === 'microphone') {
      audioStream = await navigator.mediaDevices.getUserMedia({ audio: true })
      startAudioTest()
    }
  } catch (error) {
    ElMessage.error('设备访问失败，请检查设备权限')
  }
}

// 确认设备测试
const confirmDeviceTest = () => {
  if (currentDevice.value) {
    const index = devices.value.findIndex(d => d.type === currentDevice.value.type)
    devices.value[index].status = 'success'
  }
  showDeviceTest.value = false
  stopDeviceTest()
}

// 停止设备测试
const stopDeviceTest = () => {
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop())
  }
  if (audioStream) {
    audioStream.getTracks().forEach(track => track.stop())
  }
  if (audioContext) {
    audioContext.close()
    audioContext = null
  }
}

// 开始音频测试
const startAudioTest = () => {
  audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const analyser = audioContext.createAnalyser()
  const microphone = audioContext.createMediaStreamSource(audioStream)
  microphone.connect(analyser)
  
  analyser.fftSize = 256
  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)

  const updateAudioLevel = () => {
    analyser.getByteFrequencyData(dataArray)
    const average = dataArray.reduce((a, b) => a + b) / bufferLength
    audioLevel.value = Math.round(average)
    if (showDeviceTest.value) {
      requestAnimationFrame(updateAudioLevel)
    }
  }
  updateAudioLevel()
}

// 播放测试音频
const playTestSound = () => {
  const audio = new Audio('/test-sound.mp3')
  audio.play()
}

// 格式化时间
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 开始面试
const startInterview = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: true,
      audio: true 
    })
    localVideo.value.srcObject = stream
    isInterviewStarted.value = true
    remainingTime.value = parseInt(interviewSettings.value.duration) * 60
    
    timer = setInterval(() => {
      if (remainingTime.value > 0) {
        remainingTime.value--
      } else {
        endInterview()
      }
    }, 1000)
  } catch (error) {
    ElMessage.error('无法访问摄像头或麦克风')
  }
}

// 结束面试
const endInterview = async () => {
  try {
    await ElMessageBox.confirm('确定要结束面试吗？', '提示', {
      type: 'warning'
    })
    
    if (timer) {
      clearInterval(timer)
    }
    if (localVideo.value?.srcObject) {
      localVideo.value.srcObject.getTracks().forEach(track => track.stop())
    }
    isInterviewStarted.value = false
    ElMessage.success('面试已结束')
    // 这里可以添加跳转到结果页面的逻辑
  } catch {
    // 用户取消操作
  }
}

// 提交答案
const submitAnswer = () => {
  // 这里添加答案提交逻辑
  ElMessage.success('答案已提交')
  currentAnswer.value = ''
  currentQuestion.value = '请描述一下你最近做过的一个项目'
}

// 组件卸载时清理资源
onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
  stopDeviceTest()
})
</script>

<style scoped>
.video-box {
  position: relative;
  overflow: hidden;
}

.video-box video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.device-test-content {
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-test video {
  width: 100%;
  border-radius: 8px;
}

.mic-test {
  width: 100%;
  padding: 20px;
}

.speaker-test {
  text-align: center;
}
</style>