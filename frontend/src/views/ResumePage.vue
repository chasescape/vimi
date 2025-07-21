<template>
    <div class="cyber-gradient">
        <div class="cyber-grid"></div>
        <div class="cyber-pulse"></div>
        <div class="cyber-orb" style="top: 10%; left: 10%; animation-delay: 0s;"></div>
        <div class="cyber-orb" style="top: 70%; left: 80%; animation-delay: 3s;"></div>
        <div class="cyber-orb" style="top: 30%; left: 60%; animation-delay: 6s;"></div>

        <header>
            <div class="container header-content">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <span>未来科技AI</span>
                </div>
                <nav class="nav-links">
                    <a href="#upload">简历优化</a>
                    <a href="#features">核心功能</a>
                    <a href="#analysis">AI分析</a>
                    <a href="#preview">简历预览</a>
                    <a href="#contact">联系我们</a>
                </nav>
            </div>
        </header>

        <main class="container">
            <section class="main-title">
                <h1>AI智能简历优化平台</h1>
                <p>利用先进的人工智能技术，为您的简历提供专业级的优化建议，提升求职成功率</p>
            </section>

            <section id="upload" class="upload-section">
                <div class="upload-card">
                    <div class="upload-icon">
                        <i class="fas fa-file-upload"></i>
                    </div>
                    <h2>上传您的简历</h2>
                    <p>支持PDF、Word、TXT等多种格式，我们的AI将立即分析您的简历并提供优化建议</p>

                    <input type="file" ref="fileInputRef" class="file-input" accept=".pdf,.doc,.docx,.txt">
                    <button class="upload-btn" ref="uploadTriggerRef" @click="handleUploadClick">
                        <i class="fas fa-cloud-upload-alt"></i> 选择文件上传
                    </button>

                    <div class="upload-progress" ref="uploadProgressRef">
                        <div class="upload-progress-bar" ref="progressBarRef"></div>
                    </div>

                    <div class="upload-success" ref="uploadSuccessRef">
                        <i class="fas fa-check-circle"></i> 简历上传成功！AI正在分析中...
                    </div>
                </div>
            </section>

            <section id="features" class="features-section">
                <h2 class="section-title"><i class="fas fa-star"></i> 核心功能</h2>

                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-magic"></i>
                        </div>
                        <h3>智能内容优化</h3>
                        <p>AI自动分析简历内容，提供关键词优化建议，使您的简历更符合职位要求，轻松通过ATS筛选系统。</p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h3>竞争力分析</h3>
                        <p>与同职位其他候选人简历对比，展示您的优势与不足，提供针对性的改进建议。</p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-bullseye"></i>
                        </div>
                        <h3>职位匹配度</h3>
                        <p>上传职位描述，AI将计算您的简历与该职位的匹配程度，并指出需要加强的部分。</p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-edit"></i>
                        </div>
                        <h3>实时编辑预览</h3>
                        <p>在线编辑简历，实时查看优化效果，多种专业模板一键切换，打造完美简历。</p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-graduation-cap"></i>
                        </div>
                        <h3>职业发展建议</h3>
                        <p>基于您的经历和技能，AI提供职业发展路径建议和需要提升的关键技能。</p>
                    </div>

                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-file-export"></i>
                        </div>
                        <h3>多格式导出</h3>
                        <p>优化后的简历可导出为PDF、Word等多种格式，支持一键投递至各大招聘平台。</p>
                    </div>
                </div>
            </section>

            <section id="analysis" class="analysis-section">
                <h2 class="section-title"><i class="fas fa-brain"></i> AI深度分析</h2>

                <div class="analysis-container">
                    <div class="analysis-visual">
                        <div ref="resume3dRef" class="resume-3d-element"></div>
                    </div>

                    <div class="analysis-content">
                        <h2>全方位简历评估</h2>
                        <p>我们的AI系统从内容结构、关键词匹配、可读性、成就量化等12个维度对您的简历进行全面评估，提供专业级的优化建议。</p>
                        <p>通过机器学习数百万份成功简历，我们的算法能精准识别简历中的问题，并给出具体的改进方案。</p>

                        <div class="analysis-stats">
                            <div class="stat-item">
                                <h4>内容完整性</h4>
                                <p>92%</p>
                            </div>
                            <div class="stat-item">
                                <h4>关键词匹配</h4>
                                <p>87%</p>
                            </div>
                            <div class="stat-item">
                                <h4>成就量化</h4>
                                <p>78%</p>
                            </div>
                            <div class="stat-item">
                                <h4>可读性</h4>
                                <p>95%</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="preview" class="resume-preview">
                <div class="preview-container">
                    <div class="preview-header">
                        <h2>简历优化预览</h2>
                        <div class="preview-actions">
                            <button class="preview-btn">
                                <i class="fas fa-download"></i> 下载PDF
                            </button>
                            <button class="preview-btn">
                                <i class="fas fa-edit"></i> 在线编辑
                            </button>
                            <button class="preview-btn">
                                <i class="fas fa-share-alt"></i> 分享
                            </button>
                        </div>
                    </div>

                    <div class="preview-content">
                        <div class="preview-sidebar">
                            <div style="text-align: center; margin-bottom: 30px;">
                                <div
                                    style="width: 120px; height: 120px; background: #333; border-radius: 50%; margin: 0 auto 15px;">
                                </div>
                                <h3 style="color: white; margin-bottom: 5px;">张小明</h3>
                                <p style="color: var(--accent-color); font-weight: 500;">高级前端开发工程师</p>
                            </div>

                            <div style="margin-bottom: 25px;">
                                <h4
                                    style="color: var(--accent-color); margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                                    <i class="fas fa-info-circle"></i> 基本信息
                                </h4>
                                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 8px;"><strong>电话：</strong>
                                    138-0013-8000</p>
                                <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 8px;"><strong>邮箱：</strong>
                                    zhangxiaoming@email.com</p>
                                <p style="color: rgba(255, 255, 255, 0.8);"><strong>GitHub：</strong> github.com/xiaoming</p>
                            </div>

                            <div>
                                <h4
                                    style="color: var(--accent-color); margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                                    <i class="fas fa-code"></i> 技术技能
                                </h4>
                                <p style="color: white; margin-bottom: 10px;">JavaScript/TypeScript</p>
                                <div
                                    style="height: 5px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; margin-bottom: 15px;">
                                    <div
                                        style="height: 100%; width: 90%; background: var(--accent-color); border-radius: 5px;">
                                    </div>
                                </div>

                                <p style="color: white; margin-bottom: 10px;">React/Vue</p>
                                <div
                                    style="height: 5px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; margin-bottom: 15px;">
                                    <div
                                        style="height: 100%; width: 85%; background: var(--accent-color); border-radius: 5px;">
                                    </div>
                                </div>

                                <p style="color: white; margin-bottom: 10px;">Node.js</p>
                                <div
                                    style="height: 5px; background: rgba(255, 255, 255, 0.1); border-radius: 5px; margin-bottom: 15px;">
                                    <div
                                        style="height: 100%; width: 80%; background: var(--accent-color); border-radius: 5px;">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="preview-main">
                            <div style="margin-bottom: 30px;">
                                <h3
                                    style="color: white; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                                    个人简介</h3>
                                <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                                    5年前端开发经验，精通现代前端技术栈，主导过多个大型项目的前端架构设计和实现。擅长性能优化和组件化开发，对用户体验有深刻理解。热爱技术分享，团队协作能力强。
                                </p>
                            </div>

                            <div style="margin-bottom: 30px;">
                                <h3
                                    style="color: white; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                                    工作经历</h3>

                                <div style="margin-bottom: 20px;">
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                        <h4 style="color: white;">高级前端工程师 | ABC科技有限公司</h4>
                                        <p style="color: var(--accent-color);">2019.06 - 至今</p>
                                    </div>
                                    <ul style="color: rgba(255, 255, 255, 0.8); padding-left: 20px; line-height: 1.8;">
                                        <li>负责公司核心产品的前端架构设计和开发，使用React+TypeScript技术栈</li>
                                        <li>主导前端性能优化项目，将页面加载时间减少40%</li>
                                        <li>设计并实现组件库，提高团队开发效率30%</li>
                                    </ul>
                                </div>

                                <div>
                                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                        <h4 style="color: white;">前端开发工程师 | XYZ网络公司</h4>
                                        <p style="color: var(--accent-color);">2017.03 - 2019.05</p>
                                    </div>
                                    <ul style="color: rgba(255, 255, 255, 0.8); padding-left: 20px; line-height: 1.8;">
                                        <li>参与公司多个项目的前端开发，使用Vue.js技术栈</li>
                                        <li>负责移动端H5页面开发，优化用户体验</li>
                                        <li>协助团队建立前端开发规范和工作流程</li>
                                    </ul>
                                </div>
                            </div>

                            <div>
                                <h3
                                    style="color: white; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                                    教育背景</h3>
                                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                    <h4 style="color: white;">计算机科学与技术 | 清华大学</h4>
                                    <p style="color: var(--accent-color);">2013.09 - 2017.06</p>
                                </div>
                                <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.8;">
                                    主修课程：数据结构与算法、操作系统、计算机网络、数据库系统等
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="preview-ai-suggestions">
                        <h4><i class="fas fa-lightbulb"></i> AI优化建议</h4>

                        <div class="suggestion-item">
                            <div class="suggestion-icon"><i class="fas fa-check"></i></div>
                            <div class="suggestion-text">
                                <strong>优势：</strong> 技术栈描述清晰，工作经历量化指标明确，教育背景优秀。
                            </div>
                        </div>

                        <div class="suggestion-item">
                            <div class="suggestion-icon"><i class="fas fa-bolt"></i></div>
                            <div class="suggestion-text">
                                <strong>建议1：</strong> 在个人简介中添加更多与目标职位相关的关键词，如"前端架构"、"性能优化"等。
                            </div>
                        </div>

                        <div class="suggestion-item">
                            <div class="suggestion-icon"><i class="fas fa-bolt"></i></div>
                            <div class="suggestion-text">
                                <strong>建议2：</strong> 在工作经历中增加更多具体数据，如"用户增长XX%"、"性能提升XX毫秒"等。
                            </div>
                        </div>

                        <div class="suggestion-item">
                            <div class="suggestion-icon"><i class="fas fa-bolt"></i></div>
                            <div class="suggestion-text">
                                <strong>建议3：</strong> 添加"项目经验"部分，详细描述2-3个代表性项目，展示技术深度和解决问题的能力。
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section class="cta-section">
                <div class="cta-card">
                    <h2>立即优化您的简历</h2>
                    <p>上传您的简历，体验AI智能优化服务，让您的简历在众多求职者中脱颖而出，获得更多面试机会。</p>
                    <button class="cta-btn">
                        <i class="fas fa-rocket"></i> 免费开始优化
                    </button>
                </div>
            </section>
        </main>

        <footer id="contact">
            <div class="container">
                <div class="footer-content">
                    <div class="footer-column">
                        <h3>关于我们</h3>
                        <ul>
                            <li><a href="#"><i class="fas fa-info-circle"></i> 公司简介</a></li>
                            <li><a href="#"><i class="fas fa-users"></i> 团队介绍</a></li>
                            <li><a href="#"><i class="fas fa-newspaper"></i> 新闻动态</a></li>
                            <li><a href="#"><i class="fas fa-briefcase"></i> 加入我们</a></li>
                        </ul>
                    </div>

                    <div class="footer-column">
                        <h3>产品服务</h3>
                        <ul>
                            <li><a href="#"><i class="fas fa-file-alt"></i> 简历优化</a></li>
                            <li><a href="#"><i class="fas fa-clipboard-check"></i> 面试辅导</a></li>
                            <li><a href="#"><i class="fas fa-chart-line"></i> 职业规划</a></li>
                            <li><a href="#"><i class="fas fa-graduation-cap"></i> 技能提升</a></li>
                        </ul>
                    </div>

                    <div class="footer-column">
                        <h3>帮助中心</h3>
                        <ul>
                            <li><a href="#"><i class="fas fa-question-circle"></i> 常见问题</a></li>
                            <li><a href="#"><i class="fas fa-book"></i> 使用指南</a></li>
                            <li><a href="#"><i class="fas fa-shield-alt"></i> 隐私政策</a></li>
                            <li><a href="#"><i class="fas fa-file-contract"></i> 服务条款</a></li>
                        </ul>
                    </div>

                    <div class="footer-column">
                        <h3>联系我们</h3>
                        <ul>
                            <li><a href="#"><i class="fas fa-envelope"></i> contact@futuretech.com</a></li>
                            <li><a href="#"><i class="fas fa-phone"></i> 400-888-9999</a></li>
                            <li><a href="#"><i class="fas fa-map-marker-alt"></i> 北京市海淀区科技园路88号</a></li>
                        </ul>
                        <div class="social-links">
                            <a href="#"><i class="fab fa-weixin"></i></a>
                            <a href="#"><i class="fab fa-weibo"></i></a>
                            <a href="#"><i class="fab fa-linkedin"></i></a>
                            <a href="#"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                </div>

                <div class="copyright">
                    &copy; 2023 未来科技AI. 保留所有权利. | 由AI驱动的智能求职平台
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import * as THREE from 'three'
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

