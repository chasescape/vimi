<template>
  <div class="ai-interview-system" :class="{'dark-mode': darkMode}">
    <!-- 顶部控制栏 -->
    <header class="interview-header" :class="{'scrolled': scrollPosition > 10}">
      <div class="header-left">
        <h1>AI智能面试系统</h1>
        <div class="interview-info">
          <span class="interview-id">面试ID: {{ interviewId }}</span>
          <span class="interview-time"><i class="fas fa-clock"></i> {{ formattedTime }}</span>
        </div>
      </div>
      <div class="header-right">
        <button class="control-btn" @click="toggleDarkMode" :title="darkMode ? '切换亮色模式' : '切换暗色模式'">
          <i :class="darkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
        </button>
        <button class="control-btn" @click="toggleMiddleScreen" :title="isMiddleScreenExpanded ? '缩小中间屏幕' : '放大中间屏幕'">
          <i :class="isMiddleScreenExpanded ? 'fas fa-compress' : 'fas fa-expand'"></i>
        </button>
        <button class="control-btn" @click="toggleFullscreen" title="全屏">
          <i class="fas fa-expand"></i>
        </button>
        <button class="control-btn danger" @click="endInterview" title="结束面试">
          <i class="fas fa-phone-slash"></i>
        </button>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="interview-main">
      <!-- 左侧面试者信息面板 -->
      <div class="candidate-panel" 
           :class="{'panel-active': leftPanelActive, 'expanded': leftPanelExpanded}">
        <div class="panel-toggle" @click="toggleLeftPanel">
          <i :class="leftPanelActive ? 
                      (leftPanelExpanded ? 'fas fa-compress' : 'fas fa-chevron-left') : 
                      'fas fa-chevron-right'"></i>
        </div>
        <div class="candidate-card">
          <div class="candidate-avatar">
            <img :src="candidate.avatar" alt="候选人头像" @error="handleImageError">
            <div class="status-indicator" :class="{'active': candidate.online}"></div>
          </div>
          <div class="candidate-info">
            <h3>{{ candidate.name }}</h3>
            <p><i class="fas fa-id-card"></i> {{ candidate.id }}</p>
            <p><i class="fas fa-briefcase"></i> {{ candidate.position }}</p>
            <p><i class="fas fa-graduation-cap"></i> {{ candidate.education }}</p>
            <p><i class="fas fa-star"></i> 匹配度: <span class="match-score">{{ candidate.matchScore }}%</span></p>
          </div>
        </div>
        
        <!-- 面试控制面板 -->
        <div class="interview-controls">
          <button class="start-btn" @click="startInterview" :disabled="interviewStarted">
            <i class="fas fa-play"></i> {{ interviewStarted ? '面试进行中' : '开始面试' }}
          </button>
          <div class="timer-display">
            <i class="fas fa-stopwatch"></i> 面试时长: {{ interviewDuration }}
          </div>
        </div>
      </div>

      <!-- 中间AI面试官区域 -->
      <div class="ai-interviewer" :class="{'expanded': isMiddleScreenExpanded}">
        <div class="video-container" :class="{'active-speech': isSpeaking, 'pulse': interviewStarted}">
          <!-- 3D AI面试官模型 -->
          <div class="ai-3d-model" @click="triggerAIResponse">
            <div class="ai-avatar-container">
              <img :src="aiAvatar" alt="AI面试官" class="ai-avatar-img" @error="handleAIImageError">
              <div class="ai-3d-effects">
                <div class="particle" v-for="(particle, index) in particles" :key="index" 
                     :style="particleStyle(particle)"></div>
              </div>
            </div>
            <div class="ai-status" :class="{'listening': isListening}">
              <div class="listening-animation">
                <span v-for="n in 3" :key="n" :style="getListeningStyle(n)"></span>
              </div>
            </div>
          </div>
          
          <div class="video-overlay">
            <div class="ai-identity">
              <div class="ai-avatar">
                <img :src="aiAvatar" alt="AI面试官" @error="handleAIImageError">
              </div>
              <h3>AI面试官 - {{ aiName }}</h3>
              <p>正在评估: {{ currentQuestion.category }}</p>
            </div>
            <div class="ai-controls">
              <button class="ai-btn" @click="toggleMicrophone" :title="microphoneActive ? '关闭麦克风' : '开启麦克风'">
                <i :class="microphoneActive ? 'fas fa-microphone' : 'fas fa-microphone-slash'"></i>
              </button>
              <button class="ai-btn" @click="toggleAIListening" :title="isListening ? '停止监听' : '开始监听'">
                <i :class="isListening ? 'fas fa-ear-listen' : 'fas fa-ear'"></i>
              </button>
            </div>
          </div>
          
          <!-- 问题框 -->
          <transition name="fade-slide">
            <div class="question-box" v-if="currentQuestion.text">
              <h4><i class="fas fa-question-circle"></i> 当前问题</h4>
              <p>{{ currentQuestion.text }}</p>
              <div class="question-timer">
                <i class="fas fa-clock"></i> {{ formatTime(questionTime) }}
              </div>
            </div>
          </transition>
          
          <!-- 语音动画 -->
          <div class="speech-animation" v-if="isSpeaking">
            <div class="speech-bubble" v-for="i in 3" :key="i" :style="getBubbleStyle(i)"></div>
          </div>

          <!-- 画中画视频容器 -->
          <div class="candidate-pip" v-if="isMiddleScreenExpanded">
            <div class="pip-header">
              <span>面试者</span>
              <button class="pip-close" @click="toggleMiddleScreen">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="pip-video-container">
              <video
                ref="pipVideo"
                autoplay
                playsinline
                muted
                class="pip-video"
              ></video>
            </div>
            <div class="pip-controls">
              <button class="control-btn" @click="toggleCamera" 
                      :title="cameraActive ? '关闭摄像头' : '开启摄像头'">
                <i :class="cameraActive ? 'fas fa-video' : 'fas fa-video-slash'"></i>
              </button>
              <button class="control-btn" @click="toggleMicrophone" 
                      :title="microphoneActive ? '静音' : '取消静音'">
                <i :class="microphoneActive ? 'fas fa-microphone' : 'fas fa-microphone-slash'"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧候选人视频和智能体面板 - 只在非放大模式显示 -->
      <div class="right-panel" 
           :class="{'panel-active': rightPanelActive, 'expanded': rightPanelExpanded}"
           v-if="!isMiddleScreenExpanded">
        <div class="panel-toggle" @click="toggleRightPanel">
          <i :class="rightPanelActive ? 
                      (rightPanelExpanded ? 'fas fa-compress' : 'fas fa-chevron-right') : 
                      'fas fa-chevron-left'"></i>
        </div>
        
        <!-- 候选人视频区域 -->
        <div class="candidate-view">
          <div class="video-container">
            <!-- 添加头像占位符 -->
    <!-- 头像容器（仅放大内容，不改变容器结构） -->
    <div class="avatar-placeholder" v-show="!cameraActive">
      <div class="avatar-scale-wrapper">
        <img :src="candidate.avatar" 
             alt="候选人头像" 
             class="avatar-img"
             @error="handleImageError">
      </div>
    </div>
            <video 
              ref="candidateVideo"
              autoplay
              playsinline
              muted
             class="main-video"
     v-show="cameraActive"
    ></video>
 
           
            <div class="video-controls">
              <button class="control-btn" @click="toggleCamera" :title="cameraActive ? '关闭摄像头' : '开启摄像头'">
                <i :class="cameraActive ? 'fas fa-video' : 'fas fa-video-slash'"></i>
              </button>
              <button class="control-btn" @click="toggleMicrophone" :title="microphoneActive ? '静音' : '取消静音'">
                <i :class="microphoneActive ? 'fas fa-microphone' : 'fas fa-microphone-slash'"></i>
              </button>
              <button class="control-btn" @click="toggleRecording" :title="recording ? '停止录制' : '开始录制'">
                <i :class="recording ? 'fas fa-stop-circle' : 'fas fa-circle'"></i>
               
              </button>
            </div>
          </div>

          <!-- 情绪分析 -->
          <div class="emotion-analysis">
            <h4><i class="fas fa-smile"></i> 实时情绪分析</h4>
            <div class="emotion-chart" ref="emotionChart"></div>
            <div class="emotion-feedback">
              <p v-if="emotionFeedback"><i class="fas fa-comment-dots"></i> {{ emotionFeedback }}</p>
            </div>
          </div>
        </div>
        
        <!-- 智能体助手 -->
    
      </div>
    </main>
    
    <!-- 底部控制栏 -->
  <!-- 底部控制栏 -->
