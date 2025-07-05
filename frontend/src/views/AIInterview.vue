<template>
  <div class="interview-container">
    <!-- 背景效果 -->
    <div class="cyber-grid"></div>
    <div class="cyber-pulse"></div>
    <div class="cyber-orb" style="top: 10%; left: 10%;"></div>
    <div class="cyber-orb" style="top: 70%; left: 80%;"></div>

    <!-- 顶部导航 -->
    <header class="top-bar">
      <div class="left">
        <button class="icon-btn" @click="goBack">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1>AI智能面试</h1>
      </div>
      <div class="right">
        <span class="interview-id">面试ID: AI-2024-001</span>
        <button class="icon-btn">
          <i class="fas fa-cog"></i>
        </button>
      </div>
    </header>

    <!-- 主要内容区 -->
    <main class="main-content">
      <!-- 左侧候选人列表 -->
      <aside class="candidate-list">
        <div class="list-header">
          <h2>面试进度</h2>
          <div class="stats">
            <div class="stat-item">
              <span class="number">42</span>
              <span class="label">候选人</span>
            </div>
            <div class="stat-item">
              <span class="number">12</span>
              <span class="label">已完成</span>
            </div>
            <div class="stat-item">
              <span class="number">6</span>
              <span class="label">待面试</span>
            </div>
          </div>
        </div>

        <!-- 面试官和虚拟人视频区 -->
        <div class="interviewers">
          <!-- 面试官视频 -->
          <div class="interviewer-box">
            <div class="video-wrapper">
              <div class="video-placeholder">
                <i class="fas fa-user-tie"></i>
                <p>面试官</p>
              </div>
            </div>
            <div class="name-tag">面试官 - 张教授</div>
          </div>

          <!-- 虚拟人视频 -->
          <div class="interviewer-box">
            <div class="video-wrapper">
              <div class="video-placeholder">
                <i class="fas fa-robot"></i>
                <p>AI面试官</p>
              </div>
            </div>
            <div class="name-tag">AI助理 - Eva</div>
          </div>
        </div>

        <div class="candidates">
          <div class="candidate-item active">
            <img src="https://placeholder.com/40" alt="候选人头像" />
            <div class="info">
              <span class="name">张三</span>
              <span class="position">前端开发</span>
            </div>
            <span class="status">进行中</span>
          </div>
          <!-- 更多候选人... -->
        </div>
      </aside>

      <!-- 中间视频区域 -->
      <section class="video-section">
        <div class="main-video">
          <!-- 考生视频 -->
          <div class="video-container">
            <div class="video-wrapper">
              <video 
                ref="localVideo" 
                autoplay 
                playsinline 
                muted 
                class="video-element"
              ></video>
              <div class="video-placeholder" v-if="!localStream">
                <i class="fas fa-video"></i>
                <p>等待开启摄像头</p>
              </div>
            </div>
            <div class="name-tag">考生</div>
          </div>
          
          <!-- 字幕区域 -->
          <div class="caption-section">
            <div class="caption-container">
              <div class="caption-icon">
                <i class="fas fa-comment-alt"></i>
              </div>
              <div class="caption-content">
                <div class="caption-text">正在说话的内容会显示在这里...</div>
                <div class="caption-wave">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 视频控制栏 -->
          <div class="video-controls">
            <div class="left-controls">
              <button class="control-btn">
                <i class="fas fa-microphone"></i>
              </button>
              <button class="control-btn">
                <i class="fas fa-video"></i>
              </button>
              <button class="control-btn">
                <i class="fas fa-desktop"></i>
              </button>
            </div>
            <div class="center-controls">
              <button class="time-indicator">00:00</button>
            </div>
            <div class="right-controls">
              <button class="control-btn">
                <i class="fas fa-closed-captioning"></i>
              </button>
              <button class="control-btn">
                <i class="fas fa-expand"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 底部信息区 -->
        <div class="interview-info">
          <div class="tabs">
            <button class="tab-btn active">面试概要</button>
            <button class="tab-btn">实时记录</button>
            <button class="tab-btn">候选人信息</button>
            <button class="tab-btn">评估结果</button>
          </div>
          
          <div class="tab-content">
            <!-- 软技能评估 -->
            <div class="skills-assessment">
              <h3>软技能评估</h3>
              <div class="skill-bars">
                <div class="skill-bar">
                  <span class="skill-name">沟通能力</span>
                  <div class="bar">
                    <div class="progress" style="width: 85%"></div>
                  </div>
                  <span class="percentage">85%</span>
                </div>
                <div class="skill-bar">
                  <span class="skill-name">逻辑思维</span>
                  <div class="bar">
                    <div class="progress" style="width: 75%"></div>
                  </div>
                  <span class="percentage">75%</span>
                </div>
                <!-- 更多技能条... -->
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 右侧工具栏 -->
      <aside class="tools-panel">
        <div class="tools-header">
          <h2>AI 工具</h2>
        </div>
        
        <div class="tools-list">
          <button class="tool-btn">
            <i class="fas fa-brain"></i>
            <span>面试分析</span>
          </button>
          <button class="tool-btn">
            <i class="fas fa-eye"></i>
            <span>表情检测</span>
          </button>
          <button class="tool-btn">
            <i class="fas fa-keyboard"></i>
            <span>关键词匹配</span>
          </button>
          <button class="tool-btn">
            <i class="fas fa-chart-line"></i>
            <span>表现评估</span>
          </button>
        </div>

        <div class="interview-chat">
          <div class="chat-messages">
            <div class="message">
              <img src="https://placeholder.com/30" alt="AI头像" />
              <div class="message-content">
                <p>请做一个简单的自我介绍</p>
              </div>
            </div>
            <!-- 更多消息... -->
          </div>
          
          <div class="chat-input">
            <input type="text" placeholder="输入评论..." />
            <button class="send-btn">
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </aside>
    </main>

    <!-- 设备检测弹窗 -->
    <div class="modal device-check" v-if="showDeviceCheck">
      <div class="modal-content">
        <h2>设备检测</h2>
        
        <!-- 步骤指示器 -->
        <div class="steps">
          <div class="step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
            <div class="step-number">1</div>
            <div class="step-label">上传证件照</div>
          </div>
          <div class="step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
            <div class="step-number">2</div>
            <div class="step-label">设备检测</div>
          </div>
          <div class="step" :class="{ active: currentStep === 3, completed: currentStep > 3 }">
            <div class="step-number">3</div>
            <div class="step-label">身份验证</div>
          </div>
        </div>

        <!-- 步骤1: 上传证件照 -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="upload-section">
            <div class="upload-preview" 
                 :class="{ 'has-image': idPhotoUrl }"
                 @click="triggerFileInput">
              <img v-if="idPhotoUrl" :src="idPhotoUrl" alt="证件照预览" />
              <div v-else class="upload-placeholder">
                <i class="fas fa-id-card"></i>
                <p>点击上传证件照</p>
                <span>支持jpg、png格式</span>
              </div>
            </div>
            <input 
              type="file" 
              ref="fileInput" 
              accept="image/*" 
              style="display: none"
              @change="handleFileUpload"
            />
          </div>
          <div class="step-buttons">
            <button class="secondary-btn" @click="cancelDeviceCheck">取消</button>
            <button 
              class="primary-btn" 
              :disabled="!idPhotoUrl"
              @click="goToNextStep">
              下一步
            </button>
          </div>
        </div>

        <!-- 步骤2: 设备检测 -->
        <div v-if="currentStep === 2" class="step-content">
          <div class="device-list">
            <!-- 麦克风检测 -->
            <div class="device-item">
              <i class="fas fa-microphone"></i>
              <span>麦克风</span>
              <select v-model="deviceStatus.microphone.selectedId">
                <option v-for="device in deviceStatus.microphone.devices" 
                        :key="device.deviceId" 
                        :value="device.deviceId">
                  {{ device.label || '默认麦克风' }}
                </option>
              </select>
              <div class="test-controls">
                <button class="test-btn" 
                        @click="testMicrophone"
                        :class="{ 'testing': deviceStatus.microphone.testing }">
                  {{ deviceStatus.microphone.testing ? '停止' : '测试' }}
                </button>
                <div class="volume-indicator" v-if="deviceStatus.microphone.testing">
                  <div class="volume-bar" :style="{ width: microphoneVolume + '%' }"></div>
                </div>
              </div>
            </div>

            <!-- 摄像头检测 -->
            <div class="device-item">
              <i class="fas fa-video"></i>
              <span>摄像头</span>
              <select v-model="deviceStatus.camera.selectedId">
                <option v-for="device in deviceStatus.camera.devices" 
                        :key="device.deviceId" 
                        :value="device.deviceId">
                  {{ device.label || '默认摄像头' }}
                </option>
              </select>
              <div class="camera-preview" v-if="deviceStatus.camera.testing">
                <video ref="cameraPreview" autoplay playsinline muted></video>
              </div>
              <button class="test-btn" 
                      @click="testCamera"
                      :class="{ 'testing': deviceStatus.camera.testing }">
                {{ deviceStatus.camera.testing ? '停止' : '测试' }}
              </button>
            </div>

            <!-- 网络检测 -->
            <div class="device-item">
              <i class="fas fa-wifi"></i>
              <span>网络状态</span>
              <div class="status-container">
                <div class="status" :class="deviceStatus.network.status">
                  {{ deviceStatus.network.status === 'good' ? '良好' : 
                     deviceStatus.network.status === 'poor' ? '一般' : '差' }}
                </div>
                <div class="network-speed" v-if="deviceStatus.network.speed">
                  {{ deviceStatus.network.speed }} Mbps
                </div>
                <button class="test-btn" 
                        @click="testNetwork"
                        :disabled="deviceStatus.network.testing">
                  测试
                </button>
              </div>
            </div>
          </div>

          <div class="step-buttons">
            <button class="secondary-btn" @click="currentStep--">上一步</button>
            <button 
              class="primary-btn" 
              :disabled="!isDeviceTestComplete"
              @click="goToNextStep">
              下一步
            </button>
          </div>
        </div>

        <!-- 步骤3: 身份验证 -->
        <div v-if="currentStep === 3" class="step-content">
          <FaceVerification 
            @verification-success="handleVerificationSuccess"
            @start-interview="startInterview" 
          />
          
          <div class="step-buttons">
            <button class="secondary-btn" @click="currentStep--">上一步</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 面试界面 -->
    <div v-if="!showDeviceCheck" class="interview-container">
      <video ref="localVideo" autoplay playsinline muted></video>
    </div>
  </div>
