<template>
  <div class="job-page">
    <!-- 标题 -->
    <h1 class="page-title">岗位信息总览</h1>

    <!-- 筛选区域 -->
    <div class="filters">
      <input v-model="searchKeyword" placeholder="搜索岗位/类别" class="filter-input" />
      <select v-model="city" class="filter-input">
        <option value="">全部城市</option>
        <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
      </select>
      <div class="salary-filter">
        <input type="number" v-model.number="salaryMin" placeholder="最低薪资" class="salary-input" />
        <span>-</span>
        <input type="number" v-model.number="salaryMax" placeholder="最高薪资" class="salary-input" />
      </div>
      <button class="filter-btn" @click="applyFilters">筛选</button>
      <button class="filter-btn reset" @click="resetFilters">重置</button>
    </div>

    <!-- 新增按钮 -->
    <div class="add-btn-wrapper">
      <button class="add-btn" @click="openForm()">+ 新增岗位</button>
    </div>

    <!-- 加载/空状态 -->
    <div v-if="loading" class="loading-state">正在加载数据...</div>
    <div v-else-if="filteredJobs.length === 0" class="empty-state">暂无岗位</div>

    <!-- 岗位表格 -->
    <table class="job-table" v-else>
      <thead>
        <tr>
          <th>岗位</th>
          <th>薪资</th>
          <th>城市</th>
          <th>描述</th>
          <th>要求</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="job in paginatedJobs" :key="job.id">
          <td>{{ job.job_title }}</td>
          <td class="salary">{{ job.salary_min }}-{{ job.salary_max }}元/{{ job.salary_type || '月' }}</td>
          <td>{{ job.location }}</td>
          <td>
            <span>{{ expandedRows[job.id] ? job.description : truncate(job.description, 10) }}</span>
            <a v-if="job.description && job.description.length > 40" @click="toggleExpand(job.id)">
              {{ expandedRows[job.id] ? '收起' : '查看更多' }}
            </a>
          </td>
          <td>
            <span>{{ expandedRowsReq[job.id] ? job.requirements : truncate(job.requirements, 10) }}</span>
            <a v-if="job.requirements && job.requirements.length > 40" @click="toggleExpandReq(job.id)">
              {{ expandedRowsReq[job.id] ? '收起' : '查看更多' }}
            </a>
          </td>
          <td class="actions">
            <button @click="viewJob(job)">查看</button>
            <button @click="openForm(job)">修改</button>
            <button class="delete-btn" @click="deleteJob(job.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页 -->
    <div class="pagination" v-if="filteredJobs.length > pageSize">
      <button :disabled="currentPage === 1" @click="prevPage">上一页</button>
      <span>第 {{ currentPage }} / {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="nextPage">下一页</button>
    </div>

    <!-- 查看详情模态框 -->
    <div class="modal-overlay" v-if="showModal">
      <div class="modal-content detail-modal">
        <div class="modal-header">
          <h2>{{ currentJob.job_title }}</h2>
          <span class="modal-close" @click="showModal = false">&times;</span>
        </div>
        <div class="modal-body">
          <div class="info-item">
            <i class="icon">💰</i>
            <span><strong>薪资：</strong>{{ currentJob.salary_min }} - {{ currentJob.salary_max }}元/{{ currentJob.salary_type || '月' }}</span>
          </div>
          <div class="info-item">
            <i class="icon">📍</i>
            <span><strong>地点：</strong>{{ currentJob.location }} {{ currentJob.address_detail || '' }}</span>
          </div>
          <div class="info-item">
            <i class="icon">🏷️</i>
            <span><strong>岗位类别：</strong>{{ currentJob.job_category }}</span>
          </div>
          <div class="info-item">
            <i class="icon">💼</i>
            <span><strong>工作性质：</strong>{{ currentJob.job_nature || '全职' }}</span>
          </div>
          <div class="info-item">
            <i class="icon">🎓</i>
            <span><strong>学历要求：</strong>{{ currentJob.education_req || '不限' }}</span>
          </div>
          <hr />
          <div class="section">
            <h3>岗位描述</h3>
            <p>{{ currentJob.description || '无' }}</p>
          </div>
          <div class="section">
            <h3>岗位要求</h3>
            <p>{{ currentJob.requirements || '无' }}</p>
          </div>
          <div class="section">
            <h3>福利待遇</h3>
            <p>{{ currentJob.benefits || '无' }}</p>
          </div>
          <hr />
          <div class="info-item">
            <i class="icon">📧</i>
            <span><strong>联系邮箱：</strong>{{ currentJob.contact_email || '无' }}</span>
          </div>
          <div class="info-item">
            <i class="icon">📞</i>
            <span><strong>联系电话：</strong>{{ currentJob.contact_phone || '无' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/修改岗位模态框 -->
    <div class="modal-overlay" v-if="showForm">
      <div class="modal-content form-modal enhanced-form">
        <div class="modal-header">
          <h2>{{ form.id ? '修改岗位' : '新增岗位' }}</h2>
          <span class="modal-close" @click="closeForm">&times;</span>
        </div>

        <form class="job-form" @submit.prevent="saveJob">
          <!-- 岗位名称 -->
          <div class="form-group full">
            <label>岗位名称</label>
            <input v-model="form.job_title" required placeholder="请输入岗位名称" />
          </div>

          <!-- 岗位类别 -->
          <div class="form-group full">
            <label>岗位类别</label>
            <select v-model="form.job_category" @change="checkCustomCategory">
              <option disabled value="">请选择类别</option>
              <option v-for="c in jobCategories" :key="c" :value="c">{{ c }}</option>
              <option value="_custom">自定义</option>
            </select>
            <input v-if="customCategory" v-model="form.job_category" placeholder="输入自定义类别" />
          </div>

          <!-- 薪资 -->
          <div class="form-group-row">
            <div>
              <label>最低薪资</label>
              <input type="number" v-model.number="form.salary_min" />
            </div>
            <div>
              <label>最高薪资</label>
              <input type="number" v-model.number="form.salary_max" />
            </div>
            <div>
              <label>薪资单位</label>
              <select v-model="form.salary_type" @change="checkCustomSalaryType">
                <option disabled value="">单位</option>
                <option value="月">月薪</option>
                <option value="年">年薪</option>
                <option value="_custom">自定义</option>
              </select>
              <input v-if="customSalaryType" v-model="form.salary_type" placeholder="输入单位" />
            </div>
          </div>

          <!-- 城市、性质、经验 -->
          <div class="form-group-row">
            <div>
              <label>城市</label>
              <select v-model="form.location" @change="checkCustomCity">
                <option disabled value="">请选择城市</option>
                <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
                <option value="_custom">自定义</option>
              </select>
              <input v-if="customCity" v-model="form.location" placeholder="输入自定义城市" />
            </div>
            <div>
              <label>工作性质</label>
              <select v-model="form.job_nature" @change="checkCustomNature">
                <option disabled value="">请选择性质</option>
                <option value="全职">全职</option>
                <option value="兼职">兼职</option>
                <option value="_custom">自定义</option>
              </select>
              <input v-if="customNature" v-model="form.job_nature" placeholder="输入自定义性质" />
            </div>
            <div>
              <label>经验要求</label>
              <select v-model="form.experience_req" @change="checkCustomExperience">
                <option disabled value="">请选择</option>
                <option value="不限">不限</option>
                <option value="3年以上">3年以上</option>
                <option value="5年以上">5年以上</option>
                <option value="_custom">自定义</option>
              </select>
              <input v-if="customExperience" v-model="form.experience_req" placeholder="输入自定义经验" />
            </div>
          </div>

          <!-- 学历 + 联系 -->
          <div class="form-group-row">
            <div>
              <label>学历要求</label>
              <select v-model="form.education_req" @change="checkCustomEducation">
                <option disabled value="">请选择学历</option>
                <option value="中专">中专</option>
                <option value="大专">大专</option>
                <option value="本科">本科</option>
                <option value="研究生">研究生</option>
                <option value="博士">博士</option>
                <option value="_custom">自定义</option>
              </select>
              <input v-if="customEducation" v-model="form.education_req" placeholder="输入自定义学历" />
            </div>
            <div>
              <label>联系邮箱</label>
              <input v-model="form.contact_email" placeholder="HR邮箱" />
            </div>
            <div>
              <label>联系电话</label>
              <input v-model="form.contact_phone" placeholder="联系电话" />
            </div>
          </div>

          <!-- 描述信息 -->
          <div class="form-group full">
            <label>岗位描述</label>
            <textarea v-model="form.description"></textarea>
          </div>
          <div class="form-group full">
            <label>岗位要求</label>
            <textarea v-model="form.requirements"></textarea>
          </div>
          <div class="form-group full">
            <label>福利待遇</label>
            <textarea v-model="form.benefits"></textarea>
          </div>

          <!-- 按钮 -->
          <div class="form-actions fancy-buttons">
            <button type="submit" class="btn-save">保存</button>
            <button type="button" class="btn-cancel" @click="closeForm">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'JobFullList',
  data() {
    return {
      jobs: [],
      loading: false,
      searchKeyword: '',
      city: '',
      salaryMin: '',
      salaryMax: '',
      currentPage: 1,
      pageSize: 7,
      expandedRows: {},
      expandedRowsReq: {},
      showModal: false,
      currentJob: {},
      showForm: false,
      form: {},
      customCategory: false,
      customSalaryType: false,
      customCity: false,
      customNature: false,
      customExperience: false,
      customEducation: false,
      jobCategories: ['技术', '运营', '市场', '销售', '产品', '人事', '设计', '客服'],
      cities: [
        '北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '南京', '武汉', '西安',
        '苏州', '天津', '郑州', '长沙', '合肥', '青岛', '宁波', '东莞', '佛山', '无锡',
        '厦门', '福州', '济南', '大连', '沈阳', '南昌'
      ]
    }
  },
  created() {
    this.fetchJobs()
  },
  computed: {
    filteredJobs() {
      return this.jobs.filter(job => {
        const kw = this.searchKeyword
        const matchKeyword = !kw || job.job_title?.includes(kw) || job.job_category?.includes(kw)
        const matchCity = !this.city || job.location?.includes(this.city)
        const matchSalary = (!this.salaryMin || job.salary_max >= this.salaryMin) && (!this.salaryMax || job.salary_min <= this.salaryMax)
        return matchKeyword && matchCity && matchSalary
      })
    },
    paginatedJobs() {
      const start = (this.currentPage - 1) * this.pageSize
      return this.filteredJobs.slice(start, start + this.pageSize)
    },
    totalPages() {
      return Math.ceil(this.filteredJobs.length / this.pageSize)
    }
  },
  methods: {
    fetchJobs() {
      this.loading = true
      axios.get('/api/job/list').then(res => {
        this.jobs = res.data || []
      }).catch(() => alert('获取数据失败')).finally(() => (this.loading = false))
    },
    applyFilters() { this.currentPage = 1 },
    resetFilters() {
      this.searchKeyword = ''
      this.city = ''
      this.salaryMin = ''
      this.salaryMax = ''
      this.currentPage = 1
    },
    nextPage() { if (this.currentPage < this.totalPages) this.currentPage++ },
    prevPage() { if (this.currentPage > 1) this.currentPage-- },
    truncate(text, len) {
      if (!text) return '无'
      return text.length > len ? text.slice(0, len) + '...' : text
    },
    toggleExpand(id) { this.$set(this.expandedRows, id, !this.expandedRows[id]) },
    toggleExpandReq(id) { this.$set(this.expandedRowsReq, id, !this.expandedRowsReq[id]) },
    viewJob(job) { this.currentJob = job; this.showModal = true },
    openForm(job = null) {
      this.form = job ? { ...job } : {}
      this.customCategory = false
      this.customSalaryType = false
      this.customCity = false
      this.customNature = false
      this.customExperience = false
      this.customEducation = false
      this.showForm = true
    },
    closeForm() {
      this.showForm = false
      this.form = {}
    },
    saveJob() {
      if (this.form.id) {
        axios.put(`/api/job/${this.form.id}`, this.form).then(() => {
          alert('修改成功')
          this.fetchJobs()
          this.closeForm()
        }).catch(() => alert('修改失败'))
      }else {
    // 新增岗位要用 FormData（因为后端 add_job 只能接收 form-data）
    const formData = new FormData();

    // 遍历 this.form，把每个字段都放进 FormData
    for (const key in this.form) {
      if (this.form[key] !== null && this.form[key] !== undefined) {
        formData.append(key, this.form[key]);
      }
    }

    // 如果表单中有 logo 文件（假设 this.logo 是 <input type="file"> 选的文件）
    if (this.logo) {
      formData.append('logo', this.logo);
    }

    axios.post('/api/job/add', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(() => {
        alert('新增成功');
        this.fetchJobs();  // 刷新列表
        this.closeForm();  // 关闭弹窗
      })
      .catch(() => alert('新增失败'));
  }
},
    deleteJob(id) {
      if (confirm('确定删除该岗位吗？')) {
        axios.delete(`/api/job/${id}`).then(() => {
          this.jobs = this.jobs.filter(j => j.id !== id)
        }).catch(() => alert('删除失败'))
      }
    },
    checkCustomCategory() {
      this.customCategory = this.form.job_category === '_custom'
      if (this.customCategory) this.form.job_category = ''
    },
    checkCustomSalaryType() {
      this.customSalaryType = this.form.salary_type === '_custom'
      if (this.customSalaryType) this.form.salary_type = ''
    },
    checkCustomCity() {
      this.customCity = this.form.location === '_custom'
      if (this.customCity) this.form.location = ''
    },
    checkCustomNature() {
      this.customNature = this.form.job_nature === '_custom'
      if (this.customNature) this.form.job_nature = ''
    },
    checkCustomExperience() {
      this.customExperience = this.form.experience_req === '_custom'
      if (this.customExperience) this.form.experience_req = ''
    },
    checkCustomEducation() {
      this.customEducation = this.form.education_req === '_custom'
      if (this.customEducation) this.form.education_req = ''
    }
  }
}
</script>
<style scoped>
.add-btn-wrapper {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 15px;
}
.add-btn {
  background: #4caf50;
  color: #fff;
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.add-btn:hover {
  background: #43a047;
}
.form-modal form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.form-modal input, .form-modal textarea, .form-modal select {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-actions {
    min-width: 200px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}
.form-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.form-actions button:first-child { background: #1976d2; color: #fff; }
.form-actions button:last-child { background: #aaa; color: #fff; }
.detail-modal {
  width: 600px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  animation: fadeIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
  max-height: 85%;
  overflow-y: auto;
  font-size: 15px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #1976d2, #42a5f5);
  color: #fff;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.modal-header h2 {
  margin: 0;
  font-size: 22px;
}

.modal-close {
  font-size: 26px;
  cursor: pointer;
  transition: color 0.2s;
}
.modal-close:hover {
  color: #ffd54f;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #444;
}

.info-item .icon {
  font-size: 18px;
}

.section {
  background: #f9fbff;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}
.section h3 {
  margin: 0 0 6px 0;
  color: #1976d2;
  font-size: 16px;
}
.section p {
  margin: 0;
  line-height: 1.6;
  color: #333;
}

@keyframes fadeIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
/* 顶部标题渐变 */
.enhanced-form .modal-header {
  background: linear-gradient(135deg, #4e8cff, #7a60ff);
  color: #fff;
  padding: 15px 20px;
  border-radius: 8px 8px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.modal-header h2 { margin: 0; font-size: 20px; font-weight: bold; }
.modal-close {
  font-size: 22px;
  cursor: pointer;
  transition: 0.3s;
}
.modal-close:hover { transform: rotate(90deg); color: #ffd700; }

/* 表单卡片 */
.job-form {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  background: #fafbff;
  border-radius: 0 0 8px 8px;
  animation: fadeIn 0.5s ease-in-out;
}

/* 分组布局 */
.form-group { display: flex; flex-direction: column; gap: 5px; }
.form-group-row { display: flex; gap: 15px; }
.form-group-row > div { flex: 1; display: flex; flex-direction: column; gap: 5px; }
.full { width: 100%; }

/* 输入框美化 */
.job-form input, .job-form select, .job-form textarea {
  padding: 8px 10px;
  border: 1px solid #d0d7f0;
  border-radius: 6px;
  background: #fff;
  transition: all 0.3s ease;
  font-size: 14px;
}
.job-form input:focus, .job-form select:focus, .job-form textarea:focus {
  border-color: #7a60ff;
  box-shadow: 0 0 8px rgba(122,96,255,0.3);
  outline: none;
}
.job-form textarea { min-height: 80px; resize: vertical; }

/* 按钮炫酷渐变 */
.fancy-buttons button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}
.btn-save {
  background: linear-gradient(135deg, #4e8cff, #7a60ff);
  color: #fff;
}
.btn-save:hover {
  background: linear-gradient(135deg, #3a6de0, #6b4bff);
  transform: translateY(-2px);
}
.btn-cancel {
  background: #ddd;
  color: #333;
}
.btn-cancel:hover { background: #bbb; }

/* 模态卡片阴影 */
.enhanced-form {
  width: 650px;
  max-height: 85%;
  overflow-y: auto;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
  animation: slideUp 0.4s ease;
}

/* 动画 */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slideUp {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* 原本的样式保留 */
.job-page {
  max-width: 1300px;
  margin: 0 auto;
  padding: 20px;
  background: #f0f4fa;
  font-family: 'Microsoft YaHei', sans-serif;
}
.page-title { text-align: center; font-size: 30px; font-weight: bold; margin-bottom: 20px; color: #1976d2; }
.filters { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-bottom: 20px; }
.filter-input, .salary-input { padding: 8px; border-radius: 6px; border: 1px solid #ccc; }
.salary-filter { display: flex; gap: 6px; align-items: center; }
.filter-btn { background: #1976d2; color: #fff; padding: 8px 14px; border: none; border-radius: 6px; cursor: pointer; }
.filter-btn:hover { background: #1565c0; }
.filter-btn.reset { background: #aaa; }
.job-table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.job-table th, .job-table td { padding: 12px; border-bottom: 1px solid #e0e0e0; font-size: 14px; }
.job-table th { background: #e3f2fd; color: #333; }
.job-table td.salary { color: #d32f2f; font-weight: bold; }
.job-table tr:nth-child(even) { background: #f9fbff; }
.job-table tr:hover { background: #eaf4ff; }
.actions button { margin: 0 4px; padding: 5px 10px; border: none; border-radius: 4px; cursor: pointer; }
.actions button:hover { opacity: 0.85; }
.actions button:not(.delete-btn) { background: #1976d2; color: #fff; }
.actions .delete-btn { background: #e53935; color: #fff; }
.pagination { display: flex; justify-content: center; gap: 12px; margin-top: 20px; }
.pagination button { background: #1976d2; color: #fff; padding: 6px 12px; border: none; border-radius: 6px; cursor: pointer; }
.pagination button:disabled { background: #ccc; cursor: not-allowed; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; }
.modal-content { background: #fff; padding: 20px; border-radius: 8px; width: 500px; max-height: 80%; overflow-y: auto; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.modal-content h2 { margin-bottom: 10px; }
.close-btn { margin-top: 10px; background: #1976d2; color: #fff; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; }
</style>
