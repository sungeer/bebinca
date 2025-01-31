import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// 导入布局组件
import Layout from '@/views/layout'
//定义路由表
export const constantRoutes = [
    {
    path: '/',
    component: Layout,
    redirect: '/person',
    children: [
      {
        path: 'yuyuecode',
        component: () => import('@/views/yuyuecode'),
        name: 'yuyuecode',
        meta: { title: '预约二维码', icon: 'el-icon-s-grid'}
      },
      {
        path: 'person',   // 预约查询页面
        component: () => import('@/views/person'),
        name: 'person',
        meta: { title: '预约信息查询', icon: 'dashboard'}
      },
      {
        path: 'dengjicode',
        component: () => import('@/views/dengjicode'),
        name: 'dengjicode',
        meta: { title: '登记二维码', icon: 'dashboard'}
      },
      {
        path: 'checkin',  //登记查询页面
        component: () => import('@/views/checkin'),
        name: 'checkin',
        meta: { title: '登记信息查询', icon: 'dashboard'}
      },
      // {
      //   path: '404',      
      //   component: () => import('@/views/404')
      // }
      ]
    },
    {
      path: '/login',  //登录页面
      component: () => import('@/views/login')
    },
    // { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new VueRouter({
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

// 创建路由实例
const router = createRouter()  

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