<footer class="interview-footer" :class="{'footer-hidden': !showFooter}">
  <div class="footer-left">
    <button class="action-btn" @click="prevQuestion" :disabled="currentQuestionIndex === 0">
      <i class="fas fa-arrow-left"></i> 上一题
    </button>
    <button class="action-btn primary" @click="nextQuestion" :disabled="currentQuestionIndex === questions.length - 1">
      下一题 <i class="fas fa-arrow-right"></i>
    </button>
    <button class="action-btn" @click="toggleAutoMode">
      <i class="fas" :class="autoMode ? 'fa-toggle-on' : 'fa-toggle-off'"></i> 自动模式
    </button>
  </div>
  
  <div class="footer-center">
    <div class="interview-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{width: interviewProgress + '%'}"></div>
      </div>
      <span>进度: {{ currentQuestionIndex + 1 }}/{{ questions.length }}</span>
    </div>
  </div>
  
  <div class="footer-right">
    <button class="action-btn" @click="toggleNotesPanel">
      <i class="fas fa-edit"></i> 笔记
    </button>
    
    <!-- 新增的AI助手按钮 -->
    <button class="action-btn assistant-btn" @click="toggleAssistantExpanded">
      <i class="fas fa-robot"></i>
      <span class="notification-badge" v-if="unreadMessages > 0">{{ unreadMessages }}</span>
      <span>AI助手</span>
    </button>
    
    <button class="action-btn" @click="toggleAnalysisPanel">
      <i class="fas fa-chart-pie"></i> 详细分析
    </button>
  </div>
  
  <!-- AI助手面板 -->
  <transition name="slide-up">
    <div class="assistant-panel" v-if="assistantExpanded">
      <div class="assistant-header">
        <h4><i class="fas fa-robot"></i> AI面试助手</h4>
        <button class="close-btn" @click="toggleAssistantExpanded">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="assistant-messages" ref="messagesContainer">
        <div v-for="(msg, index) in assistantMessages" :key="index" 
             class="message" :class="msg.sender">
          <div class="message-content">
            <p>{{ msg.text }}</p>
            <span class="message-time">{{ msg.time }}</span>
          </div>
        </div>
      </div>
      
      <div class="assistant-input">
        <input v-model="assistantInput" 
               @keyup.enter="sendToAssistant" 
               placeholder="输入问题...">
        <button @click="sendToAssistant">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </transition>
</footer>

    <!-- 笔记面板 -->
    <transition name="slide-up">
      <div class="notes-panel" v-if="showNotes">
        <div class="panel-header">
          <h4><i class="fas fa-edit"></i> 面试笔记</h4>
          <button class="close-btn" @click="showNotes = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <textarea v-model="interviewNotes" placeholder="记录面试中的重要信息..."></textarea>
        <div class="panel-footer">
          <button class="save-btn" @click="saveNotes">
            <i class="fas fa-save"></i> 保存笔记
          </button>
        </div>
      </div>
    </transition>



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

  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch, nextTick } from 'vue';
import * as echarts from 'echarts';

