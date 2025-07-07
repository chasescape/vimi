<!-- 人脸分析结果显示组件 -->
<template>
  <div class="face-analysis">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <span>分析中...</span>
    </div>
    
    <div v-else-if="analysisResult?.error" class="error">
      <i class="fas fa-exclamation-circle"></i>
      <span>{{ analysisResult.error }}</span>
    </div>
    
    <div v-else-if="analysisResult?.success" class="results">
      <div v-if="analysisResult.face_count === 0" class="no-face">
        <i class="fas fa-user-slash"></i>
        <p>未检测到人脸</p>
        <ul class="tips">
          <li>请确保正面对着摄像头</li>
          <li>保持适当的光线</li>
          <li>调整与摄像头的距离</li>
        </ul>
      </div>
      
      <div v-else class="face-info">
        <div class="face-count">
          <i class="fas fa-users"></i>
          <span>检测到 {{ analysisResult.face_count }} 个人脸</span>
        </div>
        
        <div v-for="(face, index) in analysisResult.faces" :key="index" class="face-details">
          <h4>人脸 {{ index + 1 }}</h4>
          <div class="properties">
            <div class="property">
              <i class="fas fa-smile"></i>
              <span>表情: {{ face.properties.expression }}</span>
            </div>
            <div class="property">
              <i class="fas fa-venus-mars"></i>
              <span>性别: {{ face.properties.gender }}</span>
            </div>
            <div class="property">
              <i class="fas fa-glasses"></i>
              <span>眼镜: {{ face.properties.glass }}</span>
            </div>
            <div class="property">
              <i class="fas fa-cut"></i>
              <span>发型: {{ face.properties.hair }}</span>
            </div>
            <div class="property">
              <i class="fas fa-user-tie"></i>
              <span>胡须: {{ face.properties.beard }}</span>
            </div>
            <div class="property">
              <i class="fas fa-head-side-mask"></i>
              <span>口罩: {{ face.properties.mask }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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

defineProps<{
  analysisResult: FaceAnalysisResult | null
  loading: boolean
}>()
</script>

<style scoped>
.face-analysis {
  padding: 20px;
  background: rgba(15, 15, 27, 0.7);
  border-radius: 10px;
  border: 1px solid rgba(76, 201, 240, 0.2);
}

.loading {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #4CC9F0;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff4757;
}

.no-face {
  text-align: center;
  color: #ffa800;
}

.no-face i {
  font-size: 32px;
  margin-bottom: 10px;
}

.tips {
  list-style: none;
  padding: 0;
  margin: 10px 0 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.tips li {
  margin: 5px 0;
}

.face-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.face-count {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #4CC9F0;
  font-size: 18px;
}

.face-details {
  background: rgba(76, 201, 240, 0.1);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
}

.face-details h4 {
  margin: 0 0 15px;
  color: #4CC9F0;
}

.properties {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
}

.property {
  display: flex;
  align-items: center;
  gap: 8px;
}

.property i {
  color: #4CC9F0;
  width: 20px;
  text-align: center;
}
</style> 