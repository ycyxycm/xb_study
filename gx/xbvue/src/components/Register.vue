<template>

      <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="姓名:" prop="User_name">
          <el-input type="text" v-model="ruleForm.User_name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱:" prop="User_email">
          <el-input type="text" v-model="ruleForm.User_email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码:" prop="User_password">
          <el-input type="password" v-model="ruleForm.User_password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="验证码:" prop="vcode">
          <el-input type="text" v-model="ruleForm.vcode" style="width: 100px" autocomplete="off"></el-input>
          <el-button type="success" @click="send_eamil()" icon="el-icon-message" :disabled="email_bt_status">{{ email_bt_outtime }}</el-button>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>
</template>
<script>
import Register from "./Register";
import {request} from "../utils/request";
import api from "@/utils/api";

export default {
  data() {
    var validateUser_name = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入姓名'));
      }else if(value.length>8){
        callback(new Error('姓名不能超过8个字符'));
      }
      else {
        callback();
      }
    };
    var validateUser_password = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      }else if(value.length>16){
        callback(new Error('密码不能超过16个字符'));
      } else {
        callback();
      }
    };
    var checkUser_email = (rule, value, callback) => {
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }else if(value.length>30){
        callback(new Error('邮箱不能超过30个字符'));
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          request.get(api.http+"/us/register/checkemail",{params:{'email':value}}).then(res=>{
            if (res.data.status!=200){
              return callback(new Error(res.data.msg))
            }else{
              return callback()
            }
          })
        } else {
          return callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)


    };
    var checkVcode = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('验证码不能为空'))
      }else {
        callback();
      }
    }
    return {
      email_bt_status:false,
      email_bt_outtime:"",
      ruleForm: {
        User_name:'',
        User_email:'',
        User_password: '',
      },
      rules: {
        User_password: [
          { validator: validateUser_password, trigger: 'blur' }
        ],
        User_email: [
          {validator:checkUser_email,trigger:'blur'}
        ],
        User_name: [
          {validator:validateUser_name,trigger:'blur'}
        ],
        vcode: [
          {validator:checkVcode,trigger:'blur'}
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          //注册验证通过
          request.post(api.http+'/user',this.ruleForm).then(res=>{
            if (res.data.status!=200){
              this.email_bt_status=false
              this.$message.error(res.data.msg);
            }else{
              this.$message({
                message: res.data.msg,
                type: 'success'
              });
              this.resetForm(formName)
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
    },
    send_eamil(){
      this.$refs['ruleForm'].validateField(['User_email'], (info)=>{
        if (!info) {
          this.email_bt_status=true
          //邮箱验证成功
          request.post(api.http+"/us/register/cemail",{'email':this.ruleForm.User_email}).then(res=>{
            if (res.data.status!=200){
              this.email_bt_status=false
              this.$message.error(res.data.msg);
            }else{
              this.$message({
                message: res.data.msg,
                type: 'success'
              });
              //按钮状态改变
              this.email_bt_outtime=15
              var countTime=setInterval(()=>{
                this.email_bt_outtime-=1
                if (this.email_bt_outtime<1){
                  clearInterval(countTime)
                  this.email_bt_status=false
                  this.email_bt_outtime=""
                }
              },1000)
            }
          })
        } else {
          this.$message.error(info);
          return false;
        }
      })

    }
  },
  components:{
    Register
  }
}
</script>
<style>
</style>
