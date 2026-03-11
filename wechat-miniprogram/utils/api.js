// utils/api.js

const baseUrl = 'http://localhost:5000'; // 后端API地址

// 发起请求
function request(url, method, data) {
  const token = getApp().globalData.token;
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl + url,
      method: method,
      data: data,
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: res => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          // 未授权，跳转到登录页
          wx.redirectTo({ url: '/pages/login/login' });
          reject(res.data);
        } else {
          reject(res.data);
        }
      },
      fail: err => {
        reject(err);
      }
    });
  });
}

// 登录
const login = (data) => request('/auth/login', 'POST', data);

// 考勤相关
const attendanceApi = {
  getList: (params) => request('/attendance', 'GET', params)
};

// 作业相关
const homeworkApi = {
  getList: (params) => request('/homework', 'GET', params)
};

// 成绩相关
const scoreApi = {
  getList: (params) => request('/scores', 'GET', params)
};

// 餐饮相关
const mealApi = {
  getList: (params) => request('/meals', 'GET', params)
};

// AI分析相关
const aiAnalysisApi = {
  getList: (params) => request('/ai-analysis', 'GET', params)
};

module.exports = {
  login,
  attendanceApi,
  homeworkApi,
  scoreApi,
  mealApi,
  aiAnalysisApi
};