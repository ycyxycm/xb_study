<template>
  <el-container  style="height: 1261px; border: 1px solid #eee">
    <el-header height="60px" style="text-align: right; font-size: 16px;background-color: rgb(85,92,100)">
      <span>{{User_email}}</span>
      <span>{{User_name}}</span>
      <el-dropdown>
        <span class="el-dropdown-link">
<!--          <el-avatar :src="User_face"></el-avatar>-->
          <div class="block" style="margin-top: 10px">
            <el-badge :value="10" class="item">
              <el-avatar shape="square" :size="42" :src="User_face"></el-avatar>
            </el-badge>

          </div>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>{{User_name}}</el-dropdown-item>
          <el-dropdown-item>{{User_email}}</el-dropdown-item>
          <el-dropdown-item>螺蛳粉</el-dropdown-item>
          <el-dropdown-item disabled>双皮奶</el-dropdown-item>
          <el-dropdown-item divided>安全退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </el-header>
  <el-container style="height: 100%">
    <el-aside width="200px" style="background-color: rgb(85, 92, 100)">
      <!--        导航侧栏-->
      <el-row  class="tac">
        <el-col :span="24">
          <el-menu
            :router="true"
            default-active="2"
            class="el-menu-vertical-demo"
            @open="handleOpen"
            @close="handleClose"
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-location"></i>
                <span>财务</span>
              </template>
                <el-menu-item index="/home/dy_content">抖音日报表</el-menu-item>
                <el-menu-item index="/home/pdd_content">拼多多日报表</el-menu-item>
                <el-menu-item index="/home/finace_content">成本价/吊牌价</el-menu-item>
            </el-submenu>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-menu"></i>
                <span>聚水潭</span>
              </template>
                <el-menu-item index="/erp/changefd">福袋替换</el-menu-item>
                <el-menu-item index="2-2">选项2</el-menu-item>
            </el-submenu>
            <el-menu-item index="3" disabled>
              <i class="el-icon-document"></i>
              <span slot="title">导航三</span>
            </el-menu-item>
            <el-menu-item index="4">
              <i class="el-icon-setting"></i>
              <span slot="title">导航四</span>
            </el-menu-item>
          </el-menu>
        </el-col>
      </el-row>
      <!--        导航侧栏-->
    </el-aside>

      <el-main>
        <router-view></router-view>
      </el-main>

    </el-container>
  </el-container>
</template>
<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}
.el-aside {
  color: #333;
}
.el-dropdown-link {
 cursor: pointer;
 color: #409EFF;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>

<script>
import myfunction from "../utils/myfunction";
import api from "../utils/api";
import {request} from "../utils/request";

export default {
  data(){
    return{
      // User_email:this.$route.params.User_email,
      // User_name:this.$route.params.User_name,
      // User_face:this.$route.params.User_face,
      // User_erp_cookies:this.$route.params.User_erp_cookies
      User_email:null,
      User_name:null,
      User_face:null,
      User_erp_cookies:null
    }
  },
  mounted() {
    //获取用户信息
    this.get_user_info()

  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    log(...args){
      window.console.log(...args)
    },
    get_user_info(){
      request.post(api.http+"/check/session").then(res => {
        if(res.data.status==200){
          var usobj=res.data.data
          this.User_name=usobj.User_name
          this.User_email=usobj.User_email
          this.User_face=api.http+usobj.User_face
          this.User_erp_cookies=usobj.User_erp_cookies
        }
      });
    },

  }
}
</script>
<style scoped>

</style>
