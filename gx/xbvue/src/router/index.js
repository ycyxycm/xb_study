import Vue from 'vue'
import VueRouter from "vue-router";
import Content from "../components/dy_finace/dy_Survey";
import Home from '../components/Home';
import Login from "../components/Login";

import Dy_Content from "../components/dy_finace/dy_Content";
import Pdd_Content from "../components/pdd_finace/pdd_Content";
import finace_Content from "../components/finace_cost_tag/finace_Content";

import erp_changefd from "../components/erp_tool/erp_changefd";
import api from "../utils/api";
import {request} from "../utils/request";

//安装路由
Vue.use(VueRouter)

//配置路由导出
const myrouter = new VueRouter({
  routes:[
    //登录页面
    {
      //路由路径
      path:'',
      //路由名
      name:'index',
      //跳转的组件
      component:Login
    },
    //登录页面
    {
      //路由路径
      path:'/login',
      //路由名
      name:'login',
      //跳转的组件
      component:Login
    },
    //headers tool
    {
      //路由路径
      path:'/home',
      //路由名
      name:'home',
      //跳转的组件
      component:Home,
      children:[
        {path:'/home/dy_content',component:Dy_Content},
        {path:'/home/pdd_content',component:Pdd_Content},
        {path:'/erp/changefd',component:erp_changefd},
        {path:'/home/finace_content',component:finace_Content},
      ]
    },
  ]
})
myrouter.beforeEach((to,from,next)=>{
  if (to.name!='login'){
    request.get(api.http+"/check/session").then(res => {
      if(to.name!='login'&&res.data.status==-1){
        alert(res.data.msg)
        next({name:'login'})
      }else {
        next()
      }
    });
  }else{
    next()
  }

})
export default myrouter;