export default {
  setup() {
    // 面板状态
    const leftPanelActive = ref(true);
    const rightPanelActive = ref(true);
    const leftPanelExpanded = ref(false);
    const rightPanelExpanded = ref(false);
    const isMiddleScreenExpanded = ref(false);

    // 面板切换逻辑
    const toggleLeftPanel = () => {
      if (leftPanelActive.value) {
        leftPanelExpanded.value = !leftPanelExpanded.value;
      } else {
        leftPanelActive.value = true;
      }
    };

    const toggleRightPanel = () => {
      if (rightPanelActive.value) {
        rightPanelExpanded.value = !rightPanelExpanded.value;
      } else {
        rightPanelActive.value = true;
      }
    };

    // 主题模式
    const darkMode = ref(true);
    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      showNotification(darkMode.value ? '已切换至暗色模式' : '已切换至亮色模式', 
                      darkMode.value ? 'fas fa-moon' : 'fas fa-sun');
    };

    // 3D粒子效果
    const particles = ref([]);
    const initParticles = () => {
      const count = 30;
      for (let i = 0; i < count; i++) {
        particles.value.push({
          x: Math.random() * 100,
          y: Math.random() * 100,
          size: Math.random() * 5 + 2,
          speed: Math.random() * 0.5 + 0.1,
          delay: Math.random() * 5,
          opacity: Math.random() * 0.5 + 0.1
        });
      }
    };
    
    // 中间屏幕放大/缩小
    const toggleMiddleScreen = () => {
      isMiddleScreenExpanded.value = !isMiddleScreenExpanded.value;

      nextTick(() => {
        // 确保视频流正确显示在画中画或主视频中
        if (mediaStream.value) {
          if (isMiddleScreenExpanded.value) {
            // 切换到放大模式时，将视频流分配给画中画
            if (pipVideo.value) {
              pipVideo.value.srcObject = mediaStream.value;
              pipVideo.value.play().catch(e => {
                console.warn('画中画播放失败:', e);
                pipVideo.value.muted = true;
                pipVideo.value.play().catch(console.warn);
              });
            }
            // 确保主视频继续显示
            if (candidateVideo.value) {
              candidateVideo.value.srcObject = mediaStream.value;
            }
          } else {
            // 退出放大模式时，确保主视频显示
            if (candidateVideo.value) {
              candidateVideo.value.srcObject = mediaStream.value;
            }
          }
        }
      });

      // 显示操作通知
      showNotification(
        isMiddleScreenExpanded.value ? '屏幕已放大' : '屏幕已恢复', 
        isMiddleScreenExpanded.value ? 'fas fa-expand' : 'fas fa-compress'
      );
    };

    // 粒子效果样式生成器
    const particleStyle = (particle) => {
      return {
        left: `${particle.x}%`,
        top: `${particle.y}%`,
        width: `${particle.size}px`,
        height: `${particle.size}px`,
        animation: `float ${particle.speed}s ease-in-out infinite alternate`,
        opacity: particle.opacity,
        animationDelay: `${particle.delay}s`,
        willChange: 'transform'
      };
    };

    // 候选人数据
    const candidate = reactive({
      name: '张三',
      id: 'CAN20230001',
      position: '前端开发工程师',
      education: '本科 - 计算机科学',
      matchScore: 85,
      avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
      online: true
    });

    // 图片加载失败处理
    const handleImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/150?text=Avatar';
    };

    const handleAIImageError = (e) => {
      e.target.src = 'https://via.placeholder.com/150?text=AI+Avatar';
    };

    // AI面试官数据
    const aiName = ref('未来科技');
    const aiAvatar = ref('https://img.freepik.com/free-photo/3d-rendering-humanoid-robot-with-blue-neon-lights_23-2149760891.jpg');
    
    // 面试问题
    const questions = [
      {
        id: 1,
        category: '技术能力',
        text: '请解释React的虚拟DOM工作原理及其优势。',
        evaluation: {
          technical: 85,
          communication: 75,
          problemSolving: 80
        }
      },
      {
        id: 2,
        category: '技术能力',
        text: '如何优化一个大型前端应用的性能？请列举具体方法。',
        evaluation: {
          technical: 90,
          communication: 80,
          problemSolving: 85
        }
      },
      {
        id: 3,
        category: '项目经验',
        text: '请描述你参与过的最具挑战性的项目，你在其中扮演什么角色？',
        evaluation: {
          technical: 75,
          communication: 85,
          teamwork: 90
        }
      },
      {
        id: 4,
        category: '解决问题',
        text: '当你遇到一个难以解决的技术问题时，你的解决流程是什么？',
        evaluation: {
          technical: 80,
          problemSolving: 95,
          learning: 85
        }
      },
      {
        id: 5,
        category: '团队协作',
        text: '请举例说明你如何在团队中处理意见分歧。',
        evaluation: {
          communication: 90,
          teamwork: 85,
          problemSolving: 80
        }
      }
    ];

    // 当前问题状态
    const currentQuestionIndex = ref(0);
    const currentQuestion = computed(() => questions[currentQuestionIndex.value]);
    const questionTime = ref(0);
    
    // 自动模式
    const autoMode = ref(false);
    const autoModeTimer = ref(null);
    
    const toggleAutoMode = () => {
      autoMode.value = !autoMode.value;
      if (autoMode.value) {
        startAutoMode();
        showNotification('自动模式已开启，每题回答时间: 2分钟', 'fas fa-toggle-on');
      } else {
        clearTimeout(autoModeTimer.value);
        showNotification('自动模式已关闭', 'fas fa-toggle-off');
      }
    };
    
    const startAutoMode = () => {
      if (autoMode.value && interviewStarted.value) {
        autoModeTimer.value = setTimeout(() => {
          if (currentQuestionIndex.value < questions.length - 1) {
            nextQuestion();
            startAutoMode(); // 继续下一个问题
          } else {
            autoMode.value = false;
            showNotification('所有问题已完成，自动模式已关闭', 'fas fa-toggle-off');
          }
        }, 120000); // 2分钟自动切换
      }
    };

    // 面试进度控制
    const nextQuestion = () => {
      if (currentQuestionIndex.value < questions.length - 1) {
        currentQuestionIndex.value++;
        questionTime.value = 0;
        updateAnalysisData();
        triggerAIResponse();
        showNotification('已切换到下一题', 'fas fa-arrow-right');
      }
    };

    const prevQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
        questionTime.value = 0;
        updateAnalysisData();
        triggerAIResponse();
        showNotification('已返回上一题', 'fas fa-arrow-left');
      }
    };

    const interviewProgress = computed(() => {
      return ((currentQuestionIndex.value + 1) / questions.length) * 100;
    });

    // 分析数据
    const analysisData = reactive([
      { label: '技术能力', value: 0 },
      { label: '沟通表达', value: 0 },
      { label: '问题解决', value: 0 },
      { label: '团队协作', value: 0 },
      { label: '学习能力', value: 0 }
    ]);
    
    const analysisSummary = ref('');
    
    const updateAnalysisData = () => {
      // 计算各项平均值
      const counts = { technical: 0, communication: 0, problemSolving: 0, teamwork: 0, learning: 0 };
      const sums = { technical: 0, communication: 0, problemSolving: 0, teamwork: 0, learning: 0 };
      
      for (let i = 0; i <= currentQuestionIndex.value; i++) {
        const q = questions[i];
        if (q.evaluation.technical) {
          sums.technical += q.evaluation.technical;
          counts.technical++;
        }
        if (q.evaluation.communication) {
          sums.communication += q.evaluation.communication;
          counts.communication++;
        }
        if (q.evaluation.problemSolving) {
          sums.problemSolving += q.evaluation.problemSolving;
          counts.problemSolving++;
        }
        if (q.evaluation.teamwork) {
          sums.teamwork += q.evaluation.teamwork;
          counts.teamwork++;
        }
        if (q.evaluation.learning) {
          sums.learning += q.evaluation.learning;
          counts.learning++;
        }
      }
      
      analysisData[0].value = Math.round(sums.technical / (counts.technical || 1));
      analysisData[1].value = Math.round(sums.communication / (counts.communication || 1));
      analysisData[2].value = Math.round(sums.problemSolving / (counts.problemSolving || 1));
      analysisData[3].value = Math.round(sums.teamwork / (counts.teamwork || 1));
      analysisData[4].value = Math.round(sums.learning / (counts.learning || 1));
      
      // 更新综合评价
      updateAnalysisSummary();
    };
    
    const updateAnalysisSummary = () => {
      const avgScore = analysisData.reduce((sum, item) => sum + item.value, 0) / analysisData.length;
      
      if (avgScore >= 85) {
        analysisSummary.value = '候选人表现优秀，技术能力扎实，沟通表达清晰，具备很强的解决问题能力和团队协作精神，强烈推荐。';
      } else if (avgScore >= 70) {
        analysisSummary.value = '候选人表现良好，具备必要的技术能力和沟通技巧，能够胜任工作，建议录用。';
      } else if (avgScore >= 60) {
        analysisSummary.value = '候选人表现一般，部分能力有待提高，可以考虑但需要进一步培训。';
      } else {
        analysisSummary.value = '候选人表现不佳，多项能力未达到要求，不建议录用。';
      }
    };

    // 面试计时
    const interviewTime = ref(0);
    const interviewTimer = ref(null);
    
    const startInterview = () => {
      interviewStarted.value = true;
      interviewTime.value = 0;
      questionTime.value = 0;
      
      // 启动计时器
      interviewTimer.value = setInterval(() => {
        interviewTime.value++;
        questionTime.value++;
      }, 1000);
      
      // 自动开启摄像头和麦克风
      if (!cameraActive.value) toggleCamera();
      if (!microphoneActive.value) toggleMicrophone();
      
      // 触发AI问候
      setTimeout(() => {
        triggerAIResponse('您好！我是AI面试官，很高兴见到您。我们即将开始面试。');
      }, 1000);
      
      showNotification('面试已开始', 'fas fa-play');
    };
    
    const endInterview = () => {
      showEndInterviewModal.value = true;
    };
    
    const confirmEndInterview = () => {
      interviewStarted.value = false;
      clearInterval(interviewTimer.value);
      showNotification('面试已结束', 'fas fa-stop');
      showEndInterviewModal.value = false;
      
      // 停止所有媒体流
      if (cameraActive.value) toggleCamera();
      if (microphoneActive.value) toggleMicrophone();
      if (recording.value) toggleRecording();
    };

    // 格式化时间显示
    const interviewDuration = computed(() => {
      const minutes = Math.floor(interviewTime.value / 60);
      const seconds = interviewTime.value % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });
    
    const formattedTime = computed(() => {
      const minutes = Math.floor(interviewTime.value / 60);
      const seconds = interviewTime.value % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    // 媒体控制
    const candidateVideo = ref(null);
    const pipVideo = ref(null);
    const cameraActive = ref(false);
    const microphoneActive = ref(false);
    const recording = ref(false);
    const mediaStream = ref(null);
    const mediaRecorder = ref(null);
    const recordedChunks = ref([]);
    
    // 摄像头切换方法
    const toggleCamera = async () => {
      try {
        if (cameraActive.value) {
          // 关闭摄像头
          if (mediaStream.value) {
            mediaStream.value.getVideoTracks().forEach(track => track.stop());
            mediaStream.value = null;
          }
          cameraActive.value = false;
          
          // 清除所有视频元素的源
          if (candidateVideo.value) {
            candidateVideo.value.srcObject = null;
          }
          if (pipVideo.value) {
            pipVideo.value.srcObject = null;
          }
          
          showNotification('摄像头已关闭', 'fas fa-video-slash');
        } else {
          // 开启摄像头
          const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 1280, height: 720 },
            audio: false
          });
          
          mediaStream.value = stream;
          cameraActive.value = true;
          
          // 根据当前模式设置视频源
          if (isMiddleScreenExpanded.value) {
            // 放大模式 - 主视频和画中画都显示
            if (candidateVideo.value) {
              candidateVideo.value.srcObject = stream;
            }
            if (pipVideo.value) {
              pipVideo.value.srcObject = stream;
              pipVideo.value.play().catch(e => {
                console.warn('画中画播放失败:', e);
                pipVideo.value.muted = true;
                pipVideo.value.play().catch(console.warn);
              });
            }
          } else {
            // 正常模式 - 只显示在主视频
            if (candidateVideo.value) {
              candidateVideo.value.srcObject = stream;
            }
          }
          
          showNotification('摄像头已开启', 'fas fa-video');
        }
      } catch (error) {
        console.error('摄像头错误:', error);
        showNotification('无法访问摄像头', 'fas fa-exclamation-triangle');
      }
    };

    // 麦克风切换方法
    const toggleMicrophone = async () => {
      try {
        if (microphoneActive.value) {
          // 关闭麦克风
          if (mediaStream.value) {
            mediaStream.value.getAudioTracks().forEach(track => track.stop());
            // 保留视频轨道
            const videoTracks = mediaStream.value.getVideoTracks();
            if (videoTracks.length > 0) {
              const newStream = new MediaStream(videoTracks);
              mediaStream.value = newStream;
              
              // 更新视频元素的源
              if (candidateVideo.value) {
                candidateVideo.value.srcObject = newStream;
              }
              if (pipVideo.value) {
                pipVideo.value.srcObject = newStream;
              }
            } else {
              mediaStream.value = null;
            }
          }
          microphoneActive.value = false;
          showNotification('麦克风已关闭', 'fas fa-microphone-slash');
        } else {
          // 开启麦克风
          const audioStream = await navigator.mediaDevices.getUserMedia({ 
            audio: true,
            video: false 
          });
          
          // 合并视频和音频流（如果摄像头已开启）
          if (mediaStream.value?.getVideoTracks().length > 0) {
            const newStream = new MediaStream([
              ...mediaStream.value.getVideoTracks(),
              ...audioStream.getAudioTracks()
            ]);
            
            mediaStream.value = newStream;
          } else {
            // 只有音频的情况
            mediaStream.value = audioStream;
          }
          
          // 更新所有视频元素的源
          if (candidateVideo.value) {
            candidateVideo.value.srcObject = mediaStream.value;
          }
          if (pipVideo.value) {
            pipVideo.value.srcObject = mediaStream.value;
          }
          
          microphoneActive.value = true;
          showNotification('麦克风已开启', 'fas fa-microphone');
        }
      } catch (error) {
        console.error('麦克风错误:', error);
        showNotification('无法访问麦克风', 'fas fa-exclamation-triangle');
      }
    };

    const toggleRecording = () => {
      if (recording.value) {
        // 停止录制
        if (mediaRecorder.value) {
          mediaRecorder.value.stop();
          mediaRecorder.value = null;
        }
        recording.value = false;
        showNotification('录制已停止', 'fas fa-stop-circle');
      } else {
        // 确保有有效的媒体流
        const activeStream = pipVideo.value?.srcObject || mediaStream.value;
        if (!activeStream) {
          showNotification('请先开启摄像头或麦克风', 'fas fa-exclamation-triangle');
          return;
        }

        // 开始录制（使用当前活动的流）
        recordedChunks.value = [];
        mediaRecorder.value = new MediaRecorder(activeStream, {
          mimeType: 'video/webm;codecs=vp9'
        });

        mediaRecorder.value.ondataavailable = (e) => {
          if (e.data.size > 0) recordedChunks.value.push(e.data);
        };

        mediaRecorder.value.onstop = () => {
          const blob = new Blob(recordedChunks.value, { type: 'video/webm' });
          const url = URL.createObjectURL(blob);
          console.log('录制完成:', url);
          // 这里可以添加下载或保存逻辑
        };

        mediaRecorder.value.start(1000);
        recording.value = true;
        showNotification('录制已开始', 'fas fa-circle');
      }
    };

    // AI助手功能 (Vue 3 Composition API)
