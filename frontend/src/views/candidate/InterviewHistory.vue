<template>
  <div>
    <h3>人脸比对认证</h3>

    <button @click="startCamera">打开摄像头</button>
    <video ref="video" autoplay playsinline width="320" height="240" style="border:1px solid #ccc;"></video>
    <canvas ref="canvas" width="320" height="240" style="display:none;"></canvas>
    
    <div>
      <button @click="takePhoto" :disabled="!cameraStarted">拍照比对</button>
    </div>

    <div v-if="resultMessage" style="margin-top:20px;">{{ resultMessage }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userId: '1',  // 这里写真实用户ID，或者从上下文传入
      cameraStarted: false,
      idPhotoBase64: '',
      resultMessage: ''
    }
  },
  methods: {
    async startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        this.$refs.video.srcObject = stream
        this.cameraStarted = true
      } catch (e) {
        alert('打开摄像头失败：' + e.message)
      }
    },
    async getIdPhotoBase64() {
      // 从后端接口获取证件照 URL
      const res = await fetch(`/api/user/id_photo?user_id=${this.userId}`)
      const data = await res.json()
      if (!data.photo_url) throw new Error('未获取到证件照URL')

      // 下载图片并转Base64
      const resp = await fetch(data.photo_url)
      const blob = await resp.blob()
      return await this.blobToBase64(blob)
    },
    blobToBase64(blob) {
      return new Promise(resolve => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result.split(',')[1])  // 去掉 base64前缀
        reader.readAsDataURL(blob)
      })
    },
    async takePhoto() {
      if (!this.cameraStarted) {
        alert('请先打开摄像头')
        return
      }

      try {
        this.resultMessage = '获取证件照...'
        this.idPhotoBase64 = await this.getIdPhotoBase64()

        // 拍摄当前视频帧
        const video = this.$refs.video
        const canvas = this.$refs.canvas
        const ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
        const livePhotoBase64 = canvas.toDataURL('image/jpeg').split(',')[1] // 去掉前缀

        this.resultMessage = '发送比对请求...'

        // 调用后端接口，传两个Base64字符串
        const resp = await fetch('/face_compare_base64', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id_photo_base64: this.idPhotoBase64,
            live_photo_base64: livePhotoBase64,
            user_id: this.userId
          })
        })
        const result = await resp.json()

        if (resp.ok && result.same_person) {
          this.resultMessage = `比对通过！相似度：${result.score}`
          // 跳转会议页面
          window.location.href = `/meeting?user_id=${this.userId}`
        } else {
          this.resultMessage = `比对未通过，相似度：${result.score || 0}，请重试。`
        }

      } catch (e) {
        this.resultMessage = '比对失败：' + e.message
      }
    }
  }
}
</script>
