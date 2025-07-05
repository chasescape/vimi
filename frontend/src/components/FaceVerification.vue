<!-- FaceVerification.vue -->
<template>
  <div class="face-verification">
    <div class="camera-container" v-if="!verificationResult">
      <video ref="video" :width="640" :height="480" autoplay></video>
      <canvas ref="canvas" style="display: none"></canvas>
      <div class="controls">
        <el-button type="primary" @click="captureAndVerify" :loading="loading">
          拍照并验证
        </el-button>
      </div>
    </div>

    <div v-else class="result-container">
      <div class="result-icon">
        <i :class="resultIcon"></i>
      </div>
      <div class="result-text">{{ resultText }}</div>
      <div class="action-buttons">
        <el-button type="primary" @click="resetVerification">重新验证</el-button>
        <el-button 
          v-if="verificationResult === 'success'"
          type="success" 
          @click="$emit('start-interview')">
          开始面试
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRouter } from 'vue-router'

export default {
  name: 'FaceVerification',
  emits: ['verification-success', 'start-interview'],
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      stream: null,
      loading: false,
      verificationResult: null,
      confidence: 0
    }
  },
  computed: {
    resultIcon() {
      if (!this.verificationResult) return ''
      return this.verificationResult === 'success'
        ? 'el-icon-check success'
        : 'el-icon-close error'
    },
    resultText() {
      if (!this.verificationResult) return ''
      if (this.verificationResult === 'success') {
        return `验证通过！相似度: ${(this.confidence * 100).toFixed(2)}%`
      }
      return '验证失败，请重试'
    }
  },
  methods: {
    async initCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: 640,
            height: 480,
            facingMode: 'user'
          }
        })
        this.$refs.video.srcObject = this.stream
      } catch (error) {
        console.error('无法访问摄像头:', error)
        this.$message.error('无法访问摄像头，请确保已授权访问权限')
      }
    },
    async captureAndVerify() {
      if (!this.stream) {
        this.$message.error('摄像头未就绪')
        return
      }

      this.loading = true
      try {
        // 捕获视频帧
        const canvas = this.$refs.canvas
        const video = this.$refs.video
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        const context = canvas.getContext('2d')
        context.drawImage(video, 0, 0, canvas.width, canvas.height)

        // 获取图片数据
        const photoData = canvas.toDataURL('image/jpeg')

        // 发送到后端进行验证
        const response = await axios.post('/api/user/verify-face', {
          live_photo: photoData
        })

        if (response.data.success) {
          this.verificationResult = response.data.is_same_person ? 'success' : 'error'
          this.confidence = response.data.confidence
          if (response.data.is_same_person) {
            this.$emit('verification-success', { confidence: this.confidence })
          } else {
            this.$message.error('验证失败：不是同一个人')
          }
        } else {
          this.$message.error(response.data.error || '验证失败')
          this.verificationResult = 'error'
        }
      } catch (error) {
        console.error('验证过程出错:', error)
        this.$message.error(error.response?.data?.error || '验证失败，请重试')
        this.verificationResult = 'error'
      } finally {
        this.loading = false
      }
    },
    resetVerification() {
      this.verificationResult = null
      this.confidence = 0
      this.initCamera() // 重新初始化摄像头
    },
    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop())
        this.stream = null
      }
    }
  },
  mounted() {
    this.initCamera()
  },
  beforeDestroy() {
    this.stopCamera()
  }
}
</script>

<style scoped>
.face-verification {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.controls {
  margin-top: 20px;
}

.result-container {
  text-align: center;
}

.result-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.result-icon .success {
  color: #67c23a;
}

.result-icon .error {
  color: #f56c6c;
}

.result-text {
  font-size: 18px;
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

video {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style> 