const assistantExpanded = ref(false);
const unreadMessages = ref(0);
const assistantMessages = ref([
  {
    sender: 'ai',
    text: '您好！我是面试助手，可以随时为您提供帮助。',
    time: new Date().toLocaleTimeString()
  }
]);
const assistantInput = ref('');

// 切换助手展开状态
const toggleAssistantExpanded = () => {
  assistantExpanded.value = !assistantExpanded.value;
  if (assistantExpanded.value) {
    unreadMessages.value = 0;
  }
};

// 发送消息到助手
const sendToAssistant = () => {
  if (!assistantInput.value.trim()) return;
  
  // 添加用户消息
  assistantMessages.value.push({
    sender: 'user',
    text: assistantInput.value,
    time: new Date().toLocaleTimeString()
  });
  
  // 模拟AI回复
  setTimeout(() => {
    const responses = [
      "我理解您的问题。",
      "这是一个很好的问题。",
      "根据我的分析...",
      "建议您可以考虑以下几个方面...",
      "让我为您详细解释一下。"
    ];
    const response = responses[Math.floor(Math.random() * responses.length)];
    assistantMessages.value.push({
      sender: 'ai',
      text: response,
      time: new Date().toLocaleTimeString()
    });
  }, 1000);
  
  assistantInput.value = '';
};

// 语音交互相关功能
const isSpeaking = ref(false);
const isListening = ref(false);
const speechTimeout = ref(null);

const triggerAIResponse = (message = null) => {
  if (!interviewStarted.value) {
    showNotification('请先开始面试', 'fas fa-exclamation-triangle');
    return;
  }
  
  isSpeaking.value = true;
  clearTimeout(speechTimeout.value);
  
  if (!message) {
    const responses = [
      "这是一个很好的问题，让我们深入探讨一下。",
      "我注意到您在这个领域有丰富的经验。",
      "您的回答很有见地。",
      "让我们继续下一个问题。",
      "您对这个话题有什么看法？"
    ];
    message = responses[Math.floor(Math.random() * responses.length)];
  }
  
  // 添加到智能助手对话
  assistantMessages.value.push({
    sender: 'ai',
    text: message,
    time: new Date().toLocaleTimeString()
  });
  
  speechTimeout.value = setTimeout(() => {
    isSpeaking.value = false;
  }, message.length * 100);
};

