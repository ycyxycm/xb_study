<template>
  <el-tabs class="login_el-tabs" type="border-card" style="height: 370px;width: 400px">
    <el-tab-pane label="登陆">
      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="邮箱:" prop="User_email">
          <el-input type="text" v-model="ruleForm.User_email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码:" prop="User_password">
          <el-input type="password" v-model="ruleForm.User_password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">登陆</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
    <el-tab-pane label="注册"><Register/></el-tab-pane>
  </el-tabs>
</template>
<script>
import Register from "./Register";
import api from "../utils/api";
import {request} from "../utils/request";

export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      }else if(value.length>16){
        callback(new Error('密码不能超过16个字符'));
      }else {
        callback();
      }
    };
    var checkEmail = (rule, value, callback) => {
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }else if(value.length>30){
        callback(new Error('邮箱不能超过30个字符'));
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }

    return {
      ruleForm: {
        User_email:'',
        User_password: '',
      },
      rules: {
        User_password: [
          { validator: validatePass, trigger: 'blur' }
        ],
        User_email: [
          {validator:checkEmail,trigger:'blur'}
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          request.post(api.http+'/login',this.ruleForm).then(res=>{
            if (res.data.status!=200){
              this.$message.error(res.data.msg);
              this.ruleForm.User_password=""
            }else{
              this.$message({
                message: res.data.msg,
                type: 'success'
              });
              // this.$router.push('/home')
              //带参数跳转
              // this.$router.push({name:'home',params:res.data.data});
              this.$router.push({name:'home'});

              // this.$router.push({name:'testDemo',params:{setid:111222}});
            }
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  },
  components:{
    Register
  }
}
</script>
<style>
.login_el-tabs{
  flex-direction: column;
  margin: 0 !important;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
