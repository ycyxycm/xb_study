
import Vue from 'vue'
import App from './App'
import router from "./router";
import '@/style/css/dy_sales.css'
import adaptive from "./utils/adaptive";
// import './style/css/dy_sales.css'

//导入ElementUI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import JsonExcel from 'vue-json-excel'

Vue.config.productionTip = false
Vue.use(adaptive)
Vue.use(ElementUI)
Vue.component('downloadExcel', JsonExcel)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  //配置路由
  router,
  render: h => h(App)
})