const toggleAIListening = () => {
  isListening.value = !isListening.value;
  showNotification(
    isListening.value ? 'AI正在监听' : 'AI停止监听',
    isListening.value ? 'fas fa-ear-listen' : 'fas fa-ear'
  );
};

// 动画样式相关
const getBubbleStyle = (index) => ({
  '--delay': `${index * 0.2}s`,
  '--size': `${10 + index * 5}px`,
  '--opacity': `${1 - index * 0.2}`
});

const getListeningStyle = (index) => ({
  '--delay': `${index * 0.2}s`,
  '--height': `${10 + index * 5}px`,
  '--opacity': `${0.5 + index * 0.15}`
});

    // 图表引用
    // 图表引用
const emotionChart = ref(null);
const emotionTrendChart = ref(null);
const skillsRadarChart = ref(null);

// 初始化图表
const initCharts = () => {
  nextTick(() => {
    // 1. 情绪分析饼图
    if (emotionChart.value) {
      const chart = echarts.init(emotionChart.value);
      chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center',
          data: ['自信', '专注', '愉悦', '紧张', '困惑']
        },
        series: [{
          name: '情绪分析',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {c} ({d}%)'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '18',
              fontWeight: 'bold'
            }
          },
          labelLine: {
            show: true
          },
          data: [
            { value: 45, name: '自信', itemStyle: { color: '#4cc9f0' } },
            { value: 25, name: '专注', itemStyle: { color: '#4361ee' } },
            { value: 15, name: '愉悦', itemStyle: { color: '#3f37c9' } },
            { value: 10, name: '紧张', itemStyle: { color: '#f8961e' } },
            { value: 5, name: '困惑', itemStyle: { color: '#ef233c' } }
          ]
        }]
      });
    }

    if (emotionTrendChart.value) {
      const chart = echarts.init(emotionTrendChart.value);
      chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['开始', '5分钟', '10分钟', '15分钟', '20分钟', '25分钟', '30分钟'],
          axisLine: {
            lineStyle: {
              color: '#999'
            }
          }
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLine: {
            lineStyle: {
              color: '#999'
            }
          }
        },
        series: [{
          name: '情绪指数',
          data: [65, 72, 80, 88, 85, 78, 82],
          type: 'line',
          smooth: true,
          lineStyle: {
            width: 4,
            color: '#4cc9f0'
          },
          itemStyle: {
            color: '#4361ee'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(76, 201, 240, 0.5)' },
              { offset: 1, color: 'rgba(76, 201, 240, 0.1)' }
            ])
          }
        }]
      });
    }

    // 2. 技能雷达图
    if (skillsRadarChart.value) {
      const chart = echarts.init(skillsRadarChart.value);
      chart.setOption({
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: ['候选人', '岗位要求']
        },
        radar: {
          indicator: [
            { name: 'JavaScript', max: 100 },
            { name: 'React', max: 100 },
            { name: 'Vue', max: 100 },
            { name: '算法', max: 100 },
            { name: '系统设计', max: 100 },
            { name: '沟通', max: 100 }
          ],
          splitArea: {
            areaStyle: {
              color: ['rgba(255, 255, 255, 0.5)']
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(0, 0, 0, 0.2)'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(0, 0, 0, 0.2)'
            }
          }
        },
        series: [{
          name: '技能对比',
          type: 'radar',
          data: [
            {
              value: [94, 89, 75, 87, 82, 85],
              name: '候选人',
              areaStyle: {
                color: 'rgba(76, 201, 240, 0.4)'
              },
              lineStyle: {
                width: 2,
                color: '#4cc9f0'
              }
            },
            {
              value: [90, 85, 80, 85, 80, 80],
              name: '岗位要求',
              areaStyle: {
                color: 'rgba(248, 150, 30, 0.4)'
              },
              lineStyle: {
                width: 2,
                color: '#f8961e'
              }
            }
          ]
        }]
      });
    }
  });
};

// 在onMounted中调用
onMounted(() => {
  initCharts();
  
  // 添加窗口大小变化监听
  const handleResize = () => {
    [emotionTrendChart, skillsRadarChart].forEach(chartRef => {
      if (chartRef.value && chartRef.value.__echarts_instance__) {
        echarts.getInstanceByDom(chartRef.value).resize();
      }
    });
  };
  
  window.addEventListener('resize', handleResize);
  
  // 组件卸载时清理
  onBeforeUnmount(() => {
    [emotionTrendChart, skillsRadarChart].forEach(chartRef => {
      if (chartRef.value && chartRef.value.__echarts_instance__) {
        echarts.getInstanceByDom(chartRef.value).dispose();
      }
    });
    window.removeEventListener('resize', handleResize);
  });
});
    // 面板控制
    const showNotes = ref(false);
    const showAnalysis = ref(false);
    const interviewStarted = ref(false);
    const interviewId = ref(`AI-${Math.floor(Math.random() * 1000000)}`);
    const interviewNotes = ref('');
    const showEndInterviewModal = ref(false);
    
    const toggleNotesPanel = () => {
      showNotes.value = !showNotes.value;
      if (showNotes.value) {
        showAnalysis.value = false;
      }
    };
    
    const toggleAnalysisPanel = () => {
      showAnalysis.value = !showAnalysis.value;
      if (showAnalysis.value) {
        showNotes.value = false;
      }
    };
    
    const saveNotes = () => {
      console.log('笔记已保存:', interviewNotes.value);
      showNotes.value = false;
      showNotification('笔记已保存', 'fas fa-save');
    };

    // 滚动控制
    const scrollPosition = ref(0);
    const showFooter = ref(true);
    
    const handleScroll = () => {
      scrollPosition.value = window.scrollY;
      showFooter.value = scrollPosition.value < 50;
    };

    // 全屏控制
    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
          console.error(`全屏错误: ${err.message}`);
          showNotification('全屏模式不可用', 'fas fa-exclamation-triangle');
        });
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      }
    };

    // 通知系统
    const notification = reactive({
      show: false,
      text: '',
      icon: '',
      timeout: null
    });
    
    const showNotification = (text, icon = 'fas fa-info-circle') => {
      clearTimeout(notification.timeout);
      notification.text = text;
      notification.icon = icon;
      notification.show = true;
      notification.timeout = setTimeout(() => {
        notification.show = false;
      }, 3000);
    };

    // 进度条颜色
    const getProgressColor = (value) => {
      if (value >= 85) return '#4cc9f0';
      if (value >= 70) return '#4361ee';
      if (value >= 50) return '#f8961e';
      return '#ef233c';
    };

    // 情绪反馈
    const emotionFeedback = ref('候选人表现自信，语言表达清晰，情绪稳定');

    // 初始化
    onMounted(() => {
      initParticles();
      nextTick(() => {
        initCharts();
      });
      window.addEventListener('scroll', handleScroll);
    });
    
    onBeforeUnmount(() => {
      window.removeEventListener('scroll', handleScroll);
      clearInterval(interviewTimer.value);
      if (mediaStream.value) {
        mediaStream.value.getTracks().forEach(track => track.stop());
      }
    });

    return {
      // 状态
    assistantExpanded,
  unreadMessages,
  assistantMessages,
  assistantInput,
  toggleAssistantExpanded,
  sendToAssistant,
  isSpeaking,
  isListening,
  triggerAIResponse,
  toggleAIListening,
  getBubbleStyle,
  getListeningStyle,
      isMiddleScreenExpanded,
      toggleMiddleScreen,
      darkMode,
      leftPanelActive,
      rightPanelActive,
      leftPanelExpanded,
      rightPanelExpanded,
      showNotes,
      showAnalysis,
      interviewStarted,
      currentQuestionIndex,
      questionTime,
      interviewTime,
      scrollPosition,
      showFooter,
      cameraActive,
      microphoneActive,
      recording,
      isSpeaking,
      isListening,
      showEndInterviewModal,
      interviewId,
      candidate,
      aiName,
      aiAvatar,
      questions,
      currentQuestion,
      analysisData,
      analysisSummary,
      particles,
      assistantMessages,
      assistantInput,
      interviewNotes,
      emotionFeedback,
      notification,
      
      // 引用
      candidateVideo,
      pipVideo,
      emotionChart,
      emotionTrendChart,
      skillsRadarChart,
      
      // 方法
      toggleDarkMode,
      toggleFullscreen,
      startInterview,
      endInterview,
      confirmEndInterview,
      toggleCamera,
      toggleMicrophone,
      toggleRecording,
      nextQuestion,
      prevQuestion,
      toggleAutoMode,
      toggleNotesPanel,
      toggleAnalysisPanel,
      saveNotes,
      sendToAssistant,
      triggerAIResponse,
      toggleAIListening,
      getBubbleStyle,
      getListeningStyle,
      particleStyle,
      handleImageError,
      handleAIImageError,
      showNotification,
      toggleLeftPanel,
      toggleRightPanel,
      
      // 计算属性
      interviewProgress,
      interviewDuration,
      formattedTime,
      formatTime,
      getProgressColor
    }
  }
}
;
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');

