<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="搜索时间">
      <el-col :span="6">
        <el-date-picker :editable="false" :clearable="false" type="date" placeholder="选择日期" v-model="form.date" style="width: 70%;"></el-date-picker>
      </el-col>
      <el-col :span="6">
        <el-button type="primary" @click="onSubmit">查询</el-button>
      </el-col>
    </el-form-item>

  <div style="height: 500px;" v-loading="divLoading"  :element-loading-text="div_msg" element-loading-spinner="el-icon-loading" element-loading-background="rgb(0,0,0,0,)">
    <el-steps direction="vertical" :active="this.today_number">
      <el-step title="拼多多平台数据获取">
        <template slot="description">

          <span >主要获取拼多多店铺成交 退款 推广费用</span><br>
        </template>
      </el-step>
      <el-step title="拼多多ERP数据获取">
        <template slot="description">
          <span >主要获取拼多多ERP对应发退货以及订单数信息</span><br>
        </template>
      </el-step>
      <el-step title="拼多多 日常记账Excel导出">
        <template slot="description">
          <span >主要导出在拼多多日报表流程中需要导入聚水潭 日常记账 中需要的excel!</span><br>
          <div>
          <download-excel
            style="width: 56px"
            class="export-excel-wrapper"
            :data=json_data2
            :fields="json_fields2"
            type="xls"
            worksheet="My Worksheet"
            name="拼多多日常记账导入表"
            v-if="this.today_number>=2 ? true : false"
          >
            <el-button v-loading="export_erp_loading" type="success" size="small" @click="this.myexport" v-if="this.today_number>=2 ? true : false"> 导出</el-button>
          </download-excel>
          </div>

        </template>
      </el-step>
      <el-step title="拼多多 获取多维度数据(需要确保当天 日常记账 与 当天账单 已导入)">
        <template slot="description">
          <span>在聚水潭日常记账导入之后 会在多维度生成数据,此处为获取多维度数据,获取之后则会存入数据库以及生成数据汇总</span><br>
          <el-button type="success" size="small" :disabled="this.today_number==3 ? false : true" @click=this.get_dwd>获取</el-button>
        </template>
      </el-step>
      <el-step title="完成 数据生成">
        <template slot="description">
          <span>聚水潭日常记账后从多维度导出的数据</span><br>
        </template>
      </el-step>
    </el-steps>
  </div>
  </el-form>
</template>

<script>
import {request} from "../../utils/request";
import api from "../../utils/api";
import moment from "moment";

export default {
  data() {
    return {
      form: {
        date: '',
      },
      today_number:0,
      json_fields2: {
      店铺名称: "店铺名称", //常规字段
        发生日期: "发生日期", //支持嵌套属性
        利润表项目编码:"利润表项目编码",
        项目名称:"项目名称",
        金额:"金额"
      },
      json_data2:[],
      export_erp_loading:false,
      divLoading:false,
      div_msg:"数据加载中...."
      }

  },
  mounted() {
    this.getDate();
  },
  methods:{
    getDate(){
      //获取前天日期
      let tempDate = new Date() // 获取今天的日期
      tempDate.setDate(tempDate.getDate() - 2) // 今天的前N天的日期，N自定义
      let endDate = tempDate.getFullYear() + '-' + (tempDate.getMonth() + 1) + '-' + tempDate.getDate()
      this.form.date=endDate
      //日期获取后渲染当天页面情况
      this.onSubmit()
    },
    onSubmit() {
      this.divLoading=true
      if (this.form.date!=null){this.form.date=moment(this.form.date).format('YYYY-MM-DD')}
      request.get(api.http+"/pdd/dateStatus",{params:{date:this.form.date}}).then(res=>{
        if (res.data.status!=200){
          this.$notify.error({
            title: '错误',
            message: res.data.msg
          });
        }else {
          this.$message({
            message:res.data.msg+res.data.data,
            type:'success'
          });
          this.today_number=res.data.data
        }
      })
      //获取导出列表
      request.post(api.http+"/pdd/export",{"now_date":this.form.date}).then(res=>{
        if (res.data.status!=200){
          this.$message.error(res.data.msg);
          this.divLoading=false
        }else {
          this.json_data2=res.data.data
          this.divLoading=false
        }
      })

    },
    myexport(){
      //修改redis3号状态位
      request.get(api.http+"/pdd/upstatus",{params:{date:this.form.date}}).then(res=>{
        if (res.data.status!=200){
          this.$message.error(res.data.msg);
        }else {
          this.$message({
            message: "导出"+res.data.msg,
            type: 'success'
          });
          this.onSubmit()
        }
      })
    },
    get_dwd(){
      this.div_msg="多维度数据分析中,请稍等....."
      this.divLoading=true
      request.post(api.http+"/pdd/dwd_data",{"date":this.form.date}).then(res=>{
        if (res.data.status!=200){
          this.$alert(res.data.msg, '多维度数据生分析出错!', {
            confirmButtonText: '确定',
            callback: action => {
              this.$message({
                type: 'info',
                message: `action: ${ action }`
              });
            }
          });
          this.divLoading=false;
          this.onSubmit()
        }else {
          this.$alert(res.data.msg, '多维度数据生分析完成!', {
            confirmButtonText: '确定',
            callback: action => {
              this.$message({
                type: 'info',
                message: `action: ${ action }`
              });
            }
          });
          this.divLoading=false
          this.onSubmit()
        }
      })
      this.div_msg="数据加载中...."
    },
  },
  watch:{
  }
}
</script>

<style>
</style>
