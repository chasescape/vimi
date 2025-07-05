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
        <div class="device-list">
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
            <button class="test-btn" 
                    @click="testMicrophone"
                    :class="{ 'testing': deviceStatus.microphone.testing }">
              {{ deviceStatus.microphone.testing ? '停止' : '测试' }}
            </button>
          </div>
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
            <button class="test-btn" 
                    @click="testCamera"
                    :class="{ 'testing': deviceStatus.camera.testing }">
              {{ deviceStatus.camera.testing ? '停止' : '测试' }}
            </button>
          </div>
          <div class="device-item">
            <i class="fas fa-wifi"></i>
            <span>网络状态</span>
            <div class="status-container">
              <div class="status" :class="deviceStatus.network.status">
                {{ deviceStatus.network.status === 'good' ? '良好' : 
                   deviceStatus.network.status === 'poor' ? '一般' : '差' }}
              </div>
              <button class="test-btn" 
                      @click="testNetwork"
                      :disabled="deviceStatus.network.testing">
                测试
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="secondary-btn" @click="cancelDeviceCheck">取消</button>
          <button class="primary-btn" @click="startInterview">开始面试</button>
        </div>
      </div>
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

.device-list {
  margin: 20px 0;
}

.device-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-bottom: 1px solid rgba(76, 201, 240, 0.2);
}

.device-item select {
  flex: 1;
  padding: 8px;
  border-radius: 5px;
  background: rgba(76, 201, 240, 0.1);
  border: 1px solid rgba(76, 201, 240, 0.3);
  color: #fff;
}

.test-btn {
  padding: 6px 12px;
  border-radius: 5px;
  border: 1px solid rgba(76, 201, 240, 0.3);
  background: rgba(76, 201, 240, 0.1);
  color: #fff;
  cursor: pointer;
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 20px;
}

.secondary-btn, .primary-btn {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.secondary-btn {
  background: rgba(76, 201, 240, 0.1);
  border: 1px solid rgba(76, 201, 240, 0.3);
  color: #fff;
}

.primary-btn {
  background: #4CC9F0;
  border: none;
  color: #fff;
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
</style>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showDeviceCheck = ref(true)
const localVideo = ref<HTMLVideoElement | null>(null)
const localStream = ref<MediaStream | null>(null)

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
    testing: false
  }
})

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
        deviceId: deviceStatus.value.camera.selectedId
      }
    })
    deviceStatus.value.camera.stream = stream
  } catch (error) {
    console.error('测试摄像头失败:', error)
    deviceStatus.value.camera.testing = false
  }
}

// 测试网络
const testNetwork = async () => {
  try {
    deviceStatus.value.network.testing = true
    
    // 使用简单的网络测试方法
    const startTime = Date.now()
    try {
      await fetch('https://www.google.com/favicon.ico')
      const endTime = Date.now()
      const duration = endTime - startTime
      
      if (duration < 100) {
        deviceStatus.value.network.status = 'good'
      } else if (duration < 300) {
        deviceStatus.value.network.status = 'poor'
      } else {
        deviceStatus.value.network.status = 'bad'
      }
    } catch {
      deviceStatus.value.network.status = 'bad'
    }
  } catch (error) {
    console.error('测试网络失败:', error)
    deviceStatus.value.network.status = 'bad'
  } finally {
    deviceStatus.value.network.testing = false
  }
}

// 开始面试
const startInterview = async () => {
  try {
    // 确保设备可用
    const microphoneAvailable = deviceStatus.value.microphone.devices.length > 0
    const cameraAvailable = deviceStatus.value.camera.devices.length > 0
    const networkGood = deviceStatus.value.network.status !== 'bad'

    if (!microphoneAvailable || !cameraAvailable || !networkGood) {
      alert('请确保设备正常且网络状态良好')
      return
    }

    // 停止测试流
    if (deviceStatus.value.microphone.stream) {
      deviceStatus.value.microphone.stream.getTracks().forEach(track => track.stop())
    }
    if (deviceStatus.value.camera.stream) {
      deviceStatus.value.camera.stream.getTracks().forEach(track => track.stop())
    }

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

  } catch (error) {
    console.error('开始面试失败:', error)
    alert('启动设备失败，请检查设备权限设置')
  }
}

// 取消设备检测
const cancelDeviceCheck = () => {
  // 停止所有媒体流
  if (deviceStatus.value.microphone.stream) {
    deviceStatus.value.microphone.stream.getTracks().forEach(track => track.stop())
  }
  if (deviceStatus.value.camera.stream) {
    deviceStatus.value.camera.stream.getTracks().forEach(track => track.stop())
  }
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
  }
  
  // 重置状态
  deviceStatus.value.microphone.testing = false
  deviceStatus.value.camera.testing = false
  deviceStatus.value.network.testing = false
  localStream.value = null
  
  // 关闭弹窗
  showDeviceCheck.value = false
  
  // 返回上一页
  router.back()
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 页面加载时获取设备列表
getDevices()

// 页面卸载时清理资源
onUnmounted(() => {
  if (localStream.value) {
    localStream.value.getTracks().forEach(track => track.stop())
  }
})
</script> 