:root {
  --primary-color: #006EFF;
  --secondary-color: #0052D9;
  --accent-color: #4cc9f0;
  --success-color: #38b000;
  --warning-color: #ffaa00;
  --danger-color: #ef233c;
  --text-color: #333;
  --bg-color: #f5f5f5;
  --card-bg: #fff;
  --border-color: #e1e1e1;
  --shadow-color: rgba(0, 0, 0, 0.1);
}

.dark-mode {
  --text-color: #f0f0f0;
  --bg-color: #0f0f1b;
  --card-bg: rgba(15, 15, 27, 0.7);
  --border-color: rgba(255, 255, 255, 0.1);
  --shadow-color: rgba(0, 0, 0, 0.3);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', 'Microsoft YaHei', sans-serif;
}

.ai-interview-system {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: all 0.3s ease;
  overflow: hidden;

  &.dark-mode {
    background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f1b 70%);
  }
}

.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  z-index: 100;
  box-shadow: 0 2px 10px var(--shadow-color);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  transition: all 0.3s ease;
  
  &.scrolled {
    padding: 8px 24px;
    box-shadow: 0 4px 15px var(--shadow-color);
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 20px;

    .logo {
      height: 32px;
      transition: transform 0.3s;
      
      &:hover {
        transform: rotate(15deg);
      }
    }

    h1 {
      font-size: 20px;
      font-weight: 600;
      background: linear-gradient(to right, var(--primary-color), var(--accent-color));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .interview-info {
      display: flex;
      gap: 15px;
      font-size: 14px;
      opacity: 0.8;

      .interview-id {
        background: rgba(0, 110, 255, 0.1);
        padding: 4px 8px;
        border-radius: 4px;
        transition: all 0.3s;
        
        &:hover {
          background: rgba(0, 110, 255, 0.2);
        }
      }

      .interview-time {
        display: flex;
        align-items: center;
        gap: 5px;
      }
    }
  }

  .header-right {
    display: flex;
    gap: 10px;
  }
}

.control-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &:hover {
    background: rgba(0, 110, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px var(--shadow-color);
  }
  
  &.small {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }

  &.danger {
    &:hover {
      background: rgba(239, 35, 60, 0.2);
    }
  }
}

.interview-main {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
  padding-top: 60px;
}

.candidate-panel {
  width: 280px;
  height: 100%;
  padding: 20px;
  background-color: var(--card-bg);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
  
  &.panel-active {
    transform: translateX(0);
  }
  
  &:not(.panel-active) {
    transform: translateX(-240px);
    width: 40px;
    padding: 20px 5px;
    
    .candidate-card, .interview-controls {
      opacity: 0;
      pointer-events: none;
    }
  }
  
  &.expanded {
    width: 500px;
    z-index: 1000;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    
    .panel-toggle i {
      transform: rotate(180deg);
    }
  }
}

.right-panel {
  width: 400px;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 20px;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  overflow-y: auto;
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
  
  &.panel-active {
    transform: translateX(0);
  }
  
  &:not(.panel-active) {
    transform: translateX(360px);
    width: 40px;
    padding: 20px 5px;
    
    .candidate-view, .ai-assistant {
      opacity: 0;
      pointer-events: none;
    }
  }
  
  &.expanded {
    width: 500px;
    z-index: 1000;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    
    .panel-toggle i {
      transform: rotate(180deg);
    }
  }
}

.panel-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 48px;
  background: rgba(0, 110, 255, 0.1);
  border-radius: 0 12px 12px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  z-index: 10;
  
  &:hover {
    background: rgba(0, 110, 255, 0.2);
  }
  
  i {
    font-size: 12px;
    color: var(--text-color);
    transition: transform 0.3s;
  }
}

.right-panel .panel-toggle {
  left: 10px;
  right: auto;
  border-radius: 12px 0 0 12px;
}

.candidate-card {
  background: rgba(0, 110, 255, 0.05);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px var(--shadow-color);
  transition: all 0.3s ease;

  .candidate-avatar {
    position: relative;
    width: 80px;
    height: 80px;
    margin: 0 auto 15px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(0, 110, 255, 0.3);
    transition: all 0.3s;
    
    &:hover {
      transform: scale(1.05);
      box-shadow: 0 0 20px rgba(0, 110, 255, 0.2);
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .status-indicator {
      position: absolute;
      bottom: 5px;
      right: 5px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #ccc;
      border: 2px solid var(--card-bg);
      transition: all 0.3s;

      &.active {
        background: var(--success-color);
        box-shadow: 0 0 10px var(--success-color);
      }
    }
  }

  .candidate-info {
    text-align: center;

    h3 {
      font-size: 18px;
      margin-bottom: 10px;
      color: var(--text-color);
    }

    p {
      font-size: 14px;
      margin-bottom: 8px;
      opacity: 0.8;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;

      i {
        color: var(--primary-color);
      }

      .match-score {
        font-weight: 600;
        color: var(--accent-color);
      }
    }
  }
}

.interview-controls {
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.3s;
  
  .start-btn {
    padding: 12px;
    border-radius: 8px;
    background: var(--primary-color);
    border: none;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    &:hover {
      background: var(--secondary-color);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 110, 255, 0.3);
    }
    
    &:disabled {
      background: #ccc;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }
  }
  
  .timer-display {
    padding: 10px;
    background: rgba(0, 110, 255, 0.1);
    border-radius: 8px;
    text-align: center;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    i {
      color: var(--accent-color);
    }
  }
}

.ai-interviewer {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  position: relative;
}

.video-container {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 8px 24px var(--shadow-color);
  transition: all 0.3s;
  
  &.active-speech {
    box-shadow: 0 0 30px rgba(76, 201, 240, 0.3);
    
    .ai-3d-model {
      &::before {
        opacity: 0.3;
      }
      
      .ai-3d-effects {
        opacity: 1;
      }
    }
  }
  
  &.pulse {
    animation: pulseGlow 2s infinite alternate;
  }
}

@keyframes pulseGlow {
  0% {
    box-shadow: 0 0 10px rgba(76, 201, 240, 0.3);
  }
  100% {
    box-shadow: 0 0 30px rgba(76, 201, 240, 0.6);
  }
}

.ai-3d-model {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.5s ease;
  cursor: pointer;
  perspective: 1000px;
  transform-style: preserve-3d;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(76, 201, 240, 0.3), transparent 70%);
    opacity: 0;
    transition: opacity 0.5s ease;
    z-index: 1;
  }
  
  &:hover {
    .ai-avatar-img {
      transform: rotateY(10deg) scale(1.05);
    }
  }
}

