<template>
  <div class="homework-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>作业管理</span>
          <el-button type="primary" @click="openAddDialog">添加作业</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.student_id" placeholder="请输入学生ID" style="width: 150px; margin-right: 10px;"></el-input>
        <el-date-picker v-model="searchForm.date_from" type="date" placeholder="开始日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-date-picker v-model="searchForm.date_to" type="date" placeholder="结束日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="homeworkList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="student_id" label="学生ID"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="chinese_homework" label="语文作业" show-overflow-tooltip></el-table-column>
        <el-table-column prop="math_homework" label="数学作业" show-overflow-tooltip></el-table-column>
        <el-table-column prop="english_homework" label="英语作业" show-overflow-tooltip></el-table-column>
        <el-table-column prop="science_homework" label="科学作业" show-overflow-tooltip></el-table-column>
        <el-table-column prop="other_homework" label="其他作业" show-overflow-tooltip></el-table-column>
        <el-table-column prop="completion_status" label="完成情况">
          <template #default="scope">
            <el-tag :type="scope.row.completion_status === '已完成' ? 'success' : 'warning'">
              {{ scope.row.completion_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="teacher_evaluation" label="教师评价" show-overflow-tooltip></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteHomework(scope.row.id)">删除</el-button>
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

    <!-- 添加作业对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加作业"
      width="600px"
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
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="addForm.date" type="date" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="语文作业" prop="chinese_homework">
          <el-input v-model="addForm.chinese_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="数学作业" prop="math_homework">
          <el-input v-model="addForm.math_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="英语作业" prop="english_homework">
          <el-input v-model="addForm.english_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="科学作业" prop="science_homework">
          <el-input v-model="addForm.science_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="其他作业">
          <el-input v-model="addForm.other_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="完成情况" prop="completion_status">
          <el-select v-model="addForm.completion_status">
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="未完成" value="未完成"></el-option>
            <el-option label="部分完成" value="部分完成"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="教师评价">
          <el-input v-model="addForm.teacher_evaluation" type="textarea" rows="2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addHomework">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑作业对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑作业"
      width="600px"
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
        <el-form-item label="日期">
          <el-date-picker v-model="editForm.date" type="date" disabled style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="语文作业" prop="chinese_homework">
          <el-input v-model="editForm.chinese_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="数学作业" prop="math_homework">
          <el-input v-model="editForm.math_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="英语作业" prop="english_homework">
          <el-input v-model="editForm.english_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="科学作业" prop="science_homework">
          <el-input v-model="editForm.science_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="其他作业">
          <el-input v-model="editForm.other_homework" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="完成情况" prop="completion_status">
          <el-select v-model="editForm.completion_status">
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="未完成" value="未完成"></el-option>
            <el-option label="部分完成" value="部分完成"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="教师评价">
          <el-input v-model="editForm.teacher_evaluation" type="textarea" rows="2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateHomework">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { homeworkApi } from '../api'
import { ElMessage } from 'element-plus'

// 作业列表
const homeworkList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索表单
const searchForm = reactive({
  student_id: '',
  date_from: '',
  date_to: ''
})

// 添加作业对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  student_id: '',
  date: '',
  chinese_homework: '',
  math_homework: '',
  english_homework: '',
  science_homework: '',
  other_homework: '',
  completion_status: '已完成',
  teacher_evaluation: ''
})

// 编辑作业对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  student_id: '',
  date: '',
  chinese_homework: '',
  math_homework: '',
  english_homework: '',
  science_homework: '',
  other_homework: '',
  completion_status: '已完成',
  teacher_evaluation: ''
})

// 表单验证规则
const addRules = {
  student_id: [{ required: true, message: '请输入学生ID', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  chinese_homework: [{ required: true, message: '请输入语文作业', trigger: 'blur' }],
  math_homework: [{ required: true, message: '请输入数学作业', trigger: 'blur' }],
  english_homework: [{ required: true, message: '请输入英语作业', trigger: 'blur' }],
  science_homework: [{ required: true, message: '请输入科学作业', trigger: 'blur' }],
  completion_status: [{ required: true, message: '请选择完成情况', trigger: 'change' }]
}

const editRules = {
  chinese_homework: [{ required: true, message: '请输入语文作业', trigger: 'blur' }],
  math_homework: [{ required: true, message: '请输入数学作业', trigger: 'blur' }],
  english_homework: [{ required: true, message: '请输入英语作业', trigger: 'blur' }],
  science_homework: [{ required: true, message: '请输入科学作业', trigger: 'blur' }],
  completion_status: [{ required: true, message: '请选择完成情况', trigger: 'change' }]
}

// 获取作业列表
const getHomework = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      student_id: searchForm.student_id,
      date_from: searchForm.date_from,
      date_to: searchForm.date_to
    }
    const response = await homeworkApi.getList(params)
    if (response.code === 200) {
      homeworkList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取作业列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getHomework()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getHomework()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getHomework()
}

// 打开添加作业对话框
const openAddDialog = () => {
  // 重置表单
  Object.keys(addForm).forEach(key => {
    addForm[key] = ''
  })
  addForm.completion_status = '已完成'
  addDialogVisible.value = true
}

// 添加作业
const addHomework = async () => {
  try {
    const response = await homeworkApi.create(addForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addDialogVisible.value = false
      getHomework()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 打开编辑作业对话框
const openEditDialog = (row) => {
  // 复制数据到编辑表单
  Object.assign(editForm, row)
  editDialogVisible.value = true
}

// 更新作业
const updateHomework = async () => {
  try {
    const response = await homeworkApi.update(editForm.id, editForm)
    if (response.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      getHomework()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

// 删除作业
const deleteHomework = async (id) => {
  try {
    const response = await homeworkApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getHomework()
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

// 页面加载时获取作业列表
onMounted(() => {
  getHomework()
})
</script>

<style scoped>
.homework-container {
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
</style>