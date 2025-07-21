<template>
  <!-- 复制面试结果2.html 的 <body> 内容到这里，去除 <script> 标签中的原生 JS，后续可用 Vue 实现交互 -->
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
                <span>未来科技招聘AI</span>
            </div>
            <button class="download-btn">
                <i class="fas fa-download"></i> 下载完整报告
            </button>
        </div>
    </header>
    
    <main class="container">
        <div class="report-header">
            <h1>3D动态面试分析报告</h1>
            <p>基于多模态AI深度分析的全面评估，采用先进算法生成的3D可视化报告，全方位展示您的面试表现</p>
            
            <div class="candidate-info">
                <div class="info-item">
                    <h3>候选人</h3>
                    <p>张小明</p>
                </div>
                
                <div class="info-item">
                    <h3>应聘职位</h3>
                    <p>高级前端开发工程师</p>
                </div>
                
                <div class="info-item">
                    <h3>面试日期</h3>
                    <p>2023年11月20日</p>
                </div>
                
                <div class="info-item">
                    <h3>综合评分</h3>
                    <p>86.5/100</p>
                    <div class="overall-score">优秀表现</div>
                </div>
            </div>
        </div>
        
        <section class="section">
            <h2 class="section-title"><i class="fas fa-video"></i> 全息面试录像</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>候选人视频 <span class="score">流畅度: 92%</span></h3>
                    <div class="video-container">
                        <video id="candidate-video" src="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4" controls></video>
                        <div class="video-controls">
                            <button title="播放/暂停"><i class="fas fa-play"></i></button>
                            <button title="全屏"><i class="fas fa-expand"></i></button>
                            <button title="3D模式"><i class="fas fa-cube"></i></button>
                            <button title="分析模式"><i class="fas fa-chart-line"></i></button>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>面试官视频 <span class="score">互动质量: 88%</span></h3>
                    <div class="video-container">
                        <video id="interviewer-video" src="https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4" controls></video>
                        <div class="video-controls">
                            <button title="播放/暂停"><i class="fas fa-play"></i></button>
                            <button title="全屏"><i class="fas fa-expand"></i></button>
                            <button title="3D模式"><i class="fas fa-cube"></i></button>
                            <button title="分析模式"><i class="fas fa-chart-line"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title"><i class="fas fa-chart-network"></i> 3D能力图谱</h2>
            <div class="grid-3">
                <div class="card">
                    <h3>技术能力 <span class="score">91/100</span></h3>
                    <div class="progress-bars">
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>JavaScript深度</span>
                                <span>94%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 94%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>React框架</span>
                                <span>89%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 89%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>算法与数据结构</span>
                                <span>87%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 87%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>系统设计</span>
                                <span>82%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 82%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>沟通表达 <span class="score">85/100</span></h3>
                    <div class="progress-bars">
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>语言清晰度</span>
                                <span>92%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 92%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>逻辑性</span>
                                <span>88%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 88%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>回答结构化</span>
                                <span>83%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 83%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>倾听能力</span>
                                <span>77%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 77%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>综合素质 <span class="score">83/100</span></h3>
                    <div class="progress-bars">
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>问题解决能力</span>
                                <span>89%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 89%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>团队协作</span>
                                <span>85%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 85%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>学习能力</span>
                                <span>82%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 82%"></div>
                            </div>
                        </div>
                        
                        <div class="progress-item">
                            <div class="progress-label">
                                <span>抗压能力</span>
                                <span>76%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: 76%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title"><i class="fas fa-brain"></i> 动态情绪图谱</h2>
            <div class="grid-2">
                <div class="card">
                    <h3>3D情绪波动曲线 <span class="score">稳定性: 88%</span></h3>
                    <div ref="emotion3DChartRef" class="chart-container"></div>
                </div>
                
                <div class="card">
                    <h3>情绪热点分布 <span class="score">积极情绪: 82%</span></h3>
                    <div ref="emotionRadar3DRef" class="chart-container" id="emotion-radar-3d"></div>
                </div>
            </div>
        </section>
        
 <section class="section">
        <h2 class="section-title"><i class="fas fa-atom"></i> 3D岗位匹配分析</h2>
        <div class="grid-2">
            <div class="card">
                <h3>能力匹配球体 <span class="score">匹配度: 89%</span></h3>
                <div ref="sphereContainerRef" class="chart-container" id="skill-sphere-3d" style="height: 400px;">
                    <div id="sphere-container" style="width: 100%; height: 100%; position: relative;">
                        <div id="sphere-info" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 10; color: white; pointer-events: none;">
                            <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">技能匹配度</div>
                            <div style="font-size: 48px; font-weight: bold; color: #4cc9f0;">89%</div>
                            <div style="font-size: 14px; opacity: 0.8;">高级前端开发工程师</div>
                        </div>
                    </div>
                    <div id="skill-legend" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 20px;">
                        <div class="legend-item">
                            <div class="legend-color" style="width: 15px; height: 15px; background: #4cc9f0; border-radius: 50%; margin-right: 8px;"></div>
                            <span>JavaScript (94%)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="width: 15px; height: 15px; background: #4361ee; border-radius: 50%; margin-right: 8px;"></div>
                            <span>React (89%)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="width: 15px; height: 15px; background: #3f37c9; border-radius: 50%; margin-right: 8px;"></div>
                            <span>算法 (87%)</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="width: 15px; height: 15px; background: #1a1a2e; border-radius: 50%; margin-right: 8px;"></div>
                            <span>系统设计 (82%)</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>岗位需求对比 <span class="score">核心匹配: 91%</span></h3>
                <div ref="match3DChartRef" class="chart-container" id="match-3d-chart"></div>
            </div>
        </div>
    </section>

        
        <section class="section">
            <h2 class="section-title"><i class="fas fa-comment-dots"></i> AI深度反馈</h2>
            <div class="card">
                <h3>面试官综合评价</h3>
                <div class="feedback-item">
                    <div class="feedback-category"><i class="fas fa-code"></i> 技术能力评价</div>
                    <div class="feedback-content">
                        候选人在JavaScript和React方面表现出色，展示了深厚的理论基础和丰富的实践经验。系统设计能力良好，能够清晰地阐述架构思路，但在高并发场景下的优化方案可以进一步深入。
                    </div>
                </div>
                
                <div class="feedback-item">
                    <div class="feedback-category"><i class="fas fa-comments"></i> 沟通表达评价</div>
                    <div class="feedback-content">
                        语言表达清晰流畅，能够有条理地组织回答。在解释复杂概念时表现优秀，但偶尔会急于回答问题，建议在回答前多思考几秒钟以确保回答的完整性。
                    </div>
                </div>
                
                <div class="feedback-item">
                    <div class="feedback-category"><i class="fas fa-star"></i> 综合素质评价</div>
                    <div class="feedback-content">
                        展现了优秀的问题解决能力和学习能力。团队协作意识强，能够很好地理解面试官的问题意图。在压力测试环节表现稳定，但可以更主动地展示自己的优势。
                    </div>
                </div>
            </div>
            
            <div class="grid-2" style="margin-top: 30px;">
                <div class="card">
                    <h3>核心优势</h3>
                    <div class="strengths-weaknesses">
                        <div class="strengths">
                            <h4><i class="fas fa-bolt"></i> AI识别优势</h4>
                            <div class="sw-item">
                                <i class="fas fa-star strength-icon"></i>
                                <p>扎实的JavaScript基础，对ES6+特性掌握全面</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-star strength-icon"></i>
                                <p>React框架使用熟练，对虚拟DOM原理理解深刻</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-star strength-icon"></i>
                                <p>算法思维优秀，能够快速找到问题解决方案</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-star strength-icon"></i>
                                <p>沟通表达清晰，能够有效传递技术观点</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h3>AI改进建议</h3>
                    <div class="strengths-weaknesses">
                        <div class="weaknesses">
                            <h4><i class="fas fa-lightbulb-on"></i> 智能提升方案</h4>
                            <div class="sw-item">
                                <i class="fas fa-rocket weakness-icon"></i>
                                <p>加强大型前端项目架构设计经验，特别是微前端领域</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-rocket weakness-icon"></i>
                                <p>学习更多性能优化技巧，特别是首屏加载优化</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-rocket weakness-icon"></i>
                                <p>提高系统设计环节的白板绘图能力</p>
                            </div>
                            <div class="sw-item">
                                <i class="fas fa-rocket weakness-icon"></i>
                                <p>准备更多项目中的具体案例来佐证能力</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="section">
            <h2 class="section-title"><i class="fas fa-clock"></i> 关键时间点全息分析</h2>
            <div class="card">
                <h3>面试关键事件时间轴</h3>
                <div class="timeline">
                    <div class="timeline-item">
                        <div class="timeline-time"><i class="fas fa-play"></i> 00:02:30 - 技术问题回答</div>
                        <div class="timeline-content">
                            在回答关于React性能优化的问题时表现优异，详细列举了多种优化手段并解释了原理，情绪稳定且自信。
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="timeline-time"><i class="fas fa-code"></i> 00:12:15 - 算法白板编程</div>
                        <div class="timeline-content">
                            快速准确地完成了二叉树遍历问题，代码整洁且考虑了边界条件，展示了扎实的算法基础。
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="timeline-time"><i class="fas fa-project-diagram"></i> 00:25:40 - 系统设计环节</div>
                        <div class="timeline-content">
                            设计一个高并发票务系统时思路清晰，但在数据库分片策略上稍有迟疑，经提示后能快速调整方案。
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="timeline-time"><i class="fas fa-users"></i> 00:38:20 - 行为问题回答</div>
                        <div class="timeline-content">
                            讲述团队冲突解决案例时真实可信，但语速稍快，情绪波动略大，反映了对这类问题的重视。
                        </div>
                    </div>
                    
                    <div class="timeline-item">
                        <div class="timeline-time"><i class="fas fa-question"></i> 00:45:00 - 反问环节</div>
                        <div class="timeline-content">
                            提出的问题展现了对公司技术的深入了解和职业发展的清晰规划，给面试官留下深刻印象。
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section class="next-steps">
            <h2>AI职业发展路径</h2>
            <p>基于您的面试表现，AI为您量身定制的发展建议</p>
            
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-icon">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h3>学习路径</h3>
                    <p>推荐阅读《前端架构设计》和《高性能JavaScript》，完成3个中型项目实践，掌握微前端架构</p>
                </div>
                
                <div class="step-card">
                    <div class="step-icon">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <h3>项目实践</h3>
                    <p>建议主导一个微前端架构项目，积累复杂项目经验，使用React+TypeScript+Webpack5技术栈</p>
                </div>
                
                <div class="step-card">
                    <div class="step-icon">
                        <i class="fas fa-briefcase"></i>
                    </div>
                    <h3>职业发展</h3>
                    <p>6个月内可申请技术主管岗位，1-2年可向架构师方向发展，年薪增长潜力40-60%</p>
                </div>
                
                <div class="step-card">
                    <div class="step-icon">
                        <i class="fas fa-handshake"></i>
                    </div>
                    <h3>面试结果</h3>
                    <p>已进入最终候选名单，HR将在3个工作日内联系您，通过概率87%</p>
                </div>
            </div>
        </section>
    </main>
    
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h3>关于AI分析</h3>
                    <ul>
                        <li><a href="#"><i class="fas fa-robot"></i> 分析算法说明</a></li>
                        <li><a href="#"><i class="fas fa-chart-line"></i> 数据采集方式</a></li>
                        <li><a href="#"><i class="fas fa-shield-alt"></i> 隐私保护政策</a></li>
                        <li><a href="#"><i class="fas fa-question-circle"></i> 常见问题</a></li>
                    </ul>
                </div>
                
                <div class="footer-column">
                    <h3>候选人服务</h3>
                    <ul>
                        <li><a href="#"><i class="fas fa-user-tie"></i> 职业咨询</a></li>
                        <li><a href="#"><i class="fas fa-book-open"></i> 学习资源</a></li>
                        <li><a href="#"><i class="fas fa-project-diagram"></i> 项目实践</a></li>
                        <li><a href="#"><i class="fas fa-file-alt"></i> 简历优化</a></li>
                    </ul>
                </div>
                
                <div class="footer-column">
                    <h3>企业服务</h3>
                    <ul>
                        <li><a href="#"><i class="fas fa-bullhorn"></i> 发布职位</a></li>
                        <li><a href="#"><i class="fas fa-search"></i> 人才搜索</a></li>
                        <li><a href="#"><i class="fas fa-chart-pie"></i> 分析报告</a></li>
                        <li><a href="#"><i class="fas fa-cogs"></i> 企业解决方案</a></li>
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
                &copy; 2023 未来科技招聘AI. 保留所有权利. | 由AI生成的分析报告
            </div>
        </div>
    </footer>
    

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import * as THREE from 'three'
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const emotion3DChartRef = ref<HTMLDivElement | null>(null)
const emotionRadar3DRef = ref<HTMLDivElement | null>(null)
const match3DChartRef = ref<HTMLDivElement | null>(null)
const sphereContainerRef = ref<HTMLDivElement | null>(null)

