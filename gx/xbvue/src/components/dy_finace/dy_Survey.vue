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
              style="margin-left: 20px;width: 280px"
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
            <el-date-picker type="date" :editable='false' placeholder="开始日期" v-model="form.start_date" style="width:200px"></el-date-picker>
          </el-col>
          <el-col class="line" :span="1">-</el-col>
          <el-col :span="5">
            <el-date-picker type="date" :editable='false' placeholder="结束日期" v-model="form.end_date" style="width:200px"></el-date-picker>
          </el-col>
          <el-col class="line" :span="1">-</el-col>
          <el-col :span="2">
            <el-button type="primary" @click="onSubmit">搜索</el-button>
          </el-col>
          <el-col :span="2">
            <download-excel
              class="export-excel-wrapper"
              :data="this.data"
              :fields="json_fields"
              type="xls"
              worksheet="My Worksheet"
              name="抖音日报概况"
            >
              <el-button type="success">导出EXCEL</el-button>
            </download-excel>
          </el-col>
        </el-form-item>
      </el-form>
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        style="width: 100%"
        :row-style="{height:'20px'}"
        :cell-style="{padding:'4px'}"
      >
        <el-table-column
          fixed
          prop="shop"
          label="店铺"
          width="205"
        ></el-table-column>
<!--        <el-table-column-->
<!--          fixed-->
<!--          prop="start_date"-->
<!--          label="日期"-->
<!--          width="100"-->
<!--        ></el-table-column>-->
        <el-table-column
          fixed
          prop="net_sales_sum"
          label="净销售额合计"
          :formatter="matter"
        ></el-table-column>
        <el-table-column
          fixed
          prop="profit_es_sum"
          label="利润预估合计"
          :formatter="matter"
        ></el-table-column>
        <el-table-column
          fixed
          prop="jmll_sum"
          label="净毛利率"
        ></el-table-column>
        <el-table-column

          v-for="item in dateInfo.interval"
          :key="item"
          :label="item"
        >
          <template v-slot="ins">
            <div>
              {{ findTrueItem(ins, item).su_profit || "0" }}
            </div>
          </template>
        </el-table-column>
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
      loading: false,
      form: {
        shop: null,
        start_date:null,
        end_date:null,
      },
      json_fields: {
        店铺: "shop", //常规字段
        日期: "start_date", //支持嵌套属性
        净销售额合计:"net_sales_sum",
        利润预估合计:"profit_es_sum",
        净毛利率:"jmll_sum",
      },
      options: [],//多级选择框 下拉列表的值
      value2: []//多级选择框 选择的值
    };
  },
  computed: {
    //table 表数据
    tableData() {
      const { pageNum, pageSize } = this.query;
      return this.data.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    },
    dateInfo() {
      const allDateInfo = this.data.flatMap(i =>
        i.profit_es_s.map(i => moment(i.su_nowdate).valueOf())
      );
      console.log(this.data)
      console.log(allDateInfo)
      const maxDate = Math.max(...allDateInfo);
      const minDate = Math.min(...allDateInfo);
      const interval = moment(maxDate).diff(moment(minDate), "day");
      return {
        minDate: moment(minDate).format("MMMM-YY-DD"),
        maxDate: moment(maxDate).format("MMMM-YY-DD"),
        interval: Array.from({ length: interval+1 }, (_, i) => {
          return moment(minDate)
            .add(i, "day")
            .format("YYYY-MM-DD");
        })
      };
    }
  },
  mounted() {
    this.getData();
  },
  methods: {
    log(...args) {
      window.console.log(...args);
    },
    findTrueItem(item, key) {
      return item.row.profit_es_s.find(i => i.su_nowdate === key) || {};
    },
    requestData() {
      this.loading = true;
      return request.get(api.http+"/dy/survey").then(res => {
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
      if (this.form.start_date != null) {
        this.form.start_date = moment(this.form.start_date).format(
          "YYYY-MM-DD"
        );
      }
      if (this.form.end_date != null) {
        this.form.end_date = moment(this.form.end_date).format(
          "YYYY-MM-DD"
        );
      }
      this.loading = true;
      return request
        .get(api.http+"/dy/survey", { params: this.form })
        .then(res => {
          if (res.data.status != 200) {
            this.$notify.error({
            title: '错误',
            message: res.data.msg
          });;
          } else {
            this.data = res.data.data;
          }
          this.loading = false;
        });

    },
    matter(row, column, cellValue) {
      cellValue += ''
      if (!cellValue.includes('.')) cellValue += '.'
      return cellValue.replace(/(\d)(?=(\d{3})+\.)/g, function($0, $1) {
        return $1 + ','
      }).replace(/\.$/, '')
    }
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
