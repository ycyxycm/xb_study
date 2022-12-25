<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_主题分析+平台成交退款"
      name="PDD_主题分析+平台成交退款.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" height="1000" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="120"></el-table-column>
        <el-table-column prop="deal_price" label="成交金额" :formatter="matter" v-if="lists[0].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.deal_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="refund_price" label="退款金额" :formatter="matter" v-if="lists[1].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.refund_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="dd_scene" label="多多场景" :formatter="matter" v-if="lists[2].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.dd_scene|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="dd_search" label="多多搜索" :formatter="matter" v-if="lists[3].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.dd_search|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="fxt" label="放心推" :formatter="matter" v-if="lists[4].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.fxt|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="qztg" label="全站推广" :formatter="matter" v-if="lists[5].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.qztg|filterNumber}}</p>
          </template>
        </el-table-column>

        <el-table-column prop="budan_price" label="补单金额" :formatter="matter" v-if="lists[6].ispass">
<!--          <template slot-scope="ins">-->
<!--            <el-input size="small" v-model="ins.row.budan_price" @keyup.enter.native="modify_budan(ins.row.budan_price,ins.row.id,ins.$index)"></el-input>-->
<!--          </template>-->
          <template slot-scope="scope">
            <p>{{scope.row.budan_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="today_male_tag" label="此店当天男吊牌价" :formatter="matter" v-if="lists[7].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.today_male_tag|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="today_female_tag" label="此店当天女吊牌价" :formatter="matter" v-if="lists[8].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.today_female_tag|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="today_child_tag" label="此店当天童吊牌价" :formatter="matter" v-if="lists[9].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.today_child_tag|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="shop_number" label="销售数总额" :formatter="matter" v-if="lists[10].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.shop_number|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="refund_number" label="实退数量" v-if="lists[11].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.refund_number|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="cost_count" label="成本总额" :formatter="matter" v-if="lists[12].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.cost_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="tag_count" label="吊牌费总额" :formatter="matter" v-if="lists[13].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.tag_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="refund_tag_count" label="吊牌费返还" :formatter="matter" v-if="lists[14].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.refund_tag_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="sendgoods_number" label="原始线上订单数" v-if="lists[15].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.sendgoods_number|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="express_price" label="快递费" :formatter="matter" v-if="lists[16].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.express_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="deliver_price" label="发货费" v-if="lists[17].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.deliver_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="budan_express_price" label="补单快递费" :formatter="matter" v-if="lists[18].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.budan_express_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="budan_deliver_price" label="补单发货费" v-if="lists[19].ispass">
          <template slot-scope="scope">
            <p>{{scope.row.budan_deliver_price|filterNumber}}</p>
          </template>
        </el-table-column>

      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="query.pageNum"
        :page-sizes="[5, 10, 15, 20,50,100]"
        :page-size="query.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="data_all.length"
      ></el-pagination>
    </el-card>
  </div>
</template>
<script>
import { request } from "@/utils/request";
import moment from "moment";
import api from '@/utils/api'
import myfunction from '@/utils/myfunction'

export default {
  props:{
    data_all:Array,
    table_status:Boolean,
    required:true
  },
  data() {
    return {
      json_fields:{
        "店铺":"shop","日期":"now_date",
        "成交金额":"deal_price","退款金额":"refund_price",
        "多多场景":"dd_scene","多多搜索":"dd_search",
        "放心推":"fxt","全站推广":"qztg",
        "补单金额":"budan_price","此店当天男吊牌价":"today_male_tag",
        "此店当天女吊牌价":"today_female_tag","此店当天童吊牌价":"today_child_tag",
        "销售数总额":"shop_number","实退数量":"refund_number",
        "成本总额":"cost_count","吊牌费总额":"tag_count",
        "吊牌费返还":"refund_tag_count","原始线上订单数":"sendgoods_number",
        "快递费":"express_price","发货费":"deliver_price",
        "补单快递费":"budan_express_price","补单发货费":"budan_deliver_price",
      },
      //分页数据
      query: {
        pageNum: 1,
        pageSize: 20,
        total: 0
      },
      check:['成交金额','退款金额','多多场景','多多搜索','放心推','全站推广','补单金额','此店当天男吊牌费','此店当天女吊牌费'
        ,'此店当天童吊牌费','销售数总额','实退数量','成本总额','吊牌费总额','吊牌费返还','原始线上订单数','快递费','发货费','补单快递费','补单发货费'],
      checkList: ['成交金额','退款金额','多多场景','多多搜索','放心推','全站推广','补单金额','此店当天男吊牌费','此店当天女吊牌费'
        ,'此店当天童吊牌费','销售数总额','实退数量','成本总额','吊牌费总额','吊牌费返还','原始线上订单数','快递费','发货费','补单快递费','补单发货费'],
      lists:[
        {label:'成交金额',ispass:true},
        {label:'退款金额',ispass:true},
        {label:'多多场景',ispass:true},
        {label:'多多搜索',ispass:true},
        {label:'放心推',ispass:true},
        {label:'全站推广',ispass:true},
        {label:'补单金额',ispass:true},
        {label:'此店当天男吊牌费',ispass:true},
        {label:'此店当天女吊牌费',ispass:true},
        {label:'此店当天童吊牌费',ispass:true},
        {label:'销售数总额',ispass:true},
        {label:'实退数量',ispass:true},
        {label:'成本总额',ispass:true},
        {label:'吊牌费总额',ispass:true},
        {label:'吊牌费返还',ispass:true},
        {label:'原始线上订单数',ispass:true},
        {label:'快递费',ispass:true},
        {label:'发货费',ispass:true},
        {label:'补单快递费',ispass:true},
        {label:'补单发货费',ispass:true},
      ]
    };
  },
  filters:{
    filterNumber:(val)=>{
      if(val===0||val==="0"){
        return "--"
      }else {
        return String(val).replace(/\B(?=(\d{3})+(?!\d))/g,',');
      }
    }
  },
  computed: {
    //table 表数据
    tableData() {
      const { pageNum, pageSize } = this.query;
      return this.data_all.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    }
  },
  mounted() {
  },
  methods: {
    //切换当前页显示的数据条数，执行方法
    handleSizeChange(val) {
      this.query.pageSize = val;
      this.query.pageNum = 1;
    },
    //切换页数，执行方法
    handleCurrentChange(val) {
      this.query.pageNum = val;
    },
    // modify_budan(val,id,col){
    //   request.put(api.http+"/pdd/sales/"+id,{"budan":val}).then(res => {
    //     if (res.data.status!=200){
    //       this.$message.error(res.data.msg);
    //     }else {
    //       this.data[col]=res.data.data
    //       this.$set(this.data,col,res.data.data)
    //       this.$message({
    //         message:id+":修改推广费用"+res.data.msg,
    //         type: 'success'
    //       })
    //     }
    //     this.loading=false
    //   });
    // },
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
    },
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
    },
    watch:{
      table_status(newV,oldV){
        this.table_status=newV
        // console.log(this.table_status)
      },
      data_all(newV,oldV){
        this.data_all=newV
        // console.log(this.data_all.length)
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
