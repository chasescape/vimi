<template>
  <div class="face-verification-modal" v-if="show">
    <div class="modal-content">
      <div class="modal-header">
        <h3>人脸对比验证</h3>
        <button class="close-btn" @click="handleClose">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="verification-container">
        <!-- 左侧：ID照片 -->
        <div class="photo-section">
          <h4>身份证照片</h4>
          <div class="photo-container">
            <img :src="idPhotoUrl" alt="身份证照片" v-if="idPhotoUrl">
            <div class="photo-placeholder" v-else>
              <i class="fas fa-id-card"></i>
              <p>请上传身份证照片</p>
            </div>
          </div>
          <input 
            type="file" 
            ref="idPhotoInput"
            @change="handleIdPhotoUpload"
            accept="image/*"
            style="display: none"
          >
          <button class="upload-btn" @click="triggerIdPhotoUpload">
            <i class="fas fa-upload"></i> 上传照片
          </button>
        </div>

        <!-- 右侧：实时摄像头 -->
        <div class="camera-section">
          <h4>实时人脸采集</h4>
          <div class="camera-container">
            <video 
              ref="videoElement"
              autoplay 
              playsinline
              class="camera-feed"
              v-show="cameraActive"
            ></video>
            <canvas 
              ref="canvasElement" 
              style="display: none"
            ></canvas>
            <div class="camera-placeholder" v-if="!cameraActive">
              <i class="fas fa-camera"></i>
              <p>等待开启摄像头</p>
            </div>
            <div class="face-frame" v-if="cameraActive"></div>
          </div>
          <div class="camera-controls">
            <button 
              class="control-btn" 
              @click="toggleCamera"
              :class="{'active': cameraActive}"
            >
              <i :class="cameraActive ? 'fas fa-video' : 'fas fa-video-slash'"></i>
              {{ cameraActive ? '关闭摄像头' : '开启摄像头' }}
            </button>
            <button 
              class="verify-btn"
              @click="startVerification"
              :disabled="!canVerify"
            >
              <i class="fas fa-check-circle"></i> 开始验证
            </button>
          </div>
        </div>
      </div>

      <!-- 验证结果 -->
      <div class="verification-result" v-if="verificationResult">
        <div :class="['result-box', verificationResult.success ? 'success' : 'error']">
          <i :class="verificationResult.success ? 'fas fa-check-circle' : 'fas fa-times-circle'"></i>
          <span>{{ verificationResult.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Props
const props = defineProps<{
  show: boolean
}>()

// Emits
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'verification-complete', result: boolean): void
}>()

// Refs
const videoElement = ref<HTMLVideoElement | null>(null)
const canvasElement = ref<HTMLCanvasElement | null>(null)
const idPhotoInput = ref<HTMLInputElement | null>(null)
const cameraActive = ref(false)
const idPhotoUrl = ref('')
const verificationResult = ref<{ success: boolean; message: string } | null>(null)
let mediaStream: MediaStream | null = null

// Computed
const canVerify = computed(() => {
  return cameraActive.value && idPhotoUrl.value
})

// Methods
const handleClose = () => {
  stopCamera()
  emit('close')
}

const triggerIdPhotoUpload = () => {
  idPhotoInput.value?.click()
}

const handleIdPhotoUpload = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    idPhotoUrl.value = URL.createObjectURL(file)
  }
}

const toggleCamera = async () => {
  if (cameraActive.value) {
    stopCamera()
  } else {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      })
      
      if (videoElement.value) {
        videoElement.value.srcObject = mediaStream
        cameraActive.value = true
      }
    } catch (error) {
      console.error('Error accessing camera:', error)
      alert('无法访问摄像头，请检查权限设置')
    }
  }
}

const stopCamera = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }
  cameraActive.value = false
}

const captureFrame = (): string | null => {
  if (!videoElement.value || !canvasElement.value) return null
  
  const video = videoElement.value
  const canvas = canvasElement.value
  const context = canvas.getContext('2d')
  
  if (!context) return null
  
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  
  return canvas.toDataURL('image/jpeg')
}

const startVerification = async () => {
  if (!canVerify.value) return
  
  const frameData = captureFrame()
  if (!frameData) {
    alert('无法捕获摄像头画面')
    return
  }

  try {
    // TODO: 调用后端API进行人脸对比
    // 这里模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    const success = true // 模拟验证结果
    verificationResult.value = {
      success,
      message: success ? '验证通过！身份匹配成功' : '验证失败！请确保光线充足且正面对着摄像头'
    }
    
    emit('verification-complete', success)
    
    if (success) {
      setTimeout(() => {
        handleClose()
      }, 2000)
    }
  } catch (error) {
    console.error('Verification failed:', error)
    verificationResult.value = {
      success: false,
      message: '验证过程出现错误，请重试'
    }
  }
}

// 组件卸载时清理资源
onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>
.face-verification-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 900px;
  background: var(--bg-color, #1a1a2e);
  border-radius: 15px;
  border: 1px solid var(--border-color, rgba(76, 201, 240, 0.2));
  padding: 25px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  color: var(--text-color, #fff);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-color, #fff);
  cursor: pointer;
  font-size: 1.2em;
}

.verification-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.photo-section, .camera-section {
  background: var(--bg-color-light, rgba(26, 26, 46, 0.8));
  border-radius: 10px;
  padding: 20px;
}

h4 {
  color: var(--text-color, #fff);
  margin: 0 0 15px 0;
}

.photo-container, .camera-container {
  width: 100%;
  aspect-ratio: 4/3;
  background: var(--bg-color-dark, rgba(0, 0, 0, 0.3));
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  margin-bottom: 15px;
}

.photo-placeholder, .camera-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-color-light, rgba(255, 255, 255, 0.6));
}

.photo-placeholder i, .camera-placeholder i {
  font-size: 2em;
  margin-bottom: 10px;
}

img, .camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-btn, .control-btn, .verify-btn {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid var(--primary-color, #4CC9F0);
  background: var(--btn-bg, rgba(76, 201, 240, 0.1));
  color: var(--text-color, #fff);
  cursor: pointer;
  transition: all 0.3s;
}

.upload-btn:hover, .control-btn:hover, .verify-btn:hover {
  background: var(--btn-bg-hover, rgba(76, 201, 240, 0.2));
}

.camera-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.control-btn.active {
  background: var(--primary-color, #4CC9F0);
  color: #000;
}

.verify-btn {
  background: var(--success-color, #2ed573);
  border-color: var(--success-color, #2ed573);
}

.verify-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.face-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  border: 2px solid var(--primary-color, #4CC9F0);
  border-radius: 50%;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
}

.verification-result {
  margin-top: 20px;
}

.result-box {
  padding: 15px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.result-box.success {
  background: rgba(46, 213, 115, 0.1);
  color: #2ed573;
}

.result-box.error {
  background: rgba(255, 71, 87, 0.1);
  color: #ff4757;
}

.result-box i {
  font-size: 1.2em;
}

@media (max-width: 992px) {
  .modal-content {
    width: 95%;
    max-width: 600px;
  }

  .verification-container {
    grid-template-columns: 1fr;
  }
}
</style> 