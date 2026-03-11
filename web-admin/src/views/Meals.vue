<template>
  <div class="meals-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>餐饮管理</span>
          <el-button type="primary" @click="openAddDialog">添加餐饮记录</el-button>
        </div>
      </template>
      <div class="search-bar">
        <el-input v-model="searchForm.student_id" placeholder="请输入学生ID" style="width: 150px; margin-right: 10px;"></el-input>
        <el-date-picker v-model="searchForm.date_from" type="date" placeholder="开始日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-date-picker v-model="searchForm.date_to" type="date" placeholder="结束日期" style="width: 180px; margin-right: 10px;"></el-date-picker>
        <el-button type="primary" @click="search">搜索</el-button>
      </div>
      <el-table :data="mealsList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="student_id" label="学生ID"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="breakfast" label="早餐" show-overflow-tooltip></el-table-column>
        <el-table-column prop="lunch" label="午餐" show-overflow-tooltip></el-table-column>
        <el-table-column prop="dinner" label="晚餐" show-overflow-tooltip></el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="openEditDialog(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteMeal(scope.row.id)">删除</el-button>
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

    <!-- 添加餐饮记录对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加餐饮记录"
      width="500px"
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
        <el-form-item label="早餐" prop="breakfast">
          <el-input v-model="addForm.breakfast" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="午餐" prop="lunch">
          <el-input v-model="addForm.lunch" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="晚餐" prop="dinner">
          <el-input v-model="addForm.dinner" type="textarea" rows="2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="addMeal">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑餐饮记录对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑餐饮记录"
      width="500px"
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
        <el-form-item label="早餐" prop="breakfast">
          <el-input v-model="editForm.breakfast" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="午餐" prop="lunch">
          <el-input v-model="editForm.lunch" type="textarea" rows="2"></el-input>
        </el-form-item>
        <el-form-item label="晚餐" prop="dinner">
          <el-input v-model="editForm.dinner" type="textarea" rows="2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="updateMeal">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { mealApi } from '../api'
import { ElMessage } from 'element-plus'

// 餐饮记录列表
const mealsList = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 搜索表单
const searchForm = reactive({
  student_id: '',
  date_from: '',
  date_to: ''
})

// 添加餐饮记录对话框
const addDialogVisible = ref(false)
const addForm = reactive({
  student_id: '',
  date: '',
  breakfast: '',
  lunch: '',
  dinner: ''
})

// 编辑餐饮记录对话框
const editDialogVisible = ref(false)
const editForm = reactive({
  id: '',
  student_id: '',
  date: '',
  breakfast: '',
  lunch: '',
  dinner: ''
})

// 表单验证规则
const addRules = {
  student_id: [{ required: true, message: '请输入学生ID', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  breakfast: [{ required: true, message: '请输入早餐', trigger: 'blur' }],
  lunch: [{ required: true, message: '请输入午餐', trigger: 'blur' }],
  dinner: [{ required: true, message: '请输入晚餐', trigger: 'blur' }]
}

const editRules = {
  breakfast: [{ required: true, message: '请输入早餐', trigger: 'blur' }],
  lunch: [{ required: true, message: '请输入午餐', trigger: 'blur' }],
  dinner: [{ required: true, message: '请输入晚餐', trigger: 'blur' }]
}

// 获取餐饮记录列表
const getMeals = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      student_id: searchForm.student_id,
      date_from: searchForm.date_from,
      date_to: searchForm.date_to
    }
    const response = await mealApi.getList(params)
    if (response.code === 200) {
      mealsList.value = response.data.items
      total.value = response.data.total
    }
  } catch (error) {
    ElMessage.error(error.message || '获取餐饮记录列表失败')
  }
}

// 搜索
const search = () => {
  currentPage.value = 1
  getMeals()
}

// 分页
const handleSizeChange = (size) => {
  pageSize.value = size
  getMeals()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getMeals()
}

// 打开添加餐饮记录对话框
const openAddDialog = () => {
  // 重置表单
  Object.keys(addForm).forEach(key => {
    addForm[key] = ''
  })
  addDialogVisible.value = true
}

// 添加餐饮记录
const addMeal = async () => {
  try {
    const response = await mealApi.create(addForm)
    if (response.code === 200) {
      ElMessage.success('添加成功')
      addDialogVisible.value = false
      getMeals()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '添加失败')
  }
}

// 打开编辑餐饮记录对话框
const openEditDialog = (row) => {
  // 复制数据到编辑表单
  Object.assign(editForm, row)
  editDialogVisible.value = true
}

// 更新餐饮记录
const updateMeal = async () => {
  try {
    const response = await mealApi.update(editForm.id, editForm)
    if (response.code === 200) {
      ElMessage.success('更新成功')
      editDialogVisible.value = false
      getMeals()
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '更新失败')
  }
}

// 删除餐饮记录
const deleteMeal = async (id) => {
  try {
    const response = await mealApi.delete(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      getMeals()
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

// 页面加载时获取餐饮记录列表
onMounted(() => {
  getMeals()
})
</script>

<style scoped>
.meals-container {
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