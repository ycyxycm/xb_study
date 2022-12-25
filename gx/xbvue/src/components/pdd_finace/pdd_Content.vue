
<template>
  <div>
  <template>
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="店铺" style="width: 100%">
        <el-col :span="4">
          <el-select
            v-model="shop_value2"
            multiple
            collapse-tags
            style="margin-left: 20px;width: 280px"
            placeholder="请选择">
            <el-option
              v-for="item in shop_options"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="3">
          <el-date-picker type="date" :clearable="false" :editable='false' placeholder="开始日期" v-model="form.start_time" style="width:200px"></el-date-picker>
        </el-col>
        <el-col class="line" :span="1">-</el-col>
        <el-col :span="3">
          <el-date-picker type="date" :clearable="false" :editable='false' placeholder="结束日期" v-model="form.end_time" style="width:200px"></el-date-picker>
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="initData">搜索</el-button>
        </el-col>
        <el-col :span="11">
<!--          <span class="el-icon-s-order" style="font-size: 20px">导出:</span>-->
<!--          <el-select v-model="exportselect" clearable placeholder="请选择需要导出的表格" @change="selectonchange">-->
<!--            <el-option-->
<!--              v-for="item in options"-->
<!--              :key="item"-->
<!--              :label="item"-->
<!--              :value="item"-->
<!--            >-->
<!--            </el-option>-->
<!--          </el-select>-->
        </el-col>
      </el-form-item>
    </el-form>
  </template>
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
    <el-tab-pane label="店长数据截图" name="first">
      <pdd_survey :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="付费推广明细" name="six">
      <pdd_pay-detail :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="平台扣费明细" name="seven">
      <pdd_plat-detail :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="客服费用明细" name="eight">
      <pdd_kf-detail :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="活动费用明细" name="nine">
      <pdd_activity-detail :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="店铺占比" name="ten">
      <pdd_shop-ratio :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="退款率" name="sixteen">
      <pdd_refund-rate :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="1.0汇总" name="eleven">
      <pdd_10count :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="1.1汇总" name="twelve">
      <pdd_11count :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="1.1每日数据" name="fourteen">
      <pdd_11daily-data :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="1.0每日数据" name="fifteen">
      <pdd_10daily-data :data_all="i_pdd_count_Data" :table_status="i_pdd_count_Status"/>
    </el-tab-pane>

    <el-tab-pane label="主题分析+平台成交退款" name="second">
      <pdd_sales :data_all="i_pdd_sales_Data" :table_status="i_pdd_sales_Status"/>
    </el-tab-pane>

    <el-tab-pane label="店铺款式发退货" name="third">
      <pdd_sendcost :data_all="i_pdd_sendcost_Data" :table_status="i_pdd_sendcost_Status"/>
    </el-tab-pane>

    <el-tab-pane label="日常记账" name="five">
      <pdd_record :data_all="i_pdd_day_record_Data" :table_status="i_pdd_day_record_Status"/>
    </el-tab-pane>

    <el-tab-pane label="other" name="thirteen">
      <pdd_other/>
    </el-tab-pane>
  </el-tabs>
  </div>
</template>
<script>
import pdd_record from "./pdd_record";
import pdd_survey from './pdd_Survey.vue'
import pdd_sales from './pdd_sales.vue'
import pdd_sendcost from "./pdd_sendcost";
import pdd_other from "./pdd_other";

import pdd_activityDetail from "./pdd_activityDetail";
import pdd_kfDetail from "./pdd_kfDetail";
import pdd_payDetail from "./pdd_payDetail";
import pdd_platDetail from "./pdd_platDetail";
import pdd_11count from "./pdd_1.1count";
import pdd_10count from "./pdd_1.0count";
import pdd_shopRatio from "./pdd_shopRatio";
import pdd_10dailyData from "./pdd_1.0dailyData";
import pdd_11dailyData from "./pdd_1.1dailyData";
import pdd_refundRate from "./pdd_refundRate";

import myfunction from '@/utils/myfunction'
import {request} from "../../utils/request";
import api from "../../utils/api";
import moment from "moment";
import Pdd_refundRate from "./pdd_refundRate";


