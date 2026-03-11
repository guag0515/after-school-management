// pages/ai-analysis/ai-analysis.js
const { aiAnalysisApi } = require('../../utils/api');

Page({
  data: {
    analysisList: [],
    periods: ['每周', '每月', '每学期', '每学年'],
    periodIndex: 0,
    studentId: ''
  },

  onLoad() {
    this.setData({
      studentId: getApp().globalData.studentId
    });
    
    // 获取AI分析数据
    this.getAnalysisList();
  },

  bindPeriodChange(e) {
    this.setData({ periodIndex: e.detail.value });
    this.getAnalysisList();
  },

  async getAnalysisList() {
    const { periodIndex, periods, studentId } = this.data;
    const analysisPeriod = periods[periodIndex];
    
    try {
      wx.showLoading({ title: '加载中...' });
      const res = await aiAnalysisApi.getList({
        student_id: studentId,
        analysis_period: analysisPeriod
      });
      
      if (res.code === 200) {
        this.setData({ analysisList: res.data.items });
      } else {
        wx.showToast({ title: res.message || '获取分析失败', icon: 'none' });
      }
    } catch (error) {
      wx.showToast({ title: '获取分析失败', icon: 'none' });
      console.error('获取分析失败:', error);
    } finally {
      wx.hideLoading();
    }
  }
});