</template>

<style scoped>
.interview-container {
  min-height: 100vh;
  background: #0f0f1b;
  color: #fff;
  position: relative;
  overflow: hidden;
}

/* 背景效果 */
.cyber-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(76, 201, 240, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(76, 201, 240, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 1;
  opacity: 0.3;
}

.cyber-pulse {
  position: fixed;
  width: 300vw;
  height: 300vh;
  left: -100vw;
  top: -100vh;
  background: radial-gradient(circle, rgba(67, 97, 238, 0.05) 0%, transparent 70%);
  animation: pulse 15s ease infinite;
  z-index: 2;
}

.cyber-orb {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(76, 201, 240, 0.1) 0%, transparent 70%);
  filter: blur(30px);
  z-index: 3;
}

/* 顶部导航 */
.top-bar {
  height: 60px;
  background: rgba(15, 15, 27, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  position: relative;
  z-index: 100;
  border-bottom: 1px solid rgba(76, 201, 240, 0.2);
}

.top-bar .left, .top-bar .right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(76, 201, 240, 0.3);
  background: rgba(76, 201, 240, 0.1);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.icon-btn:hover {
  background: rgba(76, 201, 240, 0.2);
}

/* 主要内容区 */
.main-content {
  display: grid;
  grid-template-columns: 300px minmax(600px, 1fr) 300px;
  gap: 20px;
  padding: 20px;
  height: calc(100vh - 60px);
  position: relative;
  z-index: 100;
}

/* 左侧候选人列表 */
.candidate-list {
  background: rgba(15, 15, 27, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
  backdrop-filter: blur(10px);
  padding: 20px;
}

.list-header {
  margin-bottom: 20px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.stat-item {
  text-align: center;
}

.number {
  font-size: 24px;
  font-weight: 600;
  color: #4CC9F0;
}

.label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.candidates {
  margin-top: 20px;
  max-height: 200px;
  overflow-y: auto;
}

.candidate-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.candidate-item:hover, .candidate-item.active {
  background: rgba(76, 201, 240, 0.1);
}

.candidate-item img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.info {
  flex: 1;
}

.name {
  font-weight: 500;
}

.position {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.status {
  font-size: 12px;
  color: #4CC9F0;
}

/* 中间视频区域 */
.video-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.main-video {
  flex: 1;
  min-height: 0; /* 防止溢出 */
  background: rgba(15, 15, 27, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
  backdrop-filter: blur(10px);
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

.video-container {
  flex: 1;
  min-height: 0; /* 防止溢出 */
  display: flex;
  flex-direction: column;
  background: rgba(15, 15, 27, 0.3);
}

.video-wrapper {
  flex: 1;
  position: relative;
}

.video-element {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #000;
}

.video-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  background: rgba(15, 15, 27, 0.3);
}

.video-placeholder i {
  font-size: 32px;
  margin-bottom: 10px;
}

.video-placeholder p {
  font-size: 14px;
}

.interviewer-video,
.virtual-interviewer,
.candidate-video {
  position: relative;
  height: 100%;
  background: rgba(15, 15, 27, 0.5);
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(76, 201, 240, 0.2);
}

.name-tag {
  height: 40px;
  background: rgba(15, 15, 27, 0.8);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  border-top: 1px solid rgba(76, 201, 240, 0.2);
}

.video-controls {
  height: 60px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid rgba(76, 201, 240, 0.2);
}

.left-controls, .right-controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(76, 201, 240, 0.3);
  background: rgba(76, 201, 240, 0.1);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.control-btn:hover {
  background: rgba(76, 201, 240, 0.2);
}

.time-indicator {
  background: none;
  border: none;
  color: #fff;
  font-family: monospace;
}

/* 面试信息区域 */
.interview-info {
  height: 200px; /* 固定高度 */
  background: rgba(15, 15, 27, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
  backdrop-filter: blur(10px);
  padding: 20px;
  overflow: hidden; /* 防止内容溢出 */
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-shrink: 0; /* 防止压缩 */
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  background: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.3s;
}

.tab-btn.active {
  color: #4CC9F0;
  border-bottom: 2px solid #4CC9F0;
}

.tab-content {
  flex: 1;
  overflow-y: auto; /* 内容过多时可滚动 */
  padding-right: 10px; /* 为滚动条留出空间 */
}

.skills-assessment {
  padding: 20px 0;
}

.skill-bars {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.skill-name {
  width: 80px;
  font-size: 14px;
}

.bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #4CC9F0, #4361EE);
  border-radius: 3px;
}

.percentage {
  width: 40px;
  font-size: 14px;
  text-align: right;
}

/* 右侧工具栏 */
.tools-panel {
  background: rgba(15, 15, 27, 0.7);
  border-radius: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
  backdrop-filter: blur(10px);
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.tools-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.tool-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 15px;
  border-radius: 10px;
  border: 1px solid rgba(76, 201, 240, 0.3);
  background: rgba(76, 201, 240, 0.1);
  color: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-btn:hover {
  background: rgba(76, 201, 240, 0.2);
}

.tool-btn i {
  font-size: 24px;
}

.tool-btn span {
  font-size: 12px;
}

.interview-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 20px;
  border-top: 1px solid rgba(76, 201, 240, 0.2);
  padding-top: 20px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.message img {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.message-content {
  background: rgba(76, 201, 240, 0.1);
  padding: 10px;
  border-radius: 10px;
  max-width: 80%;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 10px;
}

.chat-input input {
  flex: 1;
  padding: 8px 12px;
  border-radius: 20px;
  border: 1px solid rgba(76, 201, 240, 0.3);
  background: rgba(76, 201, 240, 0.1);
  color: #fff;
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #4CC9F0;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* 设备检测弹窗 */
.modal {
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
  width: 500px;
  background: rgba(15, 15, 27, 0.95);
  border-radius: 15px;
  border: 1px solid rgba(76, 201, 240, 0.2);
  padding: 30px;
}

.steps {
  display: flex;
  justify-content: space-between;
  margin: 20px 0 30px;
  position: relative;
}

.steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 40px;
  right: 40px;
  height: 2px;
  background: rgba(76, 201, 240, 0.1);
  z-index: 1;
}

.step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(76, 201, 240, 0.1);
  border: 2px solid rgba(76, 201, 240, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
}

.step.active .step-number {
  background: rgba(76, 201, 240, 0.2);
  border-color: #4CC9F0;
  color: #fff;
}

.step.completed .step-number {
  background: #4CC9F0;
  border-color: #4CC9F0;
  color: #fff;
}

.step-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.step.active .step-label,
.step.completed .step-label {
  color: #fff;
}

/* 上传区域样式 */
.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin: 30px 0;
}

.upload-preview {
  width: 240px;
  height: 320px;
  border: 2px dashed rgba(76, 201, 240, 0.3);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(76, 201, 240, 0.1);
}

.upload-preview:hover {
  border-color: #4CC9F0;
  background: rgba(76, 201, 240, 0.15);
}

.upload-preview.has-image {
  border-style: solid;
}

.upload-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-placeholder {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.upload-placeholder i {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-placeholder span {
  font-size: 12px;
  opacity: 0.6;
}

/* 设备测试样式 */
.test-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.volume-indicator {
  width: 100px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.volume-bar {
  height: 100%;
  background: linear-gradient(90deg, #4CC9F0, #4361EE);
  border-radius: 3px;
  transition: width 0.1s;
}

.camera-preview {
  width: 160px;
  height: 90px;
  background: #000;
  border-radius: 5px;
  overflow: hidden;
  margin: 10px 0;
}

.camera-preview video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 验证区域样式 */
.verify-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin: 20px 0;
}

.verify-preview {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.id-photo,
.live-photo {
  width: 200px;
  height: 260px;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(15, 15, 27, 0.5);
  position: relative;
}

.id-photo img,
.live-photo img,
.live-photo video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.id-photo span,
.live-photo span {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px;
  background: rgba(15, 15, 27, 0.8);
  color: #fff;
  font-size: 12px;
  text-align: center;
}

.verify-status {
  text-align: center;
}

.status-text {
  font-size: 16px;
  margin-bottom: 8px;
}

.status-text.verifying {
  color: #4CC9F0;
}

.status-text.success {
  color: #2ed573;
}

.status-text.error {
  color: #ff4757;
}

.confidence {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.verify-btn {
  padding: 12px 24px;
  border-radius: 5px;
  background: #4CC9F0;
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.verify-btn:hover:not(:disabled) {
  background: #3ab9e0;
}

.verify-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.verify-btn.verifying {
  background: #ff4757;
}

/* 步骤按钮样式 */
.step-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.step-content {
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

@keyframes pulse {
  0% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1); opacity: 0.2; }
  100% { transform: scale(0.8); opacity: 0.5; }
}

/* 响应式调整 */
@media (max-width: 1400px) {
  .main-content {
    grid-template-columns: 250px minmax(500px, 1fr) 250px;
  }
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 200px minmax(400px, 1fr) 200px;
  }
}

@media (max-width: 992px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .candidate-list, .tools-panel {
    display: none;
  }

  .interview-info {
    height: 180px;
  }

  .caption-section {
    padding: 10px 15px;
  }

  .caption-container {
    padding: 10px;
  }

  .caption-icon {
    width: 28px;
    height: 28px;
  }

  .caption-text {
    font-size: 13px;
  }
}

.device-item .status-container {
  flex: 1;
  display: flex;
  gap: 10px;
  align-items: center;
}

.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status.good {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
}

.status.poor {
  background: rgba(255, 168, 0, 0.2);
  color: #ffa800;
}

.status.bad {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
}

.test-btn.testing {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
}

.test-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 左侧面试官视频区样式 */
.interviewers {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.interviewer-box {
  background: rgba(15, 15, 27, 0.5);
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid rgba(76, 201, 240, 0.2);
}

.interviewer-box .video-wrapper {
  width: 100%;
  aspect-ratio: 16/9;
  position: relative;
}

.interviewer-box .video-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  background: rgba(15, 15, 27, 0.3);
}

.interviewer-box .video-placeholder i {
  font-size: 24px;
  margin-bottom: 8px;
}

.interviewer-box .video-placeholder p {
  font-size: 12px;
}

.interviewer-box:first-child .video-placeholder i {
  color: #4CC9F0;
}

.interviewer-box:last-child .video-placeholder i {
  color: #4361EE;
}

.interviewer-box .name-tag {
  padding: 8px;
  background: rgba(15, 15, 27, 0.8);
  color: #fff;
  font-size: 12px;
  text-align: center;
  border-top: 1px solid rgba(76, 201, 240, 0.2);
}

/* 字幕区域样式 */
.caption-section {
  padding: 15px 20px;
  border-top: 1px solid rgba(76, 201, 240, 0.2);
  background: rgba(15, 15, 27, 0.5);
}

.caption-container {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 12px 15px;
  background: rgba(76, 201, 240, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(76, 201, 240, 0.2);
}

.caption-icon {
  width: 32px;
  height: 32px;
  background: rgba(76, 201, 240, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CC9F0;
  flex-shrink: 0;
}

.caption-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.caption-text {
  color: #fff;
  font-size: 14px;
  line-height: 1.5;
}

.caption-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 12px;
}

.caption-wave span {
  display: inline-block;
  width: 3px;
  height: 100%;
  background: #4CC9F0;
  border-radius: 1px;
  animation: wave 1s ease-in-out infinite;
}

.caption-wave span:nth-child(1) { animation-delay: 0s; }
.caption-wave span:nth-child(2) { animation-delay: 0.1s; }
.caption-wave span:nth-child(3) { animation-delay: 0.2s; }
.caption-wave span:nth-child(4) { animation-delay: 0.3s; }

@keyframes wave {
  0%, 100% { height: 4px; }
  50% { height: 12px; }
}

.error-message {
  color: #ff4757;
  font-size: 14px;
  margin-top: 10px;
  padding: 10px;
  background: rgba(255, 71, 87, 0.1);
  border-radius: 5px;
}

.device-item .status.verified {
  background: rgba(46, 213, 115, 0.2);
  color: #2ed573;
}

.device-item .status.error {
  background: rgba(255, 71, 87, 0.2);
  color: #ff4757;
}
</style>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { userService } from '../services/userService'
import http from '../config/axios'
import FaceVerification from '../components/FaceVerification.vue'

const router = useRouter()
const showDeviceCheck = ref(true)
const currentStep = ref(1)
const localVideo = ref<HTMLVideoElement | null>(null)
const localStream = ref<MediaStream | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const cameraPreview = ref<HTMLVideoElement | null>(null)
const verifyVideo = ref<HTMLVideoElement | null>(null)
const idPhotoUrl = ref<string | null>(null)
const microphoneVolume = ref(0)

// 设备状态
const deviceStatus = ref({
  microphone: {
    devices: [] as MediaDeviceInfo[],
    selectedId: '',
    stream: null as MediaStream | null,
    testing: false
  },
  camera: {
    devices: [] as MediaDeviceInfo[],
    selectedId: '',
    stream: null as MediaStream | null,
    testing: false
  },
  network: {
    status: 'good' as 'good' | 'poor' | 'bad',
    speed: null as number | null,
    testing: false
  },
  faceVerify: {
    verified: false,
    verifying: false,
    error: null as string | null,
    livePhotoUrl: null as string | null,
    confidence: null as number | null
  }
})

// 计算设备测试是否完成
const isDeviceTestComplete = computed(() => {
  return deviceStatus.value.microphone.devices.length > 0 &&
         deviceStatus.value.camera.devices.length > 0 &&
         deviceStatus.value.network.status !== 'bad'
})

// 触发文件选择
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件上传
const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const file = input.files[0]
  
  try {
    // 上传到服务器并获取Base64数据
    const base64Data = await userService.uploadIdPhoto(file)
    
    // 更新预览
    idPhotoUrl.value = `data:${file.type};base64,${base64Data}`
    
  } catch (error) {
    console.error('上传证件照失败:', error)
    alert(error instanceof Error ? error.message : '上传证件照失败，请重试')
    
    // 清除文件选择
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    idPhotoUrl.value = null
  }
}

// 添加错误处理函数
const handleError = (message: string) => {
  alert(message)
  currentStep.value = 1 // 返回第一步
}

// 获取设备列表
const getDevices = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    deviceStatus.value.microphone.devices = devices.filter(device => device.kind === 'audioinput')
    deviceStatus.value.camera.devices = devices.filter(device => device.kind === 'videoinput')
    
    // 默认选择第一个设备
    if (deviceStatus.value.microphone.devices.length) {
      deviceStatus.value.microphone.selectedId = deviceStatus.value.microphone.devices[0].deviceId
    }
    if (deviceStatus.value.camera.devices.length) {
      deviceStatus.value.camera.selectedId = deviceStatus.value.camera.devices[0].deviceId
    }
  } catch (error) {
    console.error('获取设备列表失败:', error)
  }
}

// 测试麦克风
const testMicrophone = async () => {
  try {
    // 如果正在测试中，停止测试
    if (deviceStatus.value.microphone.testing) {
      if (deviceStatus.value.microphone.stream) {
        deviceStatus.value.microphone.stream.getTracks().forEach(track => track.stop())
        deviceStatus.value.microphone.stream = null
      }
      deviceStatus.value.microphone.testing = false
      microphoneVolume.value = 0
      return
    }

    // 开始测试
    deviceStatus.value.microphone.testing = true
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        deviceId: deviceStatus.value.microphone.selectedId
      }
    })
    deviceStatus.value.microphone.stream = stream

    // 创建音频分析器
    const audioContext = new AudioContext()
    const analyser = audioContext.createAnalyser()
    const microphone = audioContext.createMediaStreamSource(stream)
    microphone.connect(analyser)
    analyser.fftSize = 256
    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    // 更新音量指示器
    const updateVolume = () => {
      if (!deviceStatus.value.microphone.testing) return
      
      analyser.getByteFrequencyData(dataArray)
      const average = dataArray.reduce((acc, val) => acc + val, 0) / bufferLength
      microphoneVolume.value = Math.min(100, average * 2)
      
      requestAnimationFrame(updateVolume)
    }
    updateVolume()

  } catch (error) {
    console.error('测试麦克风失败:', error)
    deviceStatus.value.microphone.testing = false
  }
}

// 测试摄像头
const testCamera = async () => {
  try {
    // 如果正在测试中，停止测试
    if (deviceStatus.value.camera.testing) {
      if (deviceStatus.value.camera.stream) {
        deviceStatus.value.camera.stream.getTracks().forEach(track => track.stop())
        deviceStatus.value.camera.stream = null
      }
      deviceStatus.value.camera.testing = false
      return
    }

    // 开始测试
    deviceStatus.value.camera.testing = true
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceStatus.value.camera.selectedId,
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    })
    deviceStatus.value.camera.stream = stream

    // 显示预览
    if (cameraPreview.value) {
      cameraPreview.value.srcObject = stream
    }

  } catch (error) {
    console.error('测试摄像头失败:', error)
    deviceStatus.value.camera.testing = false
  }
}

// 测试网络
const testNetwork = async () => {
  try {
    deviceStatus.value.network.testing = true
    deviceStatus.value.network.speed = null
    
    // 使用大文件测试下载速度
    const startTime = performance.now()
    const response = await fetch('https://speed.cloudflare.com/__down?bytes=26214400') // 25MB
    const endTime = performance.now()
    
    if (response.ok) {
      const duration = (endTime - startTime) / 1000 // 转换为秒
      const bytes = await response.blob().then(b => b.size)
      const bitsPerSecond = (bytes * 8) / duration
      const megabitsPerSecond = bitsPerSecond / 1000000
      
      deviceStatus.value.network.speed = Math.round(megabitsPerSecond * 100) / 100
      
      if (megabitsPerSecond >= 10) {
        deviceStatus.value.network.status = 'good'
      } else if (megabitsPerSecond >= 5) {
        deviceStatus.value.network.status = 'poor'
      } else {
        deviceStatus.value.network.status = 'bad'
      }
    } else {
      throw new Error('网络测试失败')
    }
  } catch (error) {
    console.error('测试网络失败:', error)
    deviceStatus.value.network.status = 'bad'
  } finally {
    deviceStatus.value.network.testing = false
  }
}

// 进行人脸验证
const verifyFace = async () => {
  try {
    if (!idPhotoUrl.value) {
      throw new Error('请先上传证件照')
    }

    deviceStatus.value.faceVerify.verifying = true
    deviceStatus.value.faceVerify.error = null
    deviceStatus.value.faceVerify.livePhotoUrl = null
    deviceStatus.value.faceVerify.confidence = null

    // 获取摄像头流
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceStatus.value.camera.selectedId,
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    })

    // 显示预览
    if (verifyVideo.value) {
      verifyVideo.value.srcObject = stream
    }

    // 等待1秒让用户准备
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 捕获图像
    const canvas = document.createElement('canvas')
    canvas.width = verifyVideo.value!.videoWidth
    canvas.height = verifyVideo.value!.videoHeight
    const ctx = canvas.getContext('2d')
    if (!ctx) throw new Error('无法创建canvas上下文')

    ctx.drawImage(verifyVideo.value!, 0, 0)
    const imageData = canvas.toDataURL('image/jpeg')
    deviceStatus.value.faceVerify.livePhotoUrl = imageData

    // 准备API请求数据
    const idPhotoBase64 = idPhotoUrl.value.split(',')[1]
    const livePhotoBase64 = imageData.split(',')[1]

    // 停止视频流
    stream.getTracks().forEach(track => track.stop())

    // 调用后端API进行人脸比对
    const response = await http.post('/api/vision/face/verify', {
      id_photo: idPhotoBase64,
      live_photo: livePhotoBase64
    })

    const result = response.data
    
    if (!result.success) {
      throw new Error(result.error || '验证失败')
    }

    deviceStatus.value.faceVerify.verified = result.is_same_person
    deviceStatus.value.faceVerify.confidence = result.confidence

    if (!result.is_same_person) {
      deviceStatus.value.faceVerify.error = '验证失败，请确保本人操作'
    }

  } catch (error) {
    console.error('人脸验证失败:', error)
    deviceStatus.value.faceVerify.error = error instanceof Error ? error.message : '验证失败，请重试'
    deviceStatus.value.faceVerify.verified = false
  } finally {
    deviceStatus.value.faceVerify.verifying = false
  }
}

// 获取验证状态文本
const getVerifyStatusText = () => {
  if (deviceStatus.value.faceVerify.verifying) return '正在验证...'
  if (deviceStatus.value.faceVerify.verified) return '验证通过'
  if (deviceStatus.value.faceVerify.error) return '验证失败'
  return '等待验证'
}

// 获取验证按钮文本
const getVerifyButtonText = () => {
  if (deviceStatus.value.faceVerify.verifying) return '验证中...'
  if (deviceStatus.value.faceVerify.verified) return '已验证'
  return '开始验证'
}

// 下一步
const goToNextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  }
}

