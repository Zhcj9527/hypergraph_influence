import Vue from 'vue'//导入vue构造函数
import App from './App.vue'//导入根组件App.vue
import axios from "./http.js"
import * as bootstrap from 'bootstrap'
import '../node_modules/jquery/dist/jquery.js'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/bootstrap/dist/js/bootstrap.js'
import '../node_modules/bootstrap-select/dist/css/bootstrap-select.min.css'
import '../node_modules/bootstrap-select/dist/js/bootstrap-select.min.js'
import '../node_modules/ion-rangeslider/js/ion.rangeSlider.js'
import '../node_modules/ion-rangeslider/css/ion.rangeSlider.css'

// import './assets/css/dashboard.css'
import './assets/css/main.css'

Vue.config.productionTip = false
//配置axios和bus，便于前后端发送消息请求
Vue.prototype.$axios = axios//给Vue函数添加一个原型属性$axios 指向Axios
//这样做的好处是在vue实例或组件中不用再去重复引用Axios 直接用this.$axios就能执行axios 方法了
Vue.prototype.$bus = new Vue()//非父子组件的通信 ，两个组件通信，这个集中式的事件中间件就是 Bus
Vue.use(bootstrap)


new Vue({
  render: h => h(App),
}).$mount('#app')//render 函数得到这个 VNode 节点之后，返回给 Vue.js 的 mount 函数，渲染成真实 DOM 节点，并挂载到根节点上
