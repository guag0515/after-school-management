// pages/meal/meal.js
const { mealApi } = require('../../utils/api');

Page({
  data: {
    mealList: [],
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
    
    // 获取餐饮数据
    this.getMealList();
  },

  bindDateChange(e) {
    this.setData({ date: e.detail.value });
    this.getMealList();
  },

  async getMealList() {
    const { date, studentId } = this.data;
    
    try {
      wx.showLoading({ title: '加载中...' });
      const res = await mealApi.getList({
        student_id: studentId,
        date_from: date,
        date_to: date
      });
      
      if (res.code === 200) {
        this.setData({ mealList: res.data.items });
      } else {
        wx.showToast({ title: res.message || '获取餐饮记录失败', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '获取餐饮记录失败', icon: 'none' });
      console.error('获取餐饮记录失败:', error);
    } finally {
      wx.hideLoading();
    }
  }
});