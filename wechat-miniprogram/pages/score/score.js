// pages/score/score.js
const { scoreApi } = require('../../utils/api');

Page({
  data: {
    scoreList: [],
    month: '',
    currentMonth: '',
    studentId: ''
  },

  onLoad() {
    // 获取当前月份
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const currentMonth = `${year}-${month}`;
    
    this.setData({
      month: currentMonth,
      currentMonth: currentMonth,
      studentId: getApp().globalData.studentId
    });
    
    // 获取成绩数据
    this.getScoreList();
  },

  bindMonthChange(e) {
    this.setData({ month: e.detail.value });
    this.getScoreList();
  },

  async getScoreList() {
    const { month, studentId } = this.data;
    // 计算月份的开始和结束日期
    const [year, monthNum] = month.split('-');
    const startDate = `${year}-${monthNum}-01`;
    // 获取月份的最后一天
    const lastDay = new Date(year, monthNum, 0).getDate();
    const endDate = `${year}-${monthNum}-${lastDay}`;
    
    try {
      wx.showLoading({ title: '加载中...' });
      const res = await scoreApi.getList({
        student_id: studentId,
        exam_date_from: startDate,
        exam_date_to: endDate
      });
      
      if (res.code === 200) {
        this.setData({ scoreList: res.data.items });
      } else {
        wx.showToast({ title: res.message || '获取成绩失败', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '获取成绩失败', icon: 'none' });
      console.error('获取成绩失败:', error);
    } finally {
      wx.hideLoading();
    }
  }
});