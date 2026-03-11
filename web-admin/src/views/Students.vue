<template>
  <div class="students-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>学生管理</span>
          <el-button type="primary" @click="openAddDialog">添加学生</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.name" placeholder="请输入学生姓名" style="width: 200px; margin-right: 10px;"></el-input>
        <el-input v-model="searchForm.class" placeholder="请输入班级" style="width: 200px; margin-right: 10px;"></el-input>
        <el-select v-model="searchForm.service_type" placeholder="请选择服务类型" style="width: 150px; margin-right: 10px;">
          <el-option label="全托" value="全托"></el-option>
          <el-option label="午托" value="午托"></el-option>
          <el-option label="晚托" value="晚托"></el-option>
          <el-option label="半托" value="半托"></el-option>
        </el-select>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="studentsList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column prop="gender" label="性别">
          <template #default="scope">
            {{ scope.row.gender === 1 ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="class" label="班级"></el-table-column>
        <el-table-column prop="service_type" label="服务类型"></el-table-column>
        <el-table-column prop="parent1_phone" label="家长1手机号"></el-table-column>
        <el-table-column prop="parent2_phone" label="家长2手机号"></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteStudent(scope.row.id)">删除</el-button>
            <el-button type="info" size="small" @click="openAddParentDialog(scope.row.id)">添加家长</el-button>
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

    <!-- 添加学生对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加学生"
      width="500px"
    >
      <el-form
        ref="addForm"
        :model="addForm"
        :rules="addRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="addForm.gender">
            <el-radio label="1">男</el-radio>
            <el-radio label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="班级" prop="class">
          <el-input v-model="addForm.class"></el-input>
        </el-form-item>
        <el-form-item label="服务类型" prop="service_type">
          <el-select v-model="addForm.service_type">
            <el-option label="全托" value="全托"></el-option>
            <el-option label="午托" value="午托"></el-option>
            <el-option label="晚托" value="晚托"></el-option>
            <el-option label="半托" value="半托"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="家长1手机号" prop="parent1_phone">
          <el-input v-model="addForm.parent1_phone"></el-input>
        </el-form-item>
        <el-form-item label="家长2手机号">
          <el-input v-model="addForm.parent2_phone"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addStudent">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑学生对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑学生"
      width="500px"
    >
      <el-form
        ref="editForm"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editForm.name"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editForm.gender">
            <el-radio label="1">男</el-radio>
            <el-radio label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="班级" prop="class">
          <el-input v-model="editForm.class"></el-input>
        </el-form-item>
        <el-form-item label="服务类型" prop="service_type">
          <el-select v-model="editForm.service_type">
            <el-option label="全托" value="全托"></el-option>
            <el-option label="午托" value="午托"></el-option>
            <el-option label="晚托" value="晚托"></el-option>
            <el-option label="半托" value="半托"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="家长1手机号" prop="parent1_phone">
          <el-input v-model="editForm.parent1_phone"></el-input>
        </el-form-item>
        <el-form-item label="家长2手机号">
          <el-input v-model="editForm.parent2_phone"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateStudent">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加家长对话框 -->
    <el-dialog
      v-model="addParentDialogVisible"
      title="添加家长"
      width="400px"
    >
      <el-form
        ref="parentForm"
        :model="parentForm"
        :rules="parentRules"
        label-width="100px"
      >
        <el-form-item label="学生ID" prop="student_id">
          <el-input v-model="parentForm.student_id" disabled></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="parentForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="parentForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="与学生关系" prop="relation">
          <el-input v-model="parentForm.relation"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addParentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addParent">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { studentApi } from '../api'
import { ElMessage } from 'element-plus'

// 学生列表
const studentsList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索表单
const searchForm = reactive({
  name: '',
  class: '',
  service_type: ''
})

// 添加学生对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  name: '',
  gender: 1,
  class: '',
  service_type: '',
  parent1_phone: '',
  parent2_phone: ''
})

// 编辑学生对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  name: '',
  gender: 1,
  class: '',
  service_type: '',
  parent1_phone: '',
  parent2_phone: ''
})

// 添加家长对话框
const addParentDialogVisible = ref(false)
const parentForm = reactive({
  student_id: '',
  phone: '',
  password: '',
  relation: ''
})

// 表单验证规则
const addRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  class: [{ required: true, message: '请输入班级', trigger: 'blur' }],
  service_type: [{ required: true, message: '请选择服务类型', trigger: 'change' }],
  parent1_phone: [{ required: true, message: '请输入家长1手机号', trigger: 'blur' }]
}

const editRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  class: [{ required: true, message: '请输入班级', trigger: 'blur' }],
  service_type: [{ required: true, message: '请选择服务类型', trigger: 'change' }],
  parent1_phone: [{ required: true, message: '请输入家长1手机号', trigger: 'blur' }]
}

const parentRules = {
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  relation: [{ required: true, message: '请输入与学生关系', trigger: 'blur' }]
}

// 获取学生列表
const getStudents = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      name: searchForm.name,
      class: searchForm.class,
      service_type: searchForm.service_type
    }
    const response = await studentApi.getList(params)
    if (response.code === 200) {
      studentsList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取学生列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getStudents()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getStudents()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getStudents()
}

// 打开添加学生对话框
const openAddDialog = () => {
  // 重置表单
  Object.keys(addForm).forEach(key => {
    addForm[key] = ''
  })
  addForm.gender = 1
  addDialogVisible.value = true
}

// 添加学生
const addStudent = async () => {
  try {
    const response = await studentApi.create(addForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addDialogVisible.value = false
      getStudents()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 打开编辑学生对话框
const openEditDialog = (row) => {
  // 复制数据到编辑表单
  Object.assign(editForm, row)
  editDialogVisible.value = true
}

// 更新学生
const updateStudent = async () => {
  try {
    const response = await studentApi.update(editForm.id, editForm)
    if (response.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      getStudents()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

// 删除学生
const deleteStudent = async (id) => {
  try {
    const response = await studentApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getStudents()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}

// 打开添加家长对话框
const openAddParentDialog = (studentId) => {
  // 重置表单
  Object.keys(parentForm).forEach(key => {
    parentForm[key] = ''
  })
  parentForm.student_id = studentId
  addParentDialogVisible.value = true
}

// 添加家长
const addParent = async () => {
  try {
    const response = await studentApi.createParent(parentForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addParentDialogVisible.value = false
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 页面加载时获取学生列表
onMounted(() => {
  getStudents()
})
</script>

<style scoped>
.students-container {
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
