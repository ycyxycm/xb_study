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
            <el-col :span="3">
              <el-date-picker type="date" :editable='false' placeholder="开始日期" v-model="form.start_time" style="width:200px"></el-date-picker>
            </el-col>
            <el-col class="line" :span="1">-</el-col>
            <el-col :span="3">
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
                name="抖音日报汇总"
              >
                <el-button type="success">导出EXCEL</el-button>
              </download-excel>
            </el-col>
            <el-col :span="2">
              <el-button @click="drawer = true" type="primary" style="margin-left: 16px;">
                动态字段
              </el-button>
              <el-drawer
                title="动态列头"
                :visible.sync="drawer"
                :direction="direction"
                :before-close="handleClose">
                <template>
                  <el-checkbox-group v-model="check">
                    <el-dropdown-item v-for="(item,index) in checkList" :key="index">
                      <el-checkbox :label="item" :key="item"></el-checkbox>
                    </el-dropdown-item>
                  </el-checkbox-group>
                </template>
              </el-drawer>
            </el-col>
            <el-col :span="2">

            </el-col>
        </el-form-item>
      </el-form>
      <el-table v-loading="loading" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}" :cell-style="{padding:'4px'}">
        <el-table-column fixed prop="shop" label="店铺" width="205"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="100"></el-table-column>
        <el-table-column prop="deal_price" label="成交金额" :formatter="matter" v-if="lists[0].ispass"></el-table-column>
        <el-table-column prop="refund_price" label="退款金额" :formatter="matter" v-if="lists[1].ispass"></el-table-column>
        <el-table-column prop="budan_price" label="补单金额" :formatter="matter" v-if="lists[2].ispass"></el-table-column>
        <el-table-column prop="budan_yongjin" label="补单佣金" :formatter="matter" v-if="lists[3].ispass"></el-table-column>

        <el-table-column label="推广费用" :formatter="matter" v-if="lists[4].ispass">
          <template slot-scope="ins">
            <el-input size="mini" v-model="ins.row.extension_price" @keyup.enter.native="modify_ext(ins.row.extension_price,ins.row.id,ins.$index)"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="客服返现" :formatter="matter" v-if="lists[5].ispass">
          <template slot-scope="ins">
            <el-input size="mini" v-model="ins.row.kf_re_price" @keyup.enter.native="modify_kffx(ins.row.kf_re_price,ins.row.id)"></el-input>
          </template>
        </el-table-column>

        <el-table-column prop="refund_rate" label="退款率" v-if="lists[6].ispass"></el-table-column>
        <el-table-column prop="label_price" label="吊牌费" :formatter="matter" v-if="lists[7].ispass"></el-table-column>
        <el-table-column prop="net_sales" label="净销售额" :formatter="matter" v-if="lists[8].ispass"></el-table-column>
<!--        prop="plat_cost"-->
        <el-table-column label="平台花费" width="105" :formatter="matter" v-if="lists[9].ispass">
          <template slot-scope="ins">
            <el-popover
              placement="bottom"
              width="200"
              trigger="click">
              <div>
                服务费: {{ ins.row.ser_charge }}<br>
                运费险: {{ ins.row.freight }}<br>
                揽收超时: {{ ins.row.collect_timeout }}<br>
                发货超时: {{ ins.row.send_timeout }}<br>
                小额打款: {{ ins.row.small_pay }}<br>
                违规: {{ ins.row.violation }}<br>
                虚假发货超时: {{ ins.row.fake_send_timeout }}<br>
                达人带货佣金: {{ ins.row.daren_yongjin }}<br>
                营销费用划扣: {{ ins.row.marketing }}<br>
              </div>
              <el-button size="mini" style="width: 80px" slot="reference">{{ins.row.plat_cost}}</el-button>
            </el-popover>
          </template>
        </el-table-column>
<!--        平台花费明细-->
        <el-table-column label-class-name="dy_sales_table-row" prop="ser_charge" label="服务费" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="freight" label="运费险" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="send_timeout" label="发货超时" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="collect_timeout" label="揽收超时" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="fake_send_timeout" label="虚假发货超时" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="small_pay" label="小额打款" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="violation" label="违规" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="daren_yongjin" label="达人带货佣金" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
        <el-table-column label-class-name="dy_sales_table-row" prop="marketing" label="营销费用划扣" :formatter="matter" v-if="lists[17].ispass"></el-table-column>
