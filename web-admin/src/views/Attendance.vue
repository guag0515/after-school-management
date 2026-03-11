<template>
  <div class="attendance-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考勤管理</span>
          <el-button type="primary" @click="openAddDialog">添加考勤</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.student_id" placeholder="请输入学生ID" style="width: 150px; margin-right: 10px;"></el-input>
        <el-date-picker v-model="searchForm.date_from" type="date" placeholder="开始日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-date-picker v-model="searchForm.date_to" type="date" placeholder="结束日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-select v-model="searchForm.is_present" placeholder="请选择考勤状态" style="width: 120px; margin-right: 10px;">
          <el-option label="已到校" value="1"></el-option>
          <el-option label="未到校" value="0"></el-option>
        </el-select>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="attendanceList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="student_id" label="学生ID"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="is_present" label="考勤状态">
          <template #default="scope">
            <el-tag :type="scope.row.is_present === 1 ? 'success' : 'danger'">
              {{ scope.row.is_present === 1 ? '已到校' : '未到校' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteAttendance(scope.row.id)">删除</el-button>
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

    <!-- 添加考勤对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加考勤"
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
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="addForm.date" type="date" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="考勤状态" prop="is_present">
          <el-radio-group v-model="addForm.is_present">
            <el-radio label="1">已到校</el-radio>
            <el-radio label="0">未到校</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addAttendance">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑考勤对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑考勤"
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
        <el-form-item label="日期">
          <el-date-picker v-model="editForm.date" type="date" disabled style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="考勤状态" prop="is_present">
          <el-radio-group v-model="editForm.is_present">
            <el-radio label="1">已到校</el-radio>
            <el-radio label="0">未到校</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateAttendance">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { attendanceApi } from '../api'
import { ElMessage } from 'element-plus'

// 考勤列表
const attendanceList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索表单
const searchForm = reactive({
  student_id: '',
  date_from: '',
  date_to: '',
  is_present: ''
})

// 添加考勤对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  student_id: '',
  date: '',
  is_present: 1
})

// 编辑考勤对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  student_id: '',
  date: '',
  is_present: 1
})

// 表单验证规则
const addRules = {
  student_id: [{ required: true, message: '请输入学生ID', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  is_present: [{ required: true, message: '请选择考勤状态', trigger: 'change' }]
}

const editRules = {
  is_present: [{ required: true, message: '请选择考勤状态', trigger: 'change' }]
}

// 获取考勤列表
const getAttendance = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      student_id: searchForm.student_id,
      date_from: searchForm.date_from,
      date_to: searchForm.date_to,
      is_present: searchForm.is_present
    }
    const response = await attendanceApi.getList(params)
    if (response.code === 200) {
      attendanceList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取考勤列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getAttendance()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getAttendance()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getAttendance()
}

// 打开添加考勤对话框
const openAddDialog = () => {
  // 重置表单
  Object.keys(addForm).forEach(key => {
    addForm[key] = ''
  })
  addForm.is_present = 1
  addDialogVisible.value = true
}

// 添加考勤
const addAttendance = async () => {
  try {
    const response = await attendanceApi.create(addForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addDialogVisible.value = false
      getAttendance()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 打开编辑考勤对话框
const openEditDialog = (row) => {
  // 复制数据到编辑表单
  Object.assign(editForm, row)
  editDialogVisible.value = true
}

// 更新考勤
const updateAttendance = async () => {
  try {
    const response = await attendanceApi.update(editForm.id, editForm)
    if (response.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      getAttendance()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

// 删除考勤
const deleteAttendance = async (id) => {
  try {
    const response = await attendanceApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getAttendance()
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

// 页面加载时获取考勤列表
onMounted(() => {
  getAttendance()
})
</script>

<style scoped>
.attendance-container {
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
