import axios from 'axios'

// 创建Axios实例
const request = axios.create({
  timeout: 5000, // 单次请求的超时设置
  baseURL: process.env.VUE_APP_BASE_API, // 设置服务器地址
  // withCredentials: true, 
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 获取认证信息
    var token = window.sessionStorage.getItem('Authorization')
    if (token) {
      // 设置全局的请求头，用于接入OAuth2认证
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  error => {
    // 报错时，在控制台打印错误信息
    console.log('req',error) 
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    // 此处可以添加全局响应数据的处理代码，比如对自定义响应状态码的处理
    return res
  },
  error => {
     // 报错时，在控制台打印错误信息
    console.log('err', error)
    return Promise.reject(error)
  }
)

export default request
