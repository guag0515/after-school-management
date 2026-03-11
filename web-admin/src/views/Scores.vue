<template>
  <div class="scores-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>成绩管理</span>
          <el-button type="primary" @click="openAddDialog">添加成绩</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.student_id" placeholder="请输入学生ID" style="width: 150px; margin-right: 10px;"></el-input>
        <el-input v-model="searchForm.subject" placeholder="请输入考试科目" style="width: 150px; margin-right: 10px;"></el-input>
        <el-select v-model="searchForm.exam_type" placeholder="请选择考试类型" style="width: 150px; margin-right: 10px;">
          <el-option label="单元测试" value="单元测试"></el-option>
          <el-option label="期中考试" value="期中考试"></el-option>
          <el-option label="期末考试" value="期末考试"></el-option>
          <el-option label="模拟考试" value="模拟考试"></el-option>
        </el-select>
        <el-date-picker v-model="searchForm.exam_date_from" type="date" placeholder="开始日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-date-picker v-model="searchForm.exam_date_to" type="date" placeholder="结束日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="scoresList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="student_id" label="学生ID"></el-table-column>
        <el-table-column prop="subject" label="考试科目"></el-table-column>
        <el-table-column prop="exam_type" label="考试类型"></el-table-column>
        <el-table-column prop="score" label="成绩"></el-table-column>
        <el-table-column prop="exam_date" label="考试时间"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteScore(scope.row.id)">删除</el-button>
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

    <!-- 添加成绩对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加成绩"
      width="400px"
    >
      <el-form
        ref="addForm"
        :model="addForm"
        :rules="addRules"
        label-width="100px"
      >
        <el-form-item label="学生ID" prop="student_id">
          <el-input v-model="addForm.student_id"></el-input>
        </el-form-item>
        <el-form-item label="考试科目" prop="subject">
          <el-input v-model="addForm.subject"></el-input>
        </el-form-item>
        <el-form-item label="考试类型" prop="exam_type">
          <el-select v-model="addForm.exam_type">
            <el-option label="单元测试" value="单元测试"></el-option>
            <el-option label="期中考试" value="期中考试"></el-option>
            <el-option label="期末考试" value="期末考试"></el-option>
            <el-option label="模拟考试" value="模拟考试"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成绩" prop="score">
          <el-input v-model="addForm.score" type="number"></el-input>
        </el-form-item>
        <el-form-item label="考试时间" prop="exam_date">
          <el-date-picker v-model="addForm.exam_date" type="date" style="width: 100%"></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addScore">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑成绩对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑成绩"
      width="400px"
    >
      <el-form
        ref="editForm"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="学生ID">
          <el-input v-model="editForm.student_id" disabled></el-input>
        </el-form-item>
        <el-form-item label="考试科目" prop="subject">
          <el-input v-model="editForm.subject"></el-input>
        </el-form-item>
        <el-form-item label="考试类型" prop="exam_type">
          <el-select v-model="editForm.exam_type">
            <el-option label="单元测试" value="单元测试"></el-option>
            <el-option label="期中考试" value="期中考试"></el-option>
            <el-option label="期末考试" value="期末考试"></el-option>
            <el-option label="模拟考试" value="模拟考试"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="成绩" prop="score">
          <el-input v-model="editForm.score" type="number"></el-input>
        </el-form-item>
        <el-form-item label="考试时间" prop="exam_date">
          <el-date-picker v-model="editForm.exam_date" type="date" style="width: 100%"></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateScore">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { scoreApi } from '../api'
import { ElMessage } from 'element-plus'

// 成绩列表
const scoresList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索表单
const searchForm = reactive({
  student_id: '',
  subject: '',
  exam_type: '',
  exam_date_from: '',
  exam_date_to: ''
})

// 添加成绩对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  student_id: '',
  subject: '',
  exam_type: '单元测试',
  score: '',
  exam_date: ''
})

// 编辑成绩对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  student_id: '',
  subject: '',
  exam_type: '单元测试',
  score: '',
  exam_date: ''
})

// 表单验证规则
const addRules = {
  student_id: [{ required: true, message: '请输入学生ID', trigger: 'blur' }],
  subject: [{ required: true, message: '请输入考试科目', trigger: 'blur' }],
  exam_type: [{ required: true, message: '请选择考试类型', trigger: 'change' }],
  score: [{ required: true, message: '请输入成绩', trigger: 'blur' }],
  exam_date: [{ required: true, message: '请选择考试时间', trigger: 'change' }]
}

const editRules = {
  subject: [{ required: true, message: '请输入考试科目', trigger: 'blur' }],
  exam_type: [{ required: true, message: '请选择考试类型', trigger: 'change' }],
  score: [{ required: true, message: '请输入成绩', trigger: 'blur' }],
  exam_date: [{ required: true, message: '请选择考试时间', trigger: 'change' }]
}

// 获取成绩列表
const getScores = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      student_id: searchForm.student_id,
      subject: searchForm.subject,
      exam_type: searchForm.exam_type,
      exam_date_from: searchForm.exam_date_from,
      exam_date_to: searchForm.exam_date_to
    }
    const response = await scoreApi.getList(params)
    if (response.code === 200) {
      scoresList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取成绩列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getScores()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getScores()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getScores()
}

// 打开添加成绩对话框
const openAddDialog = () => {
  // 重置表单
  Object.keys(addForm).forEach(key => {
    addForm[key] = ''
  })
  addForm.exam_type = '单元测试'
  addDialogVisible.value = true
}

// 添加成绩
const addScore = async () => {
  try {
    const response = await scoreApi.create(addForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addDialogVisible.value = false
      getScores()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 打开编辑成绩对话框
const openEditDialog = (row) => {
  // 复制数据到编辑表单
  Object.assign(editForm, row)
  editDialogVisible.value = true
}

// 更新成绩
const updateScore = async () => {
  try {
    const response = await scoreApi.update(editForm.id, editForm)
    if (response.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      getScores()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

// 删除成绩
const deleteScore = async (id) => {
  try {
    const response = await scoreApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getScores()
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

// 页面加载时获取成绩列表
onMounted(() => {
  getScores()
})
</script>

<style scoped>
.scores-container {
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
  flex-wrap: wrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}
</style>