// 3D相关的 refs
const emotion3DChartRef = ref<HTMLDivElement | null>(null)
const emotionRadar3DRef = ref<HTMLDivElement | null>(null)
const match3DChartRef = ref<HTMLDivElement | null>(null)
const sphereContainerRef = ref<HTMLDivElement | null>(null)

// 文件上传相关的 refs
const fileInputRef = ref<HTMLInputElement | null>(null)
const uploadTriggerRef = ref<HTMLButtonElement | null>(null)
const uploadProgressRef = ref<HTMLDivElement | null>(null)
const progressBarRef = ref<HTMLDivElement | null>(null)
const uploadSuccessRef = ref<HTMLDivElement | null>(null)

// 处理上传点击
const handleUploadClick = () => {
    fileInputRef.value?.click()
}

// 处理文件变化
const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
        // 显示上传进度
        if (uploadProgressRef.value) {
            uploadProgressRef.value.style.display = 'block'
        }
        if (uploadSuccessRef.value) {
            uploadSuccessRef.value.style.display = 'none'
        }

        // 模拟上传进度
        let progress = 0
        const interval = setInterval(() => {
            progress += Math.random() * 10
            if (progress >= 100) {
                progress = 100
                clearInterval(interval)

                // 上传完成，显示成功消息
                setTimeout(() => {
                    if (uploadProgressRef.value) {
                        uploadProgressRef.value.style.display = 'none'
                    }
                    if (uploadSuccessRef.value) {
                        uploadSuccessRef.value.style.display = 'block'
                    }
                }, 500)
            }
            if (progressBarRef.value) {
                progressBarRef.value.style.width = `${progress}%`
            }
        }, 200)
    }
}