onMounted(() => {
  if (emotion3DChartRef.value) {
    const chart = echarts.init(emotion3DChartRef.value)
    // chart.setOption(...)
  }

  // 2. Three.js 3D 球体
  const skillSphere3D = document.getElementById('sphere-container')
  if (skillSphere3D) {
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(75, skillSphere3D.clientWidth / skillSphere3D.clientHeight, 0.1, 1000)
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(skillSphere3D.clientWidth, skillSphere3D.clientHeight)
    skillSphere3D.appendChild(renderer.domElement)
    // ...其余 three.js 逻辑同原始代码...
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
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', 'Microsoft YaHei', sans-serif;
            color: var(--text-primary);
        }
        
        body {
            background-color: var(--dark-color);
            line-height: 1.6;
            overflow-x: hidden;
            perspective: 1000px;
        }
        
        .cyber-gradient {
            background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f1b 70%);
            position: relative;
            overflow: hidden;
        }
        
        .cyber-gradient::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(72, 202, 228, 0.03),
                rgba(67, 97, 238, 0.03),
                transparent
            );
            transform-origin: center;
            animation: rotate 10s linear infinite;
            pointer-events: none;
        }
        
        @keyframes rotate {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
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
            z-index: 0;
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
            z-index: 0;
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
            z-index: 10;
        }
        
        header {
            padding: 30px 0;
            position: relative;
            z-index: 100;
            backdrop-filter: blur(10px);
            background: rgba(15, 15, 27, 0.7);
            border-bottom: 1px solid rgba(76, 201, 240, 0.2);
            margin-bottom: 30px;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(to right, var(--accent-color), var(--primary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            text-shadow: 0 0 10px rgba(76, 201, 240, 0.5);
            letter-spacing: 1px;
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
        
        .download-btn {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 30px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            z-index: 1;
        }
        
        .download-btn::before {
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
        
        .download-btn:hover::before {
            left: 100%;
        }
        
        .download-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(67, 97, 238, 0.6);
        }
        
        .download-btn i {
            margin-right: 8px;
            font-size: 18px;
        }
        
        .report-header {
            text-align: center;
            margin: 60px 0;
            position: relative;
        }
        
        .report-header h1 {
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
        
        .report-header p {
            color: var(--text-secondary);
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.8;
        }
        
        .candidate-info {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .info-item {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 20px 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(76, 201, 240, 0.3);
            min-width: 220px;
            text-align: center;
            transform-style: preserve-3d;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .info-item::before {
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
        
        .info-item:hover {
            transform: translateY(-15px) rotateX(10deg) rotateY(5deg);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            border-color: var(--accent-color);
        }
        
        .info-item:hover::before {
            left: 100%;
        }
        
        .info-item h3 {
            color: var(--accent-color);
            font-size: 1rem;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .info-item p {
            color: var(--text-primary);
            font-size: 1.2rem;
            font-weight: 500;
        }
        
        .overall-score {
            color: var(--text-primary);
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 5px 20px;
            border-radius: 30px;
            font-weight: 600;
            display: inline-block;
            margin-top: 15px;
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
        }
        
        .section {
            margin: 80px 0;
            position: relative;
        }
        
        .section-title {
            font-size: 2.5rem;
            margin-bottom: 40px;
            background: linear-gradient(120deg, #48CAE4, #4361EE, #48CAE4);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 3s linear infinite;
            display: flex;
            align-items: center;
            position: relative;
            padding-left: 60px;
        }
        
        .section-title::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 40px;
            height: 4px;
            background: linear-gradient(to right, var(--accent-color), var(--primary-color));
            border-radius: 2px;
        }
        
        .section-title i {
            margin-right: 20px;
            font-size: 2rem;
            animation: float 3s ease-in-out infinite;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }
        
        .card {
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
        
        .card::before {
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
        
        .card:hover {
            transform: translateY(-15px) rotateX(5deg) rotateY(5deg);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            border-color: var(--accent-color);
        }
        
        .card:hover::before {
            left: 100%;
        }
        
        .card h3 {
            color: var(--text-primary);
            margin-bottom: 25px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .card h3 .score {
            color: var(--text-primary);
            background: rgba(76, 201, 240, 0.2);
            padding: 5px 15px;
            border-radius: 30px;
            font-size: 1rem;
            font-weight: 600;
            border: 1px solid rgba(76, 201, 240, 0.5);
        }
        
        .video-container {
            position: relative;
            border-radius: 15px;
            overflow: hidden;
            aspect-ratio: 16/9;
            background: #000;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            transform-style: preserve-3d;
        }
        
        .video-container::before {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 15px;
            padding: 2px;
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            z-index: 1;
        }
        
        .video-container video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .video-controls {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
            padding: 20px;
            display: flex;
            justify-content: center;
            gap: 20px;
            z-index: 2;
        }
        
        .video-controls button {
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
        }
        
        .video-controls button:hover {
            background: var(--accent-color);
            transform: scale(1.1);
            box-shadow: 0 0 15px rgba(76, 201, 240, 0.5);
        }
        
        .chart-container {
            height: 350px;
            position: relative;
            transform-style: preserve-3d;
            transition: all 0.5s;
        }
        
        .chart-container:hover {
            transform: translateY(-10px);
        }
        
        .progress-bars {
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        
        .progress-item {
            margin-bottom: 20px;
        }
        
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        
        .progress-label span {
            color: var(--text-secondary);
        }
        
        .progress-label span:first-child {
            color: var(--accent-color);
        }
        
        .progress-bar {
            height: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
        }
        
        .progress-fill {
            height: 100%;
            border-radius: 5px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            transition: width 1s ease-out;
            position: relative;
            overflow: hidden;
        }
        
        .progress-fill::after {
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
        
        .feedback-item {
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
        }
        
        .feedback-item:last-child {
            border-bottom: none;
        }
        
        .feedback-category {
            color: var(--accent-color);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .feedback-category i {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        .feedback-content {
            color: var(--text-secondary);
            font-size: 1.05rem;
            line-height: 1.8;
            padding-left: 30px;
        }
        
        .strengths-weaknesses {
            display: flex;
            gap: 30px;
        }
        
        .strengths, .weaknesses {
            flex: 1;
        }
        
        .strengths h4, .weaknesses h4 {
            color: var(--text-primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            font-size: 1.3rem;
        }
        
        .strengths h4 i, .weaknesses h4 i {
            margin-right: 15px;
            font-size: 1.5rem;
        }
        
        .sw-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .sw-item:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.1);
        }
        
        .sw-item i {
            margin-right: 15px;
            margin-top: 3px;
            font-size: 1.2rem;
        }
        
        .sw-item .strength-icon {
            color: var(--success-color);
        }
        
        .sw-item .weakness-icon {
            color: var(--warning-color);
        }
        
        .sw-item p {
            color: var(--text-secondary);
            flex: 1;
            font-size: 1rem;
        }
        
        .timeline {
            position: relative;
            padding-left: 40px;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to bottom, var(--primary-color), var(--accent-color));
            border-radius: 3px;
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: 30px;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -40px;
            top: 5px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--accent-color);
            box-shadow: 0 0 0 5px rgba(76, 201, 240, 0.3);
            z-index: 1;
            animation: pulse 2s ease infinite;
        }
        
        .timeline-time {
            color: var(--accent-color);
            font-size: 0.9rem;
            margin-bottom: 10px;
            font-weight: 600;
            display: flex;
            align-items: center;
        }
        
        .timeline-time i {
            margin-right: 8px;
        }
        
        .timeline-content {
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 10px;
            font-size: 1rem;
            line-height: 1.8;
        }
        
        .timeline-content:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.1);
        }
        
        .next-steps {
            margin-top: 80px;
            text-align: center;
            position: relative;
        }
        
        .next-steps h2 {
            color: var(--text-primary) !important;
            font-size: 2.5rem;
            margin-bottom: 40px;
        }
        
        .next-steps p {
            text-align: center;
            color: var(--text-primary) !important;
            margin-bottom: 40px;
        }
        
        .steps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 40px;
            margin-top: 50px;
        }
        
        .step-card {
            background: var(--card-bg);
            border-radius: 20px;
            padding: 40px 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(76, 201, 240, 0.3);
            transform-style: preserve-3d;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .step-card::before {
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
        
        .step-card:hover {
            transform: translateY(-15px) rotateX(5deg) rotateY(5deg);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
            border-color: var(--accent-color);
        }
        
        .step-card:hover::before {
            left: 100%;
        }
        
        .step-icon {
            width: 80px;
            height: 80px;
            background: rgba(76, 201, 240, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 25px;
            font-size: 36px;
            color: var(--accent-color);
            border: 2px solid rgba(76, 201, 240, 0.3);
            transition: all 0.3s;
        }
        
        .step-card:hover .step-icon {
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
            color: white;
            transform: rotateY(180deg);
            box-shadow: 0 0 20px rgba(76, 201, 240, 0.5);
        }
        
        .step-card h3 {
            margin-bottom: 20px;
            font-size: 1.4rem;
            position: relative;
            z-index: 1;
        }
        
        .step-card p {
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.8;
            position: relative;
            z-index: 1;
        }
        
        footer {
            background: rgba(15, 15, 27, 0.9);
            padding: 60px 0 30px;
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
            color: var(--text-primary);
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
            color: var(--text-tertiary);
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
            color: var(--text-tertiary);
            text-align: center;
            padding-top: 40px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
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
            z-index: 0;
        }
        
        @keyframes floatOrb {
            0%, 100% { transform: translate(0, 0) scale(1); }
            25% { transform: translate(50px, -30px) scale(1.1); }
            50% { transform: translate(0, -60px) scale(0.9); }
            75% { transform: translate(-50px, -30px) scale(1.05); }
        }
        
        @media (max-width: 1200px) {
            .grid-2, .grid-3 {
                grid-template-columns: 1fr;
            }
            
            .report-header h1 {
                font-size: 3rem;
            }
            
            .section-title {
                font-size: 2rem;
            }
        }
        
        @media (max-width: 768px) {
            .report-header h1 {
                font-size: 2.2rem;
            }
            
            .candidate-info {
                flex-direction: column;
                gap: 20px;
            }
            
            .info-item {
                width: 100%;
            }
            
            .strengths-weaknesses {
                flex-direction: column;
            }
            
            .section-title {
                font-size: 1.8rem;
                padding-left: 40px;
            }
            
            .section-title i {
                font-size: 1.5rem;
                margin-right: 15px;
            }
        }
        
        @media (max-width: 576px) {
            .report-header h1 {
                font-size: 1.8rem;
            }
            
            .report-header p {
                font-size: 1rem;
            }
            
            .section-title {
                font-size: 1.5rem;
                padding-left: 30px;
            }
            
            .section-title::before {
                width: 25px;
            }
            
            .card {
                padding: 25px;
            }
            
            .step-card {
                padding: 30px 20px;
            }
        }

        .legend-item {
            display: flex;
            align-items: center;
            color: var(--text-secondary);
        }

        .legend-item span {
            color: var(--text-secondary);
        }

        .sw-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
            color: var(--text-secondary);
        }

        .sw-item i {
            margin-right: 10px;
            font-size: 1.2rem;
        }

        .strength-icon {
            color: var(--accent-color);
        }

        .weakness-icon {
            color: var(--warning-color);
        }

        .sw-item p {
            color: var(--text-secondary);
            margin: 0;
            line-height: 1.4;
        }

        .strengths h4, .weaknesses h4 {
            color: var(--text-primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }

        .strengths h4 i, .weaknesses h4 i {
            margin-right: 10px;
            color: var(--accent-color);
        }

        .feedback-category {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--accent-color);
            display: flex;
            align-items: center;
        }

        .feedback-category i {
            margin-right: 10px;
            color: var(--accent-color);
        }

        .feedback-content {
            color: var(--text-secondary);
            line-height: 1.8;
            margin-bottom: 25px;
            padding-left: 25px;
        }

        .timeline-time {
            font-weight: 600;
            color: var(--accent-color);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
        }

        .timeline-time i {
            margin-right: 8px;
            color: var(--accent-color);
        }

        .timeline-content {
            color: var(--text-secondary);
            line-height: 1.6;
            padding-left: 25px;
        }

        .next-steps h2 {
            text-align: center;
            margin-bottom: 10px;
            color: var(--text-primary);
        }

        .next-steps p {
            text-align: center;
            color: var(--text-primary) !important;
            margin-bottom: 40px;
        }

        .step-card {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .step-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent-color);
        }

        .step-icon {
            width: 60px;
            height: 60px;
            margin: 0 auto 20px;
            background: rgba(76, 201, 240, 0.1);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .step-icon i {
            font-size: 24px;
            color: var(--accent-color);
        }

        .step-card h3 {
            color: var(--text-primary);
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .step-card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* 确保所有文本在深色背景上可见 */
        .cyber-gradient * {
            color: var(--text-primary);
        }

        /* 特殊强调文本使用渐变色 */
        .emphasis-gradient {
            background: linear-gradient(120deg, var(--accent-color), var(--primary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 3s linear infinite;
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
        :deep(div) {
            color: var(--text-primary) !important;
        }
</style> 
 