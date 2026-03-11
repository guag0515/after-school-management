// pages/login/login.js
const { login } = require('../../utils/api');

Page({
  data: {
    phone: '',
    password: ''
  },

  bindPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  bindPasswordInput(e) {
    this.setData({ password: e.detail.value });
  },

  async login() {
    const { phone, password } = this.data;
    
    if (!phone || !password) {
      wx.showToast({ title: '请输入手机号和密码', icon: 'none' });
      return;
    }

    try {
      wx.showLoading({ title: '登录中...' });
      const res = await login({ phone, password });
      
      if (res.code === 200) {
        // 保存token和学生ID到全局数据
        const app = getApp();
        app.globalData.token = res.data.token;
        app.globalData.studentId = res.data.student_id;
        
        // 跳转到考勤页面
        wx.switchTab({ url: '/pages/attendance/attendance' });
      } else {
        wx.showToast({ title: res.message || '登录失败', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '登录失败', icon: 'none' });
      console.error('登录失败:', error);
    } finally {
      wx.hideLoading();
    }
  }
});