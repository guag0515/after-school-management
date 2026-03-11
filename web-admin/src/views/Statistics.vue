<template>
  <div class="statistics-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据统计</span>
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="handleDateChange"
          ></el-date-picker>
        </div>
      </template>
      
      <div class="statistics-grid">
        <!-- 学生考勤统计 -->
        <div class="statistics-item">
          <h3>学生考勤统计</h3>
          <div ref="attendanceChart" class="chart-container"></div>
        </div>
        
        <!-- 学生成绩统计 -->
        <div class="statistics-item">
          <h3>学生成绩统计</h3>
          <div ref="scoreChart" class="chart-container"></div>
        </div>
        
        <!-- 作业完成情况统计 -->
        <div class="statistics-item">
          <h3>作业完成情况统计</h3>
          <div ref="homeworkChart" class="chart-container"></div>
        </div>
        
        <!-- 餐饮情况统计 -->
        <div class="statistics-item">
          <h3>餐饮情况统计</h3>
          <div ref="mealChart" class="chart-container"></div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

// 日期范围
const dateRange = ref([])

// 图表引用
const attendanceChart = ref(null)
const scoreChart = ref(null)
const homeworkChart = ref(null)
const mealChart = ref(null)

// 图表实例
let attendanceChartInstance = null
let scoreChartInstance = null
let homeworkChartInstance = null
let mealChartInstance = null

// 初始化考勤统计图表
const initAttendanceChart = () => {
  if (!attendanceChart.value) return
  
  attendanceChartInstance = echarts.init(attendanceChart.value)
  
  const option = {
    title: {
      text: '考勤情况',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '考勤状态',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 45, name: '已到校' },
          { value: 5, name: '未到校' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  attendanceChartInstance.setOption(option)
}

// 初始化成绩统计图表
const initScoreChart = () => {
  if (!scoreChart.value) return
  
  scoreChartInstance = echarts.init(scoreChart.value)
  
  const option = {
    title: {
      text: '成绩分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['优秀', '良好', '及格', '不及格']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '学生数',
        type: 'bar',
        data: [15, 20, 10, 5]
      }
    ]
  }
  
  scoreChartInstance.setOption(option)
}

// 初始化作业完成情况图表
const initHomeworkChart = () => {
  if (!homeworkChart.value) return
  
  homeworkChartInstance = echarts.init(homeworkChart.value)
  
  const option = {
    title: {
      text: '作业完成情况',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '完成状态',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 35, name: '已完成' },
          { value: 10, name: '部分完成' },
          { value: 5, name: '未完成' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  homeworkChartInstance.setOption(option)
}

// 初始化餐饮情况图表
const initMealChart = () => {
  if (!mealChart.value) return
  
  mealChartInstance = echarts.init(mealChart.value)
  
  const option = {
    title: {
      text: '餐饮满意度',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['早餐', '午餐', '晚餐']
    },
    yAxis: {
      type: 'value',
      max: 5
    },
    series: [
      {
        name: '满意度',
        type: 'bar',
        data: [4.2, 4.5, 4.3]
      }
    ]
  }
  
  mealChartInstance.setOption(option)
}

// 处理日期范围变化
const handleDateChange = () => {
  // 这里可以根据日期范围重新获取数据并更新图表
  ElMessage.info('日期范围已更新，图表数据将重新加载')
  // 实际项目中这里应该调用API获取对应日期范围的数据
}

// 监听窗口大小变化，调整图表大小
const handleResize = () => {
  attendanceChartInstance?.resize()
  scoreChartInstance?.resize()
  homeworkChartInstance?.resize()
  mealChartInstance?.resize()
}

// 页面加载时初始化图表
onMounted(() => {
  nextTick(() => {
    initAttendanceChart()
    initScoreChart()
    initHomeworkChart()
    initMealChart()
    
    // 监听窗口大小变化
    window.addEventListener('resize', handleResize)
  })
})

// 组件卸载时清理
watch(
  () => false,
  () => {
    window.removeEventListener('resize', handleResize)
    attendanceChartInstance?.dispose()
    scoreChartInstance?.dispose()
    homeworkChartInstance?.dispose()
    mealChartInstance?.dispose()
  },
  { once: true }
)
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.statistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.statistics-item {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.statistics-item h3 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.chart-container {
  width: 100%;
  height: 300px;
}

@media (max-width: 768px) {
  .statistics-grid {
    grid-template-columns: 1fr;
  }
}
</style>