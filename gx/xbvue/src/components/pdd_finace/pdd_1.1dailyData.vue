<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_1.0 每日数据"
      name="PDD_1.0 每日数据.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table
        v-loading="table_status"
        :data="tableData"
        height="1000"
        style="width: 100%"
        :row-style="{height:'20px'}"
        :cell-style="{padding:'4px'}"
      >
        <el-table-column fixed width="40px" type="expand">
          <template slot-scope="props">
            <el-table
              :data="props.row.items"
              :show-header="false"
              style="width: 100%"
              :row-style="{height:'20px'}"
              :cell-style="{padding:'4px'}">
              <el-table-column width="40px"></el-table-column>
              <el-table-column width="300px" prop="now_date"></el-table-column>
              <el-table-column label="成交金额" width="125px" prop="i_deal_money">
                <template slot-scope="scope">
                  <p>{{scope.row.i_deal_money|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column label="退款金额" width="125px" prop="i_refund_money">
                <template slot-scope="scope">
                  <p>{{scope.row.i_refund_money|filterNumber}}</p>
                </template>
              </el-table-column>

              <el-table-column label="发货前退款金额" width="125px" prop="i_refund_money">
                <template slot-scope="scope">
                  <p>{{scope.row.i_sendgoods_front_refund_money|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column label="发货后退款金额" width="125px" prop="i_refund_money">
                <template slot-scope="scope">
                  <p>{{scope.row.i_sendgoods_after_refund_money|filterNumber}}</p>
                </template>
              </el-table-column>

              <el-table-column prop="i_budan_money" width="125px" label="补单金额">
                <template slot-scope="scope">
                  <p>{{scope.row.i_budan_money|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_net_sale" width="125px" label="净销售额">
                <template slot-scope="scope">
                  <p>{{scope.row.i_net_sale|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_clothing_cost_11" width="125px" label="1.1衣服成本">
                <template slot-scope="scope">
                  <p>{{scope.row.i_clothing_cost_11|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_kuaidi_fee" width="125px" label="快递费用">
                <template slot-scope="scope">
                  <p>{{scope.row.i_kuaidi_fee|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_sendgoods_fee" width="125px" label="发货费用">
                <template slot-scope="scope">
                  <p>{{scope.row.i_sendgoods_fee|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_ml_11" width="125px" label="1.1毛利">
                <template slot-scope="scope">
                  <p>{{scope.row.i_ml_11|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_tg_pay_count" width="125px" label="付费推广合计">
                <template slot-scope="scope">
                  <p>{{scope.row.i_tg_pay_count|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_plat_fee_count" width="125px" label="平台扣费合计">
                <template slot-scope="scope">
                  <p>{{scope.row.i_plat_fee_count|filterNumber}}</p>
                </template>
              </el-table-column>

              <el-table-column prop="i_kf_fee_count" width="125px" label="客服费用合计">
                <template slot-scope="scope">
                  <p>{{scope.row.i_kf_fee_count|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_huodong_fee" width="125px" label="活动费用">
                <template slot-scope="scope">
                  <p>{{scope.row.i_huodong_fee|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_tag_fee" width="125px" label="吊牌费">
                <template slot-scope="scope">
                  <p>{{scope.row.i_tag_fee|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_net_ml_11" width="125px" label="1.1净毛利">
                <template slot-scope="scope">
                  <p>{{scope.row.i_net_ml_11|filterNumber}}</p>
                </template>
              </el-table-column>
              <el-table-column prop="i_net_ml_rate_11" width="125px" label="1.1净毛利率"></el-table-column>
              <el-table-column prop="i_refund_rate" width="125px" label="退款率"></el-table-column>
              <el-table-column prop="i_tg_pat_rate" width="125px" label="运营付费占比"></el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column fixed :show-overflow-tooltip="true" label="店铺名称" width="300px" prop="shop"></el-table-column>
        <el-table-column label="成交金额" width="125px" prop="i_deal_money">
          <template slot-scope="scope">
            <p>{{scope.row.i_deal_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column label="退款金额" width="125px" prop="i_refund_money">
          <template slot-scope="scope">
            <p>{{scope.row.i_refund_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column label="发货前退款金额" width="125px" prop="i_refund_money">
          <template slot-scope="scope">
            <p>{{scope.row.i_sendgoods_front_refund_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column label="发货后退款金额" width="125px" prop="i_refund_money">
          <template slot-scope="scope">
            <p>{{scope.row.i_sendgoods_after_refund_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_budan_money" width="125px" label="补单金额">
          <template slot-scope="scope">
            <p>{{scope.row.i_budan_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_net_sale" width="125px" label="净销售额">
          <template slot-scope="scope">
            <p>{{scope.row.i_net_sale|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_clothing_cost_11" width="125px" label="1.1衣服成本">
          <template slot-scope="scope">
            <p>{{scope.row.i_clothing_cost_11|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_kuaidi_fee" width="125px" label="快递费用">
          <template slot-scope="scope">
            <p>{{scope.row.i_kuaidi_fee|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_sendgoods_fee" width="125px" label="发货费用">
          <template slot-scope="scope">
            <p>{{scope.row.i_sendgoods_fee|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_ml_11" width="125px" label="1.1毛利">
          <template slot-scope="scope">
            <p>{{scope.row.i_ml_11|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_tg_pay_count" width="125px" label="付费推广合计">
          <template slot-scope="scope">
            <p>{{scope.row.i_tg_pay_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_plat_fee_count" width="125px" label="平台扣费合计">
          <template slot-scope="scope">
            <p>{{scope.row.i_plat_fee_count|filterNumber}}</p>
          </template>
        </el-table-column>

        <el-table-column prop="i_kf_fee_count" width="125px" label="客服费用合计">
          <template slot-scope="scope">
            <p>{{scope.row.i_kf_fee_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_huodong_fee" width="125px" label="活动费用">
          <template slot-scope="scope">
            <p>{{scope.row.i_huodong_fee|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_tag_fee" width="125px" label="吊牌费">
          <template slot-scope="scope">
            <p>{{scope.row.i_tag_fee|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_net_ml_11" width="125px" label="1.1净毛利">
          <template slot-scope="scope">
            <p>{{scope.row.i_net_ml_11|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_net_ml_rate_11" width="125px" label="1.1净毛利率"></el-table-column>
        <el-table-column prop="i_refund_rate" width="125px" label="退款率"></el-table-column>
        <el-table-column prop="i_tg_pat_rate" width="125px" label="运营付费占比"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="query.pageNum"
        :page-sizes="[5, 10, 15, 20,50,100]"
        :page-size="query.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="cur_data.length"
      ></el-pagination>
    </el-card>
  </div>
</template>
<script>


import moment from "moment";

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
        "成交金额":"i_deal_money","退款金额":"i_refund_money",
        "发货前退款金额":"i_sendgoods_front_refund_money","发货后退款金额":"i_sendgoods_after_refund_money",
        "补单金额":"i_budan_money","净销售额":"i_net_sale",
        "1.1衣服成本":"i_clothing_cost_11","快递费用":"i_kuaidi_fee",
        "发货费用":"i_sendgoods_fee","1.1毛利":"i_ml_11",
        "付费推广合计":"i_tg_pay_count","平台扣费合计":"i_plat_fee_count",
        "客服费用合计":"i_kf_fee_count","活动费用":"i_huodong_fee",
        "吊牌费":"i_tag_fee","1.1净毛利":"i_net_ml_11",
        "1.1净毛利率":"i_net_ml_rate_11","运营付费占比":"i_tg_pat_rate",
        "退款率":"i_refund_rate"
      },
      cur_data:[],
      //分页数据
      query: {
        pageNum: 1,
        pageSize: 20,
        total: 0
      },
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

    // table 表数据
    tableData() {
      const { pageNum, pageSize } = this.query;
      return this.cur_data.slice((pageNum - 1) * pageSize, pageNum * pageSize);
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
    }
  },
  watch:{
    table_status(newV,oldV){
      this.table_status=newV
    },
    data_all(newV,oldV){
      this.data_all=newV
      console.log("#############")
      console.log(this.data_all)
      console.log("#############")
      var cur_data2=[]
      var cur_map= {}
      this.data_all.forEach(function (item){
        if(!cur_map.hasOwnProperty(item.shop)){
          cur_map[item.shop]={
            'shop':item.shop,'i_deal_money':item.i_deal_money,'i_refund_money':item.i_refund_money,
            'i_sendgoods_front_refund_money':item.i_sendgoods_front_refund_money,'i_sendgoods_after_refund_money':item.i_sendgoods_after_refund_money,
            'i_budan_money':item.i_budan_money,'i_net_sale':item.i_net_sale,'i_clothing_cost_11':item.i_clothing_cost_11,
            'i_kuaidi_fee':item.i_kuaidi_fee,"i_sendgoods_fee":item.i_sendgoods_fee,"i_ml_11":item.i_ml_11,
            "i_tg_pay_count":item.i_tg_pay_count,"i_plat_fee_count":item.i_plat_fee_count,"i_kf_fee_count":item.i_kf_fee_count,
            "i_huodong_fee":item.i_huodong_fee,"i_tag_fee":item.i_tag_fee,"i_net_ml_11":item.i_net_ml_11,
            "i_net_ml_rate_11":item.i_net_ml_rate_11,"i_tg_pat_rate":item.i_tg_pat_rate,"i_refund_rate":item.i_refund_rate,
            'items':[item]
          }
        }else {
          cur_map[item.shop]['i_deal_money']+=item.i_deal_money
          cur_map[item.shop]['i_refund_money']+=item.i_refund_money
          cur_map[item.shop]['i_budan_money']+=item.i_budan_money
          cur_map[item.shop]['i_net_sale']+=item.i_net_sale
          cur_map[item.shop]['i_clothing_cost_11']+=item.i_clothing_cost_10
          cur_map[item.shop]['i_kuaidi_fee']+=item.i_kuaidi_fee
          cur_map[item.shop]['i_sendgoods_fee']+=item.i_sendgoods_fee
          cur_map[item.shop]['i_ml_11']+=item.i_ml_11

          cur_map[item.shop]['i_tg_pay_count']+=item.i_tg_pay_count
          cur_map[item.shop]['i_plat_fee_count']+=item.i_plat_fee_count
          cur_map[item.shop]['i_kf_fee_count']+=item.i_kf_fee_count
          cur_map[item.shop]['i_huodong_fee']+=item.i_huodong_fee
          cur_map[item.shop]['i_tag_fee']+=item.i_tag_fee
          cur_map[item.shop]['i_net_ml_11']+=item.i_net_ml_11

          cur_map[item.shop]['i_net_ml_rate_11']+=item.i_net_ml_rate_11
          cur_map[item.shop]['i_tg_pat_rate']+=item.i_tg_pat_rate
          cur_map[item.shop]['i_refund_rate']+=item.i_refund_rate


          // console.log(cur_map[item.shop]['i_net_ml_11'])
          if (cur_map[item.shop]['i_net_ml_11']===0||cur_map[item.shop]['i_net_sale']===0){
            var number1=0
          }else {
            var number1=Math.round((cur_map[item.shop]['i_net_ml_11']/cur_map[item.shop]['i_net_sale'])*10000)/100
          }

          if (cur_map[item.shop]['i_refund_money']===0||cur_map[item.shop]['i_deal_money']===0){
            var number2=Math.round(0-cur_map[item.shop]['i_budan_money'])/100
          }else {
            var number2=Math.round((cur_map[item.shop]['i_refund_money']/(cur_map[item.shop]['i_deal_money']-cur_map[item.shop]['i_budan_money']))*10000)/100
          }

          if (cur_map[item.shop]['i_tg_pay_count']===0||cur_map[item.shop]['i_net_sale']===0){
            var number3=0
          }else {
            var number3=Math.round((cur_map[item.shop]['i_tg_pay_count']/cur_map[item.shop]['i_net_sale'])*10000)/100
          }
          cur_map[item.shop]['i_net_ml_rate_11']=number1.toString()+"%"//1.1净毛利/净销售额
          cur_map[item.shop]['i_refund_rate']=number2.toString()+"%"//退款金额/(成交金额-补单金额)
          cur_map[item.shop]['i_tg_pat_rate']=number3.toString()+"%"//付费推广合计/净销售额


          cur_map[item.shop]['i_deal_money']=Math.round(cur_map[item.shop]['i_deal_money']*100)/100
          cur_map[item.shop]['i_refund_money']=Math.round(cur_map[item.shop]['i_refund_money']*100)/100
          cur_map[item.shop]['i_budan_money']=Math.round(cur_map[item.shop]['i_budan_money']*100)/100
          cur_map[item.shop]['i_net_sale']=Math.round(cur_map[item.shop]['i_net_sale']*100)/100
          cur_map[item.shop]['i_clothing_cost_11']=Math.round(cur_map[item.shop]['i_clothing_cost_11']*100)/100
          cur_map[item.shop]['i_kuaidi_fee']=Math.round(cur_map[item.shop]['i_kuaidi_fee']*100)/100
          cur_map[item.shop]['i_sendgoods_fee']=Math.round(cur_map[item.shop]['i_sendgoods_fee']*100)/100
          cur_map[item.shop]['i_ml_11']=Math.round(cur_map[item.shop]['i_ml_11']*100)/100

          cur_map[item.shop]['i_tg_pay_count']=Math.round(cur_map[item.shop]['i_tg_pay_count']*100)/100
          cur_map[item.shop]['i_plat_fee_count']=Math.round(cur_map[item.shop]['i_plat_fee_count']*100)/100
          cur_map[item.shop]['i_kf_fee_count']=Math.round(cur_map[item.shop]['i_kf_fee_count']*100)/100
          cur_map[item.shop]['i_huodong_fee']=Math.round(cur_map[item.shop]['i_huodong_fee']*100)/100
          cur_map[item.shop]['i_tag_fee']=Math.round(cur_map[item.shop]['i_tag_fee']*100)/100
          cur_map[item.shop]['i_net_ml_11']=Math.round(cur_map[item.shop]['i_net_ml_11']*100)/100

          cur_map[item.shop]['items'].push(item)
        }
      })
      for(let key in cur_map){
        var cur2_map=cur_map[key]
        cur_data2.push(cur2_map)
      }
      this.cur_data=cur_data2
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
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>
