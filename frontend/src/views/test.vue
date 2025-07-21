<template>
  <div class="video-container">
    <video
      ref="localVideo"
      autoplay
      playsinline
      muted
      class="video-element"
    ></video>
    
    <div class="analysis-results" v-if="faceAnalysisResult">
      <div v-if="faceAnalysisResult.error" class="error">
        {{ faceAnalysisResult.error }}
      </div>
      <div v-else>
        检测到 {{ faceAnalysisResult.face_count }} 个人脸
        <div v-for="(face, index) in faceAnalysisResult.faces" :key="index">
          <div>表情: {{ face.properties.expression }}</div>
          <div>性别: {{ face.properties.gender }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-container {
  width: 100%;
  height: 100vh;
  position: relative;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.analysis-results {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 15px;
  border-radius: 8px;
}

.error {
  color: #ff4757;
}
</style>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { detectFace } from '../api/ai'

const localVideo = ref<HTMLVideoElement | null>(null)
const localStream = ref<MediaStream | null>(null)

interface FaceLocation {
  x: number
  y: number
  width: number
  height: number
}

interface FaceProperties {
  expression: string
  gender: string
  glass: string
  hair: string
  beard: string
  mask: string
}

interface Face {
  score: number
  location: FaceLocation
  properties: FaceProperties
}

interface FaceAnalysisResult {
  success: boolean
  face_count: number
  faces: Face[]
  error?: string
}

const faceAnalysisResult = ref<FaceAnalysisResult | null>(null)
let analysisTimer: ReturnType<typeof setInterval> | null = null

// 分析人脸
const analyzeFace = async () => {
  try {
    if (!localVideo.value || !localStream.value) {
      console.warn('视频流未就绪')
      return
    }

    const video = localVideo.value
    
    // 确保视频已经准备好
    if (!video.videoWidth || !video.videoHeight || video.readyState < video.HAVE_ENOUGH_DATA) {
      console.warn('视频尚未准备好，等待中...')
      return
    }

    // 使用视频的实际尺寸
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    if (!ctx) {
      console.error('无法获取canvas上下文')
      return
    }

    // 使用更高质量的图像渲染
    ctx.imageSmoothingEnabled = true
    ctx.imageSmoothingQuality = 'high'

    // 截取视频帧
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    // 转换为base64
    const imageData = canvas.toDataURL('image/jpeg', 0.9)
    
    // 调用人脸检测API
    const apiResult = await detectFace(imageData)
    faceAnalysisResult.value = apiResult

  } catch (error) {
    console.error('分析失败:', error)
    faceAnalysisResult.value = {
      success: false,
      face_count: 0,
      faces: [],
      error: error instanceof Error ? error.message : '分析失败'
    }
  }
}

// 启动视频流
const startVideo = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 15 }
      }
    })
    
    if (localVideo.value) {
      localVideo.value.srcObject = stream
      localStream.value = stream
      
      // 等待视频加载
      await localVideo.value.play()
      
      // 开始定时分析
      analysisTimer = setInterval(analyzeFace, 2000) // 每2秒分析一次
    }
  } catch (error) {
    console.error('启动摄像头失败:', error)
    alert('启动摄像头失败，请检查设备权限设置')
  }
}

onMounted(() => {
  startVideo()
})

onUnmounted(() => {
  if (analysisTimer) {
    clearInterval(analysisTimer)
  }
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
  }
})
</script> 