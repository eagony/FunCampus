// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

// 导入element ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

// 导入moment.js用于格式化UTC时间为本地时间
import moment from 'moment'
// 挂载
moment.locale('zh-cn')
Vue.prototype.$moment = moment

// 导入配置了全局拦截器后的axios
import axios from './http.js'
Vue.prototype.$axios = axios

// Sweetalert2
import Swal from 'sweetalert2'
Vue.prototype.$swal = Swal

// ApexCharts
// import ApexCharts from 'apexcharts'
// Vue.use(ApexCharts)
import VueApexCharts from 'vue-apexcharts'
Vue.component('apexchart', VueApexCharts)

// 导入bootstrap
import 'jquery'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'

// 自定义CSS
import './assets/core.css'
import './assets/custom.css'


// 图标
import './assets/icon-line/css/simple-line-icons.css' 
import './assets/icon-awesome/css/font-awesome.css'
import './assets/icon-material/material-icons.css'


Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