// 开始面试
const startInterview = async () => {
  console.log('开始面试')
  try {
    // 确保设备可用
    const microphoneAvailable = deviceStatus.value.microphone.devices.length > 0
    const cameraAvailable = deviceStatus.value.camera.devices.length > 0
    const networkGood = deviceStatus.value.network.status !== 'bad'
    const faceVerified = deviceStatus.value.faceVerify.verified

    if (!microphoneAvailable || !cameraAvailable || !networkGood) {
      alert('请确保设备正常且网络状态良好')
      return
    }

    if (!faceVerified) {
      alert('请先完成人脸验证')
      return
    }

    // 停止所有测试流
    stopAllStreams()

    // 获取正式的媒体流
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        deviceId: deviceStatus.value.microphone.selectedId
      },
      video: {
        deviceId: deviceStatus.value.camera.selectedId,
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    })

    // 设置视频流
    if (localVideo.value) {
      localVideo.value.srcObject = stream
    }
    localStream.value = stream

    // 关闭设备检测弹窗
    showDeviceCheck.value = false
    console.log('设备检测弹窗已关闭')

  } catch (error) {
    console.error('开始面试失败:', error)
    alert('启动设备失败，请检查设备权限设置')
  }
}

// 停止所有媒体流
const stopAllStreams = () => {
  if (deviceStatus.value.microphone.stream) {
    deviceStatus.value.microphone.stream.getTracks().forEach(track => track.stop())
  }
  if (deviceStatus.value.camera.stream) {
    deviceStatus.value.camera.stream.getTracks().forEach(track => track.stop())
  }
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
  }
  
  deviceStatus.value.microphone.testing = false
  deviceStatus.value.camera.testing = false
  localStream.value = null
}

// 取消设备检测
const cancelDeviceCheck = () => {
  stopAllStreams()
  router.back()
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 处理验证成功
const handleVerificationSuccess = (result: { confidence: number }) => {
  console.log('验证成功，相似度:', result.confidence)
  deviceStatus.value.faceVerify.verified = true
  deviceStatus.value.faceVerify.confidence = result.confidence
}

// 页面加载时获取设备列表
onMounted(() => {
  getDevices()
})

// 页面卸载时清理资源
onUnmounted(() => {
  stopAllStreams()
})
</script> 