// pages/homework/homework.js
const { homeworkApi } = require('../../utils/api');

Page({
  data: {
    homeworkList: [],
    date: '',
    currentDate: '',
    studentId: ''
  },

  onLoad() {
    // 获取当前日期
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const currentDate = `${year}-${month}-${day}`;
    
    this.setData({
      date: currentDate,
      currentDate: currentDate,
      studentId: getApp().globalData.studentId
    });
    
    // 获取作业数据
    this.getHomeworkList();
  },

  bindDateChange(e) {
    this.setData({ date: e.detail.value });
    this.getHomeworkList();
  },

  async getHomeworkList() {
    const { date, studentId } = this.data;
    
    try {
      wx.showLoading({ title: '加载中...' });
      const res = await homeworkApi.getList({
        student_id: studentId,
        date_from: date,
        date_to: date
      });
      
      if (res.code === 200) {
        this.setData({ homeworkList: res.data.items });
      } else {
        wx.showToast({ title: res.message || '获取作业失败', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '获取作业失败', icon: 'none' });
      console.error('获取作业失败:', error);
    } finally {
      wx.hideLoading();
    }
  }
});