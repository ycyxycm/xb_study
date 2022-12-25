<template>
  <div class="wrap">
    <el-card>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="店铺" style="width: 100%">
          <el-col :span="5">
            <el-select
              v-model="value2"
              multiple
              collapse-tags
              style="margin-left: 10px;width: 280px"
              placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item"
                :label="item"
                :value="item">
              </el-option>
            </el-select>
          </el-col>
          <el-col class="line" :span="1">-</el-col>
          <el-col :span="5">
            <el-date-picker type="date" :editable='false' placeholder="开始日期" v-model="form.start_time" style="width:200px"></el-date-picker>
          </el-col>
          <el-col class="line" :span="1">-</el-col>
          <el-col :span="5">
            <el-date-picker type="date" :editable='false' placeholder="结束日期" v-model="form.end_time" style="width:200px"></el-date-picker>
          </el-col>
          <el-col :span="2">
            <el-button type="primary" @click="onSubmit">搜索</el-button>
          </el-col>
          <el-col :span="2">
            <download-excel
              class="export-excel-wrapper"
              :data=this.data
              :fields="json_fields"
              type="xls"
              worksheet="My Worksheet"
              name="抖音日报发货退货明细"
            >
              <el-button type="success">导出EXCEL</el-button>
            </download-excel>
          </el-col>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}" :cell-style="{padding:'4px'}">
        <el-table-column fixed prop="shop" label="店铺" width="205"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="100"></el-table-column>
        <el-table-column prop="stylecode" label="款式编码"></el-table-column>
        <el-table-column prop="send_number" label="发货数量"></el-table-column>
        <el-table-column prop="refund_number" label="退货数量"></el-table-column>
        <el-table-column prop="today_price" label="当天成本价"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="query.pageNum"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="query.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="data.length"
      ></el-pagination>
    </el-card>
  </div>
</template>
<script>
import { request } from "@/utils/request";
import moment from "moment";
import api from '@/utils/api'
const _ =require('lodash')

export default {
  data() {
    return {
      data: [],
      //分页数据
      query: {
        pageNum: 1,
        pageSize: 15,
        total: 0
      },
      loading:true,
      form: {
        shop: null,
        start_time: null,
        end_time: null
      },
      json_fields: {
        店铺: "shop", //常规字段
        日期: "now_date", //支持嵌套属性
        款式编码:"stylecode",
        发货数量:"send_number",
        退货数量:"refund_number",
        当天成本价:"today_price",
      },
      options: [],//多级选择框 下拉列表的值
      value2: [],//多级选择框 选择的值
    };
  },
  computed: {
    //table 表数据
    tableData() {
      const { pageNum, pageSize } = this.query;
      return this.data.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    }
  },
  mounted() {
    this.getData();
  },
  methods: {
    requestData() {
      return request.get(api.http+"/dy/sendcost").then(res => {
        if (res.data.status!=200){
          this.$notify.error({
            title: '错误',
            message: res.data.msg
          });
        }
        this.loading=false
        return res.data.data;
      });
    },
    getData() {
      this.requestData().then(data => {
        this.data = data;
        //渲染下拉列表
        let temp_set=new Set()
        this.data.forEach(function (item,index) {
          temp_set.add(item.shop)
        })
        this.options=Array.from(temp_set)
      });
    },
    //切换当前页显示的数据条数，执行方法
    handleSizeChange(val) {
      this.query.pageSize = val;
      this.query.pageNum = 1;
    },
    //切换页数，执行方法
    handleCurrentChange(val) {
      this.query.pageNum = val;
    },
    onSubmit() {
      this.form.shop=this.value2.join()
      if (this.form.start_time!=null){this.form.start_time=moment(this.form.start_time).format('YYYY-MM-DD')}
      if (this.form.end_time!=null){this.form.end_time=moment(this.form.end_time).format('YYYY-MM-DD')}
      this.loading=true
      return request.get(api.http+"/dy/sendcost",{params:this.form}).then(res => {
        if (res.data.status!=200){
          this.$notify.error({
            title: '错误',
            message: res.data.msg
          });
        }else {
          this.data=res.data.data
        }
        this.loading=false
      });

    },
  }
};
</script>
<style scoped>
.wrap {
  width: 100%;
  height: 100%;
}
.el-pagination {
  margin-top: 15px;
}
body {
  margin: 0;
}
</style>
