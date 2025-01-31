import request from '@/request'
import qs from 'qs'

// 登录函数
export function login(data) {
    return request({
      url: '/auth/login',
      method: 'post',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: qs.stringify(data)
    })
  }

// 获取预约信息列表函数
export function getPersonList(params) {
    return request({
        method: 'get',
        url: '/person/list',
        params
    })
}

// 获取登记信息列表函数
export function getCheckInList(params) {
    return request({
        method: 'get',
        url: '/checkin/list',
        params
    })
}