<!--        平台花费明细-->

        <el-table-column prop="gpmo_sales" label="销售毛利率" v-if="lists[10].ispass"></el-table-column>
        <el-table-column prop="express_price" label="快递费用" :formatter="matter" v-if="lists[11].ispass"></el-table-column>
        <el-table-column prop="deliver_price" label="发货费用" :formatter="matter" v-if="lists[12].ispass"></el-table-column>
        <el-table-column prop="budan_express_price" label="补单快递费用" :formatter="matter" v-if="lists[18].ispass"></el-table-column>
        <el-table-column prop="budan_deliver_price" label="补单发货费用" :formatter="matter" v-if="lists[19].ispass"></el-table-column>
        <el-table-column prop="cbj_count" label="衣服成本" :formatter="matter" v-if="lists[13].ispass"></el-table-column>
        <el-table-column prop="gpm" label="毛利率" v-if="lists[14].ispass"></el-table-column>
        <el-table-column prop="profit_es" label="利润预估" :formatter="matter" v-if="lists[15].ispass"></el-table-column>
        <el-table-column prop="jmll" label="净毛利率" v-if="lists[16].ispass"></el-table-column>
        <!--        <el-table-column prop="address" label="地址"></el-table-column>-->
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
      loading:true,
      form: {
        shop: null,
        start_time: null,
        end_time: null
      },
      json_fields: {
        店铺: "shop", //常规字段
        日期: "now_date", //支持嵌套属性
        成交金额:"deal_price",
        退款金额:"refund_price",
        补单金额:"budan_price",
        补单佣金:"budan_yongjin",
        推广费用:"extension_price",
        客服返现:"kf_re_price",
        退款率:"refund_rate",
        吊牌费:"label_price",
        净销售额:"net_sales",
        平台花费:"plat_cost",
        销售毛利率:"gpmo_sales",
        快递费用:"express_price",
        发货费用:"deliver_price",
        补单快递费用:"budan_express_price",
        补单发货费用:"budan_deliver_price",
        衣服成本:"cbj_count",
        毛利率:"gpm",
        利润预估:"profit_es",
        净毛利率:"jmll",
        服务费:"ser_charge",
        运费险:"freight",
        揽收超时:"collect_timeout",
        发货超时:"send_timeout",
        小额打款:"small_pay",
        违规:"violation",
        虚假发货超时:"fake_send_timeout",
        达人带货佣金:"daren_yongjin",
        营销费用划扣:"marketing",

        // 密码: {
        // field: "info.phone",
        //   //自定义回调函数
        //   callback: value => {
        //   return `+86 ${value}`;
        // }
      },
      options: [],//多级选择框 下拉列表的值
      value2: [],//多级选择框 选择的值
      drawer: false,
      direction: 'btt',
      check:['成交金额','退款金额','补单金额','补单佣金','推广费用','客服返现','退款率','吊牌费'
        ,'净销售额','平台花费','销售毛利率','快递费用','发货费用','补单快递费用','补单发货费用','衣服成本','毛利率','利润预估','净毛利率'],
      checkList: ['平台花费明细','成交金额','退款金额','补单金额','补单佣金','推广费用','客服返现','退款率','吊牌费'
        ,'净销售额','平台花费','销售毛利率','快递费用','发货费用','补单快递费用','补单发货费用','衣服成本','毛利率','利润预估','净毛利率'],
      lists:[
        {label:'成交金额',ispass:true},
        {label:'退款金额',ispass:true},
        {label:'补单金额',ispass:true},
        {label:'补单佣金',ispass:true},
        {label:'推广费用',ispass:true},
        {label:'客服返现',ispass:true},
        {label:'退款率',ispass:true},
        {label:'吊牌费',ispass:true},
        {label:'净销售额',ispass:true},
        {label:'平台花费',ispass:true},
        {label:'销售毛利率',ispass:true},
        {label:'快递费用',ispass:true},
        {label:'发货费用',ispass:true},
        {label:'衣服成本',ispass:true},
        {label:'毛利率',ispass:true},
        {label:'利润预估',ispass:true},
        {label:'净毛利率',ispass:true},
        {label:'平台花费明细',ispass:false},
        {label:'补单快递费用',ispass:true},
        {label:'补单发货费用',ispass:true},
      ]
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
      return request.get(api.http+"/dy/sales").then(res => {
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
      return request.get(api.http+"/dy/sales",{params:this.form}).then(res => {
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
    modify_ext(val,id,col){
      request.put(api.http+"/dy/sales/"+id,{"extension_price":val}).then(res => {
        if (res.data.status!=200){
          this.$message.error(res.data.msg);
        }else {
          this.data[col]=res.data.data
          this.$set(this.data,col,res.data.data)
          this.$message({
            message:id+":修改推广费用"+res.data.msg,
            type: 'success'
          })
        }
        this.loading=false
      });
    },
    modify_kffx(val,id,col){
      request.put(api.http+"/dy/sales/"+id,{"kf_re_price":val}).then(res => {
        if (res.data.status!=200){
          this.$message.error(res.data.msg);
        }else {
          this.$message({
            message:id+":修改客服返现"+res.data.msg,
            type: 'success'
          })
          // <el-button :plain="true" @click="open2">成功</el-button>
        }
        this.loading=false
      });
    },
    log(...args){
      window.console.log(...args)
    },
    handleClose(done) {
      done();
    },
    matter(row, column, cellValue) {
      cellValue += ''
      if (!cellValue.includes('.')) cellValue += '.'
      return cellValue.replace(/(\d)(?=(\d{3})+\.)/g, function($0, $1) {
        return $1 + ','
      }).replace(/\.$/, '')
    }


  },
  watch:{
    check(newVal){
      if (newVal) {
        var arr = this.checkList.filter(i => newVal.indexOf(i) < 0) //未选中
        this.lists.map(i => {
          if (arr.indexOf(i.label) !== -1) {
            i.ispass = false
          } else {
            i.ispass = true
          }
        })
      }
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