// 卡片悬停效果
const handleCardHover = (e: MouseEvent, card: HTMLElement) => {
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    const angleY = (x - centerX) / 20
    const angleX = (centerY - y) / 20

    card.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateY(-10px)`
    card.style.boxShadow = `0 20px 40px rgba(0, 0, 0, 0.3)`
}

const handleCardLeave = (card: HTMLElement) => {
    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)'
    card.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.2)'
}

// Three.js 相关变量
let renderer: THREE.WebGLRenderer | null = null
let animationId: number | null = null

onMounted(() => {
    // 添加文件变化监听器
    fileInputRef.value?.addEventListener('change', handleFileChange)

    // 卡片悬停效果
    document.querySelectorAll('.card, .feature-card, .upload-card').forEach(card => {
        if (card instanceof HTMLElement) {
            card.addEventListener('mousemove', (e) => handleCardHover(e as MouseEvent, card))
            card.addEventListener('mouseleave', () => handleCardLeave(card))
        }
    })

    // 3D图表初始化
    if (emotion3DChartRef.value) {
        const chart = echarts.init(emotion3DChartRef.value)
        // chart.setOption(...)
    }

    // Three.js 相关代码...
})

onUnmounted(() => {
    // 移除文件变化监听器
    fileInputRef.value?.removeEventListener('change', handleFileChange)

    // 清理 Three.js 资源
    if (animationId) {
        cancelAnimationFrame(animationId)
    }
    if (renderer) {
        renderer.dispose()
        renderer = null
    }
})
</script>

<style scoped>
    :root {
        --primary-color: #4CC9F0;
        --secondary-color: #4361EE;
        --dark-color: #0f0f1b;
        --light-color: #ffffff;
        --accent-color: #48CAE4;
        --success-color: #38b000;
        --warning-color: #ffaa00;
        --danger-color: #ef233c;
        --card-bg: rgba(15, 15, 27, 0.7);
        --text-primary: rgba(255, 255, 255, 0.95);
        --text-secondary: rgba(255, 255, 255, 0.8);
        --text-tertiary: rgba(255, 255, 255, 0.6);
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', 'Microsoft YaHei', sans-serif;
        color: var(--text-primary);
    }
    
    body {
        background-color: var(--dark-color);
        color: var(--text-primary);
        line-height: 1.6;
        overflow-x: hidden;
        perspective: 1000px;
    }
    
    .cyber-gradient {
        background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f1b 70%);
        min-height: 100vh;
        position: relative;
    }
    
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
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-50px, -50px); }
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
    
    @keyframes pulse {
        0% { transform: scale(0.5); opacity: 0.5; }
        50% { transform: scale(1); opacity: 0.2; }
        100% { transform: scale(0.5); opacity: 0.5; }
    }
    
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }
    
    header {
        padding: 30px 0;
        position: relative;
        z-index: 200;
        backdrop-filter: blur(10px);
        background: rgba(15, 15, 27, 0.7);
        border-bottom: 1px solid rgba(76, 201, 240, 0.2);
        margin-bottom: 30px;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        z-index: 200;
    }
    
    .logo {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(to right, var(--accent-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        text-shadow: 0 0 2px rgba(76, 201, 240, 0.2);
        letter-spacing: 1px;
        filter: brightness(1.2);
        position: relative;
        z-index: 200;
    }
    
    .logo i {
        margin-right: 10px;
        font-size: 32px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .nav-links {
        display: flex;
        gap: 30px;
    }
    
    .nav-links a {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s;
        position: relative;
    }
    
    .nav-links a:hover {
        color: var(--accent-color);
    }
    
    .nav-links a::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 0;
        height: 2px;
        background: var(--accent-color);
        transition: width 0.3s;
    }
    
    .nav-links a:hover::after {
        width: 100%;
    }
    
    .main-title {
        text-align: center;
        margin: 60px 0;
        position: relative;
        z-index: 200;
    }
    
    .main-title h1 {
        font-size: 4rem;
        margin-bottom: 20px;
        background: linear-gradient(120deg, #48CAE4, #4361EE, #48CAE4);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        text-shadow: 0 0 20px rgba(72, 202, 228, 0.3);
    }
    
    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }
    
    .main-title p {
        color: var(--text-secondary);
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.8;
    }
    
    .upload-section {
        display: flex;
        justify-content: center;
        margin: 80px 0;
    }
    
    .upload-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 60px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(76, 201, 240, 0.3);
        transform-style: preserve-3d;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        width: 100%;
        max-width: 800px;
        text-align: center;
    }
    
    .upload-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(76, 201, 240, 0.1), transparent);
        transform: rotate(45deg);
        transition: 0.5s;
    }
    
    .upload-card:hover {
        transform: translateY(-15px) rotateX(5deg) rotateY(5deg);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border-color: var(--accent-color);
    }
    
    .upload-card:hover::before {
        left: 100%;
    }
    
    .upload-icon {
        width: 120px;
        height: 120px;
        background: rgba(76, 201, 240, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 30px;
        font-size: 50px;
        color: var(--accent-color);
        border: 2px solid rgba(76, 201, 240, 0.3);
        transition: all 0.3s;
    }
    
    .upload-card:hover .upload-icon {
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        color: white;
        transform: rotateY(180deg);
        box-shadow: 0 0 30px rgba(76, 201, 240, 0.7);
    }
    
    .upload-card h2 {
        margin-bottom: 20px;
        font-size: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .upload-card p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    .upload-btn {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
        position: relative;
        overflow: hidden;
        display: inline-flex;
        align-items: center;
        z-index: 1;
        font-size: 1.1rem;
        margin-top: 20px;
    }
    
    .upload-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
        z-index: -1;
    }
    
    .upload-btn:hover::before {
        left: 100%;
    }
    
    .upload-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.6);
    }
    
    .upload-btn i {
        margin-right: 10px;
        font-size: 20px;
    }
    
    .file-input {
        display: none;
    }
    
    .features-section {
        margin: 100px 0;
    }
    
    .section-title {
        font-size: 2.5rem;
        margin-bottom: 60px;
        background: linear-gradient(to right, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        text-align: center;
    }
    
    .section-title i {
        margin-right: 20px;
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 40px;
    }
    
    .feature-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 40px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(76, 201, 240, 0.3);
        transform-style: preserve-3d;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(76, 201, 240, 0.1), transparent);
        transform: rotate(45deg);
        transition: 0.5s;
    }
    
    .feature-card:hover {
        transform: translateY(-15px) rotateX(5deg) rotateY(5deg);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        border-color: var(--accent-color);
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-icon {
        width: 70px;
        height: 70px;
        background: rgba(76, 201, 240, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 25px;
        font-size: 30px;
        color: var(--accent-color);
        border: 2px solid rgba(76, 201, 240, 0.3);
        transition: all 0.3s;
    }
    
    .feature-card:hover .feature-icon {
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        color: white;
        transform: rotateY(180deg);
        box-shadow: 0 0 20px rgba(76, 201, 240, 0.5);
    }
    
    .feature-card h3 {
        margin-bottom: 20px;
        font-size: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .feature-card p {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    .analysis-section {
        margin: 100px 0;
        position: relative;
    }
    
    .analysis-container {
        display: flex;
        gap: 40px;
        align-items: center;
    }
    
    .analysis-visual {
        flex: 1;
        height: 500px;
        position: relative;
        transform-style: preserve-3d;
    }
    
    .analysis-content {
        flex: 1;
    }
    
    .analysis-content h2 {
        font-size: 2.2rem;
        margin-bottom: 30px;
        background: linear-gradient(to right, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .analysis-content p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.8;
        margin-bottom: 30px;
    }
    
    .analysis-stats {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 40px;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 10px;
        border-left: 3px solid var(--accent-color);
        transition: all 0.3s;
    }
    
    .stat-item:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stat-item h4 {
        color: var(--accent-color);
        margin-bottom: 10px;
        font-size: 1rem;
    }
    
    .stat-item p {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        color: white;
    }
    
    .resume-preview {
        margin: 100px 0;
    }
    
    .preview-container {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 40px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(76, 201, 240, 0.3);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .preview-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }
    
    .preview-header h2 {
        font-size: 2rem;
        background: linear-gradient(to right, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .preview-actions {
        display: flex;
        gap: 15px;
    }
    
    .preview-btn {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .preview-btn:hover {
        background: var(--accent-color);
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(76, 201, 240, 0.4);
    }
    
    .preview-content {
        display: flex;
        gap: 40px;
    }
    
    .preview-sidebar {
        width: 250px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 20px;
    }
    
    .preview-main {
        flex: 1;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 30px;
    }
    
    .preview-ai-suggestions {
        margin-top: 40px;
        background: rgba(76, 201, 240, 0.1);
        border-radius: 10px;
        padding: 20px;
        border-left: 3px solid var(--accent-color);
    }
    
    .preview-ai-suggestions h4 {
        color: var(--accent-color);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .suggestion-item {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .suggestion-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .suggestion-icon {
        color: var(--accent-color);
        font-size: 1.2rem;
        margin-top: 3px;
    }
    
    .suggestion-text {
        flex: 1;
        color: var(--text-secondary);
    }
    
    .suggestion-text strong {
        color: white;
        font-weight: 600;
    }
    
    .cta-section {
        margin: 100px 0;
        text-align: center;
    }
    
    .cta-card {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border-radius: 20px;
        padding: 60px;
        box-shadow: 0 15px 35px rgba(67, 97, 238, 0.4);
        position: relative;
        overflow: hidden;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .cta-card h2 {
        font-size: 2.5rem;
        margin-bottom: 20px;
        color: white;
    }
    
    .cta-card p {
        color: var(--text-secondary);
        font-size: 1.2rem;
        line-height: 1.8;
        margin-bottom: 30px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .cta-btn {
        background: white;
        color: #000 !important;
        border: none;
        padding: 15px 40px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
        display: inline-flex;
        align-items: center;
        z-index: 1;
        font-size: 1.1rem;
    }
    
    .cta-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: 0.5s;
        z-index: -1;
    }
    
    .cta-btn:hover::before {
        left: 100%;
    }
    
    .cta-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
    }
    
    .cta-btn i {
        margin-right: 10px;
        font-size: 20px;
    }
    
    .cta-btn, .cta-btn i {
        color: #000 !important;
    }
    
    footer {
        background: rgba(15, 15, 27, 0.9);
        padding: 80px 0 30px;
        border-top: 1px solid rgba(76, 201, 240, 0.2);
        backdrop-filter: blur(10px);
        margin-top: 100px;
        position: relative;
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 50px;
        margin-bottom: 50px;
    }
    
    .footer-column h3 {
        color: var(--accent-color);
        margin-bottom: 25px;
        font-size: 1.3rem;
        position: relative;
        padding-bottom: 10px;
    }
    
    .footer-column h3::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 3px;
        background: linear-gradient(to right, var(--accent-color), var(--primary-color));
        border-radius: 3px;
    }
    
    .footer-column ul {
        list-style: none;
    }
    
    .footer-column ul li {
        margin-bottom: 15px;
    }
    
    .footer-column ul li a {
        color: var(--text-secondary);
        text-decoration: none;
        transition: all 0.3s;
        display: flex;
        align-items: center;
    }
    
    .footer-column ul li a i {
        margin-right: 10px;
        font-size: 0.9rem;
    }
    
    .footer-column ul li a:hover {
        color: var(--accent-color);
        padding-left: 5px;
    }
    
    .social-links {
        display: flex;
        gap: 20px;
        margin-top: 25px;
    }
    
    .social-links a {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        transition: all 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .social-links a:hover {
        background: var(--accent-color);
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(76, 201, 240, 0.4);
    }
    
    .copyright {
        text-align: center;
        padding-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--text-secondary);
        font-size: 0.95rem;
    }
    
    .cyber-orb {
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(76, 201, 240, 0.1) 0%, transparent 70%);
        filter: blur(30px);
        animation: floatOrb 15s infinite ease-in-out;
        z-index: 3;
    }
    
    @keyframes floatOrb {
        0%, 100% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(50px, -30px) scale(1.1); }
        50% { transform: translate(0, -60px) scale(0.9); }
        75% { transform: translate(-50px, -30px) scale(1.05); }
    }
    
    /* 3D简历元素 */
    .resume-3d-element {
        width: 100%;
        height: 100%;
        position: relative;
    }
    
    /* 上传动画 */
    .upload-progress {
        width: 100%;
        height: 5px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        margin-top: 30px;
        overflow: hidden;
        display: none;
    }
    
    .upload-progress-bar {
        height: 100%;
        width: 0;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        border-radius: 5px;
        transition: width 0.3s;
        position: relative;
    }
    
    .upload-progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: progressShine 2s infinite;
    }
    
    @keyframes progressShine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .upload-success {
        display: none;
        margin-top: 30px;
        color: var(--success-color);
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .upload-success i {
        margin-right: 10px;
    }
    
    /* 响应式设计 */
    @media (max-width: 1200px) {
        .analysis-container {
            flex-direction: column;
        }
        
        .analysis-visual, .analysis-content {
            width: 100%;
        }
        
        .preview-content {
            flex-direction: column;
        }
        
        .preview-sidebar {
            width: 100%;
            margin-bottom: 30px;
        }
    }
    
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 3rem;
        }
        
        .header-content {
            flex-direction: column;
            gap: 20px;
        }
        
        .nav-links {
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .upload-card {
            padding: 40px 20px;
        }
        
        .feature-card {
            padding: 30px;
        }
        
        .section-title {
            font-size: 2rem;
        }
        
        .cta-card {
            padding: 40px 20px;
        }
        
        .cta-card h2 {
            font-size: 2rem;
        }
    }
    
    @media (max-width: 576px) {
        .main-title h1 {
            font-size: 2.2rem;
        }
        
        .main-title p {
            font-size: 1rem;
        }
        
        .upload-icon {
            width: 80px;
            height: 80px;
            font-size: 35px;
        }
        
        .upload-card h2 {
            font-size: 1.5rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .section-title i {
            font-size: 1.5rem;
            margin-right: 15px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .analysis-stats {
            grid-template-columns: 1fr;
        }
        
        .preview-actions {
            flex-direction: column;
            gap: 10px;
        }
        
        .preview-btn {
            width: 100%;
            justify-content: center;
        }
    }

    /* 强制所有文本使用亮色 */
    :deep(p),
    :deep(h1),
    :deep(h2),
    :deep(h3),
    :deep(h4),
    :deep(h5),
    :deep(h6),
    :deep(span),
    :deep(div),
    :deep(li),
    :deep(a) {
        color: var(--text-primary) !important;
    }

    /* 特定元素的颜色覆盖 */
    .preview-content {
        :deep(p), :deep(h3), :deep(h4), :deep(span), :deep(strong) {
            color: var(--text-primary) !important;
        }
    }

    .preview-sidebar {
        :deep(p), :deep(h3), :deep(h4), :deep(span), :deep(strong) {
            color: var(--text-primary) !important;
        }
    }

    .main-title {
        :deep(p) {
            color: var(--text-primary) !important;
        }
    }

    .upload-card {
        :deep(p) {
            color: var(--text-primary) !important;
        }
    }

    .feature-card {
        :deep(p) {
            color: var(--text-primary) !important;
        }
    }

    .analysis-content {
        :deep(p) {
            color: var(--text-primary) !important;
        }
    }

    .cta-card {
        :deep(p) {
            color: var(--text-primary) !important;
        }
    }

    .footer-column {
        :deep(a) {
            color: var(--text-primary) !important;
        }
    }

    /* 保持一些特殊样式 */
    .logo {
        background: linear-gradient(to right, var(--accent-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .section-title {
        background: linear-gradient(to right, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .main-title h1 {
        background: linear-gradient(to right, var(--text-primary), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 确保所有文本在深色背景上可见 */
    .cyber-gradient * {
        color: var(--text-primary) !important;
    }

    /* 特殊强调文本使用渐变色 */
    .emphasis-gradient {
        background: linear-gradient(120deg, var(--accent-color), var(--primary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }

    /* 覆盖全局样式 */
    :deep(.cta-btn),
    :deep(.cta-btn i) {
        color: #000 !important;
    }

    .cta-card :deep(.cta-btn),
    .cta-card :deep(.cta-btn i) {
        color: #000 !important;
    }

    /* 确保按钮文字颜色不被其他规则覆盖 */
    :deep(.cta-btn) {
        &, & * {
            color: #000 !important;
        }
    }
</style>