.ai-avatar-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.ai-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  filter: brightness(1.1);
  z-index: 2;
  transition: transform 0.5s ease;
  backface-visibility: hidden;
}

.ai-3d-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  
  .particle {
    position: absolute;
    background: #4cc9f0;
    border-radius: 50%;
    filter: blur(1px);
    transform: translate(-50%, -50%);
    
    @keyframes float {
      0% { transform: translate(-50%, -50%); }
      100% { transform: translate(-50%, calc(-50% - 20px)); }
    }
  }
  
  &::before, &::after {
    content: '';
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(76, 201, 240, 0.3), transparent 70%);
    animation: pulse 4s infinite;
  }
  
  &::before {
    width: 200px;
    height: 200px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation-delay: 0.5s;
  }
  
  &::after {
    width: 300px;
    height: 300px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.2; }
  100% { transform: translate(-50%, -50%) scale(0.8); opacity: 0.5; }
}

.ai-status {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  
  &.listening {
    .listening-animation {
      span {
        display: inline-block;
        width: 6px;
        height: var(--height);
        margin: 0 2px;
        background-color: var(--accent-color);
        border-radius: 3px;
        animation: listening 1.5s infinite ease-in-out;
        animation-delay: var(--delay);
        opacity: var(--opacity);
      }
    }
  }
}

@keyframes listening {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1.5); }
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent 30%, transparent 70%, rgba(0,0,0,0.7));
  padding: 20px;
  z-index: 3;
}

.ai-identity {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: white;
  text-align: center;
  z-index: 3;

  .ai-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(76, 201, 240, 0.5);
    box-shadow: 0 0 20px rgba(76, 201, 240, 0.3);
    transition: all 0.3s;
    
    &:hover {
      transform: scale(1.05);
      box-shadow: 0 0 30px rgba(76, 201, 240, 0.5);
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  h3 {
    font-size: 18px;
    font-weight: 600;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    background: linear-gradient(to right, #4cc9f0, #4361ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  p {
    font-size: 14px;
    opacity: 0.9;
  }
}

.ai-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  z-index: 3;
}

.ai-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 3;

  &:hover {
    background: var(--accent-color);
    transform: scale(1.1);
    box-shadow: 0 0 15px rgba(76, 201, 240, 0.5);
  }
}

.question-box {
  position: absolute;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  padding: 15px;
  color: white;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(76, 201, 240, 0.3);
  z-index: 3;
  transition: all 0.3s;

  h4 {
    font-size: 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--accent-color);
  }

  p {
    font-size: 16px;
    line-height: 1.5;
  }

  .question-timer {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 12px;
    opacity: 0.8;
    display: flex;
    align-items: center;
    gap: 5px;
  }
}

.speech-animation {
  position: absolute;
  bottom: 180px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 3;
}

.speech-bubble {
  width: var(--size);
  height: var(--size);
  background-color: var(--accent-color);
  border-radius: 50%;
  opacity: var(--opacity);
  animation: bubble 1.5s infinite ease-in-out;
  animation-delay: var(--delay);
}

@keyframes bubble {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-10px) scale(1.2); }
}

.candidate-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: all 0.3s;
}

.video-container {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.1);
  
  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    background: #000;
  }
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 15px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  z-index: 2;
}

.emotion-analysis {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 15px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px var(--shadow-color);
  transition: all 0.3s;

  h4 {
    font-size: 16px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-color);

    i {
      color: var(--primary-color);
    }
  }

  .emotion-chart {
    width: 100%;
    height: 200px;
    margin-bottom: 15px;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    background: rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    border: 1px solid var(--border-color);
    padding: 10px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
    font-size: 14px;
  }

  .emotion-feedback {
    background: rgba(0, 110, 255, 0.05);
    border-radius: 8px;
    padding: 12px;
    border-left: 3px solid var(--accent-color);
    transition: all 0.3s;

    p {
      font-size: 14px;
      line-height: 1.5;
      display: flex;
      align-items: flex-start;
      gap: 8px;

      i {
        color: var(--accent-color);
        margin-top: 2px;
      }
    }
  }
}


/* 展开动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}



.message {
  animation: fadeIn 0.3s ease;
}
@media (max-width: 480px) {
  .ai-assistant-floating {
    bottom: 10px;
    right: 10px;
  }
  
  .assistant-container {
    width: calc(100vw - 40px);
    max-height: 60vh;
  }
  
  .assistant-trigger {
    width: 50px;
    height: 50px;
  }
}
.interview-footer {
  display: flex;
  height: 90px; /* 明确高度 */
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: var(--card-bg);
  border-top: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  z-index: 1000;
  box-shadow: 0 -2px 10px var(--shadow-color);
  transition: all 0.3s ease;
  
  &.footer-hidden {
    transform: translateY(100%);
    opacity: 0;
  }
}

.action-btn {
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;

  &:hover {
    background: rgba(0, 110, 255, 0.2);
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  &.primary {
    background: var(--primary-color);
    color: white;

    &:hover {
      background: var(--secondary-color);
    }
  }
}

.interview-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;

  .progress-bar {
    width: 200px;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    overflow: hidden;

    .progress-fill {
      height: 100%;
      background: linear-gradient(to right, var(--primary-color), var(--accent-color));
      transition: width 0.5s ease;
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressShine 2s infinite;
      }
    }
  }
}

.notes-panel,
.analysis-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--card-bg);
  border-top: 1px solid var(--border-color);
  box-shadow: 0 -5px 20px var(--shadow-color);
  z-index: 1000;
  padding: 20px;
  max-height: 60vh;
  overflow-y: auto;
  backdrop-filter: blur(10px);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;

  h4 {
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .close-btn {
    background: none;
    border: none;
    color: var(--text-color);
    font-size: 18px;
    cursor: pointer;
    opacity: 0.7;
    transition: opacity 0.3s;

    &:hover {
      opacity: 1;
    }
  }
}

textarea {
  width: 100%;
  min-height: 150px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-color);
  font-size: 14px;
  resize: none;
  margin-bottom: 15px;
  transition: all 0.3s;

  &:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 10px rgba(0, 110, 255, 0.2);
  }
}

.panel-footer {
  display: flex;
  justify-content: flex-end;
}

