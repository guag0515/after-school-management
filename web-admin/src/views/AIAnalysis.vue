<template>
  <div class="ai-analysis-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>AI分析</span>
          <el-button type="primary" @click="openGenerateDialog">生成分析</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.student_id" placeholder="请输入学生ID" style="width: 150px; margin-right: 10px;"></el-input>
        <el-select v-model="searchForm.analysis_period" placeholder="请选择分析周期" style="width: 150px; margin-right: 10px;">
          <el-option label="每周" value="每周"></el-option>
          <el-option label="每月" value="每月"></el-option>
          <el-option label="每学期" value="每学期"></el-option>
          <el-option label="每学年" value="每学年"></el-option>
        </el-select>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="analysisList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="student_id" label="学生ID"></el-table-column>
        <el-table-column prop="analysis_period" label="分析周期"></el-table-column>
        <el-table-column prop="analysis_content" label="分析内容" show-overflow-tooltip>
          <template #default="scope">
            <el-popover
              placement="top"
              width="400"
              trigger="click"
            >
              <template #reference>
                <span class="content-preview">{{ scope.row.analysis_content.substring(0, 50) }}...</span>
              </template>
              <div style="white-space: pre-wrap;">{{ scope.row.analysis_content }}</div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column prop="generated_at" label="生成时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.generated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="scope">
            <el-button type="danger" size="small" @click="deleteAnalysis(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </el-card>

    <!-- 生成分析对话框 -->
    <el-dialog
      v-model="generateDialogVisible"
      title="生成AI分析"
      width="400px"
    >
      <el-form
        ref="generateForm"
        :model="generateForm"
        :rules="generateRules"
        label-width="100px"
      >
        <el-form-item label="学生ID" prop="student_id">
          <el-input v-model="generateForm.student_id"></el-input>
        </el-form-item>
        <el-form-item label="分析周期" prop="analysis_period">
          <el-select v-model="generateForm.analysis_period">
            <el-option label="每周" value="每周"></el-option>
            <el-option label="每月" value="每月"></el-option>
            <el-option label="每学期" value="每学期"></el-option>
            <el-option label="每学年" value="每学年"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="generateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="generateAnalysis" :loading="loading">生成分析</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { aiAnalysisApi } from '../api'
import { ElMessage } from 'element-plus'

// AI分析列表
const analysisList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)

// 搜索表单
const searchForm = reactive({
  student_id: '',
  analysis_period: ''
})

// 生成分析对话框
const generateDialogVisible = ref(false)
const generateForm = reactive({
  student_id: '',
  analysis_period: '每周'
})

// 表单验证规则
const generateRules = {
  student_id: [{ required: true, message: '请输入学生ID', trigger: 'blur' }],
  analysis_period: [{ required: true, message: '请选择分析周期', trigger: 'change' }]
}

// 获取AI分析列表
const getAnalysisList = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      student_id: searchForm.student_id,
      analysis_period: searchForm.analysis_period
    }
    const response = await aiAnalysisApi.getList(params)
    if (response.code === 200) {
      analysisList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取AI分析列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getAnalysisList()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getAnalysisList()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getAnalysisList()
}

// 打开生成分析对话框
const openGenerateDialog = () => {
  // 重置表单
  Object.keys(generateForm).forEach(key => {
    generateForm[key] = ''
  })
  generateForm.analysis_period = '每周'
  generateDialogVisible.value = true
}

// 生成AI分析
const generateAnalysis = async () => {
  try {
    loading.value = true
    const response = await aiAnalysisApi.generate(generateForm)
    if (response.code === 200) {
      ElMessage.success('分析生成成功')
      generateDialogVisible.value = false
      getAnalysisList()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '生成分析失败')
  } finally {
    loading.value = false
  }
}

// 删除AI分析
const deleteAnalysis = async (id) => {
  try {
    const response = await aiAnalysisApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getAnalysisList()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 页面加载时获取AI分析列表
onMounted(() => {
  getAnalysisList()
})
</script>

<style scoped>
.ai-analysis-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}

.content-preview {
  cursor: pointer;
  color: #409EFF;
}
</style>