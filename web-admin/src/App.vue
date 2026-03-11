<template>
  <div class="app-container">
    <el-container style="height: 100vh;">
      <el-aside width="200px" style="background-color: #f0f2f5;">
        <div class="logo">
          <h2>课后托管管理系统</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/students">
            <el-icon><User /></el-icon>
            <span>学生管理</span>
          </el-menu-item>
          <el-menu-item index="/attendance">
            <el-icon><Timer /></el-icon>
            <span>考勤管理</span>
          </el-menu-item>
          <el-menu-item index="/homework">
            <el-icon><Document /></el-icon>
            <span>作业管理</span>
          </el-menu-item>
          <el-menu-item index="/scores">
            <el-icon><DataAnalysis /></el-icon>
            <span>成绩管理</span>
          </el-menu-item>
          <el-menu-item index="/meals">
            <el-icon><Mugcup /></el-icon>
            <span>餐饮管理</span>
          </el-menu-item>
          <el-menu-item index="/ai-analysis">
            <el-icon><Cpu /></el-icon>
            <span>AI分析</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <el-icon><PieChart /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="background-color: #fff; border-bottom: 1px solid #e0e0e0; display: flex; justify-content: space-between; align-items: center;">
          <h1 style="margin: 0; font-size: 18px;">{{ currentPage }}</h1>
          <div>
            <el-dropdown>
              <span class="el-dropdown-link">
                管理员 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  User,
  Timer,
  Document,
  DataAnalysis,
  Mugcup,
  Cpu,
  PieChart,
  ArrowDown
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const activeMenu = ref('/students')
const currentPage = ref('学生管理')

const pageTitles = {
  '/students': '学生管理',
  '/attendance': '考勤管理',
  '/homework': '作业管理',
  '/scores': '成绩管理',
  '/meals': '餐饮管理',
  '/ai-analysis': 'AI分析',
  '/statistics': '数据统计'
}

const handleMenuSelect = (key) => {
  router.push(key)
  activeMenu.value = key
  currentPage.value = pageTitles[key]
}

const logout = () => {
  // 清除token
  localStorage.removeItem('token')
  // 跳转到登录页
  router.push('/login')
}

onMounted(() => {
  activeMenu.value = route.path
  currentPage.value = pageTitles[route.path] || '学生管理'
})
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e0e0e0;
}

.logo h2 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.el-menu-vertical-demo {
  height: calc(100vh - 60px);
}

.el-header {
  padding: 0 20px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #606266;
}
</style>