.save-btn {
  padding: 8px 16px;
  border-radius: 20px;
  background: var(--primary-color);
  border: none;
  color: white;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;

  &:hover {
    background: var(--secondary-color);
    transform: translateY(-2px);
  }
}

.analysis-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.analysis-section {
  h5 {
    font-size: 16px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-color);

    i {
      color: var(--primary-color);
    }
  }

  .chart-container,
  .skills-radar {
    width: 100%;
    height: 250px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    backdrop-filter: blur(5px);
    border: 1px solid var(--border-color);
    padding: 10px;
    box-sizing: border-box;
  }

  .progress-bars {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 10px;
  }

  .progress-item {
    .progress-label {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      margin-bottom: 5px;
    }

    .progress-bar {
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.5s ease;
      position: relative;
      overflow: hidden;

      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressShine 2s infinite;
      }
    }
  }
  
  .analysis-summary {
    margin-top: 20px;
    padding: 15px;
    background: rgba(0, 110, 255, 0.05);
    border-radius: 8px;
    border-left: 3px solid var(--accent-color);
    
    h6 {
      font-size: 14px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--accent-color);
    }
    
    p {
      font-size: 14px;
      line-height: 1.6;
    }
  }
}

@keyframes progressShine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 10px 30px var(--shadow-color);
  border: 1px solid var(--border-color);
  animation: modalIn 0.3s ease;

  h3 {
    font-size: 20px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--text-color);
  }

  p {
    margin-bottom: 20px;
    font-size: 15px;
    line-height: 1.5;
  }
}

@keyframes modalIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}


  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;

}

.panel-expand-enter-active,
.panel-expand-leave-active {
  transition: all 0.3s ease;
}

.panel-expand-enter-from,
.panel-expand-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .right-panel {
    width: 350px;
    
    &:not(.panel-active) {
      transform: translateX(310px);
    }
  }
}

@media (max-width: 992px) {
  .interview-main {
    flex-direction: column;
  }

  .candidate-panel {
    width: 100%;
    height: auto;
    flex-direction: row;
    overflow-x: auto;
    padding: 15px;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    
    &.panel-active, &:not(.panel-active) {
      transform: none;
      width: 100%;
      padding: 15px;
    }
    
    .panel-toggle {
      display: none;
    }
    
    .candidate-card, .interview-controls {
      opacity: 1 !important;
      pointer-events: auto !important;
    }
  }

  .right-panel {
    width: 100%;
    height: auto;
    border-left: none;
    border-top: 1px solid var(--border-color);
    
    &.panel-active, &:not(.panel-active) {
      transform: none;
      width: 100%;
      padding: 15px;
    }
    
    .panel-toggle {
      display: none;
    }
    
    .candidate-view, .ai-assistant {
      opacity: 1 !important;
      pointer-events: auto !important;
    }
  }

  .analysis-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .interview-header {
    flex-direction: column;
    gap: 10px;
    padding: 12px;

    .header-left {
      flex-direction: column;
      gap: 5px;
      text-align: center;

      .interview-info {
        flex-direction: column;
        gap: 5px;
      }
    }
  }

  .interview-footer {
    flex-direction: column;
    gap: 10px;
    padding: 12px;

    .footer-left,
    .footer-right {
      width: 100%;
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 5px;
    }

    .footer-center {
      width: 100%;
    }
  }
  
  .analysis-section {
    .chart-container,
    .skills-radar {
      height: 200px;
    }
  }
}


/* 确保在放大时隐藏滚动条 */
body.screen-expanded {
  overflow: hidden;
}


/* 画中画容器样式 */


/* 画中画头部 */
.pip-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 14px;
  font-weight: 500;
}

/* 画中画关闭按钮 */
.pip-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  opacity: 0.7;
  transition: all 0.2s ease;
  padding: 4px;
  border-radius: 50%;
  
  &:hover {
    opacity: 1;
    background: rgba(255, 255, 255, 0.1);
  }

  i {
    font-size: 12px;
  }
}

/* 画中画视频容器 */
.pip-video-container {
  width: 100%;
  height: 135px;
  background: #000;
  position: relative;
  
  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

/* 画中画控制按钮区域 */
.pip-controls {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.5);
  
  .control-btn {
    width: 32px;
    height: 32px;
    font-size: 12px;
    background: rgba(255, 255, 255, 0.1);
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  }
}

/* 中间区域放大时的样式 */
.ai-interviewer {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  transition: all 0.3s ease;
  
  &.expanded {
    position: fixed;
    top: 50px;
    left: 0;
    right: 0;
     bottom: calc(100px + 12px); /* 底部控制栏高度(100px) + 额外间距(12px) */
    z-index: 1000;
    padding: 0;
    background: var(--bg-color);
    
    .video-container {
      border-radius: 0;
      height: 100%;
    }
    
    /* 隐藏右侧面板 */
    ~ .right-panel {
      display: none;
    }
  }
}

/* 视频容器基础样式 */
.video-container {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 8px 24px var(--shadow-color);
  transition: all 0.3s;
}

/* 全屏状态处理 */
body.screen-expanded {
  overflow: hidden;
  
  .interview-header {
    z-index: 1001;
  }
  
  .interview-footer {
    z-index: 1001;
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .candidate-pip {
    width: 180px;
    top: 10px;
    right: 10px;
    
    .pip-video-container {
      height: 100px;
    }
  }
  
  .ai-interviewer.expanded {
    top: 50px;
    bottom: 200px;
  }
  
  .pip-controls .control-btn {
    width: 28px;
    height: 28px;
    font-size: 11px;
  }
}

/* 暗色模式适配 */
.dark-mode {
  .candidate-pip {
    border-color: rgba(255, 255, 255, 0.15);
    
    .pip-header {
      background: rgba(0, 0, 0, 0.7);
    }
    
    .pip-controls {
      background: rgba(0, 0, 0, 0.7);
    }
  }
}

/* 动画效果 */
@keyframes pipFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.candidate-pip {
  animation: pipFadeIn 0.3s ease-out forwards;
}

/* 确保画中画视频正确显示 */
.pip-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #000;
}

/* 当画中画激活时 */
.ai-interviewer.expanded .pip-video {
  visibility: visible;
}


/* 主视频样式 */
.main-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: #000;
}

/* 画中画容器定位 */
.candidate-pip {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 240px;
  z-index: 10;
}
/* 助手面板容器 */
.assistant-panel {
  position: fixed;
  bottom: 80px;
  right: 30px;
  width: 380px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 82, 204, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e1e8ed;
  z-index: 1000;
}

/* 面板头部 */
.assistant-header {
  padding: 16px 20px;
  background: #1a73e8;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.assistant-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.close-btn {
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

/* 消息区域 */
.assistant-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #f8fafd;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 消息气泡 */
.message {
  display: flex;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
}

.message.ai {
  align-self: flex-start;
}

.message-content {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  font-size: 14px;
  position: relative;
  word-break: break-word;

}

.message.user .message-content {
  background: #1a73e8;
  color: white;
  border-bottom-right-radius: 4px;
  
}



.assistant-input input:focus {
  border-color: #1a73e8;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
}


/* 通知徽章 */
.notification-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}



.assistant-messages::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}


}


/* 新增样式（确保不影响现有布局） */
/* 头像容器（保持原有布局） */
.avatar-placeholder {
  /* 保持你原有的样式，不添加任何定位或尺寸修改 */
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
