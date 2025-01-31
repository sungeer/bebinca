// 导入前端库
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import moment from 'moment'
import router from './router'

const whiteList = ['/login']

// 定义路由守卫，未登录时，跳转到登录页面
router.beforeEach(async(to, from, next) => { 
    const hasToken = window.sessionStorage.getItem('Authorization') 
    // console.log(hasToken)
    if (hasToken) {
        if (to.path === '/login') {
          next({ path: '/' })
        } else {
            next()
        }
    } else {
        if (whiteList.indexOf(to.path) !== -1) {
            next()
          } else {
            next('/login')
          }
    }
})

// 初始化Vue设置
Vue.config.productionTip = false
Vue.prototype.$moment = moment

// 启用ElemenuUI框架
Vue.use(ElementUI);

// 创建Vue应用实例
new Vue({
    el: '#app',
    router: router,
    render: h => h(App),

})