export default {
  data() {
    return {
      i_pdd_sendcost_Data:[],
      i_pdd_sendcost_Status:true,

      i_pdd_sales_Data:[],
      i_pdd_sales_Status:true,

      i_pdd_ztplat_Data:[],
      i_pdd_ztplat_Status:true,

      i_pdd_day_record_Data:[],
      i_pdd_day_record_Status:true,

      i_pdd_count_Data:[],
      i_pdd_count_Status:true,

      activeName: 'first',
      form: {
        shop: [],
        start_time: null,
        end_time: null
      },
      shop_options:[],
      shop_value2:[],
      // options:['1.1每日数据','1.0每日数据','店铺占比','付费推广明细','平台扣费明细','客服费用明细','活动费用明细','主题分析+平台数据','店铺款式发退货','日常记账'],//多级选择框 下拉列表的值
      value2: [],//多级选择框 选择的值
      exportselect:'',

    };
  },
  mounted() {
    myfunction.check_session(this)
    this.form.start_time=this.getAgoDay(2)
    this.form.end_time=this.getAgoDay(2)
    this.initData()
  },
  methods: {
    handleClick(tab, event) {
      // console.log(tab, event);
    },
    getAgoDay(n){
      let date= new Date();
      let seperator = "-"
      let newDate = new Date(date.getTime() - n*24*60*60*1000);
      let year = newDate.getFullYear();
      let month = newDate.getMonth()+1;
      let day = newDate.getDate();
      return year.toString() + seperator + month.toString() + seperator + day.toString()
    },
    selectonchange(){
      // console.log(this.exportselect)
    },
    initData(){
      this.form.shop=this.shop_value2.join()
      if (this.form.start_time!=null){this.form.start_time=moment(this.form.start_time).format('YYYY-MM-DD')}
      if (this.form.end_time!=null){this.form.end_time=moment(this.form.end_time).format('YYYY-MM-DD')}
      if (this.form.start_time>this.form.end_time){
        this.$notify.error({
          title: '错误',
          message: "请选择正确得时间区间!"
        });
      }else {
        this.i_pdd_sendcost_Status=true
        this.i_pdd_ztplat_Status=true
        this.i_pdd_sales_Status=true
        this.i_pdd_day_record_Status=true
        this.i_pdd_count_Status=true

        //拼多多 店铺款式发退货
        request.get(api.http+"/pdd/sendcost",{params:this.form}).then(res => {
          if (res.data.status!=200){
            this.$notify.error({
              title: '错误',
              message: res.data.msg
            });
          }else {
            this.i_pdd_sendcost_Data=res.data.data
          }
          this.i_pdd_sendcost_Status=false
          console.log("拼多多 店铺款式发退货 数据获取成功!")
        });
        //拼多多 主题分析+平台数据
        request.get(api.http+"/pdd/sales",{params:this.form}).then(res => {
          if (res.data.status!=200){
            this.$notify.error({
              title: '错误',
              message: res.data.msg
            });
          }else{
            this.i_pdd_sales_Data=res.data.data
          }
          this.i_pdd_sales_Status=false
          console.log("拼多多 主题分析+平台数据 数据获取成功!")
        });
        //拼多多 日常记账
        request.get(api.http+"/pdd/record",{params:this.form}).then(res => {
          if (res.data.status!=200){
            this.$notify.error({
              title: '错误',
              message: res.data.msg
            });
          }else{
            this.i_pdd_day_record_Data=res.data.data
          }
          this.i_pdd_day_record_Status=false
          console.log("拼多多 日常记账 数据获取成功!")
        });
        //拼多多 汇总
        request.post(api.http+'/pdd/generate',{'start_time':this.form.start_time,'end_time':this.form.end_time,'shop':this.shop_value2}).then(res=>{
          if (res.data.status!=200){
            this.$notify.error({
              title: '错误',
              message: res.data.msg
            });
          }else{
            this.i_pdd_count_Data=res.data.data
          }
          this.i_pdd_count_Status=false
          console.log("拼多多 汇总 数据获取成功!")
        })
        //拼多多 所有店铺
        request.get(api.http+'/pdd/shops').then(res=>{
          if (res.data.status!=200){
            this.$notify.error({
              title: '错误',
              message: res.data.msg
            });
          }else{
            this.shop_options=res.data.data
          }
          console.log("拼多多 所有店铺名 数据获取成功!")
        })
      }
    }
  },
  components:{
    Pdd_refundRate,
    pdd_survey,
    pdd_sales,
    pdd_sendcost,
    pdd_other,
    pdd_record,
    pdd_payDetail,
    pdd_platDetail,
    pdd_kfDetail,
    pdd_activityDetail,
    pdd_11count,
    pdd_10count,
    pdd_shopRatio,
    pdd_11dailyData,
    pdd_10dailyData
  }
};
</script>
