<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h2>课后托管管理系统</h2>
          <p>管理员登录</p>
        </div>
      </template>
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="用户类型" prop="user_type">
          <el-select v-model="loginForm.user_type" placeholder="请选择用户类型">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="家长" value="parent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="login" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const loginForm = reactive({
  username: 'admin',
  password: 'admin123',
  user_type: 'admin'
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ],
  user_type: [
    { required: true, message: '请选择用户类型', trigger: 'change' }
  ]
}

const login = async () => {
  loading.value = true
  try {
    const response = await authApi.login(loginForm)
    if (response.code === 200) {
      localStorage.setItem('token', response.data.access_token)
      ElMessage.success('登录成功')
      router.push('/students')
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f2f5;
}

.login-card {
  width: 400px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
}

.login-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.login-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.el-form-item {
  margin-bottom: 20px;
}

.el-button {
  width: 100%;
}
</style>
