<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_店铺占比"
      name="PDD_店铺占比.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" height="1000" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="120"></el-table-column>
        <el-table-column prop="i_deal_money" label="成交金额">
          <template slot-scope="scope">
            <p>{{scope.row.i_deal_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_refund_money" label="退款金额">
          <template slot-scope="scope">
            <p>{{scope.row.i_refund_money|filterNumber}}</p>
          </template>
        </el-table-column>

        <el-table-column prop="i_sendgoods_after_refund_rate" label="退款率"></el-table-column>
        <el-table-column prop="i_budan_money" label="补单金额">
          <template slot-scope="scope">
            <p>{{scope.row.i_budan_money|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_budan_rate" label="补单率"></el-table-column>
        <el-table-column prop="i_net_sale" label="净销售额">
          <template slot-scope="scope">
            <p>{{scope.row.i_net_sale|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_net_ml_11" label="1.1净毛利"></el-table-column>
        <el-table-column prop="i_net_ml_rate_11" label="1.1净毛利率"></el-table-column>
        <el-table-column prop="i_clothing_cost_rate_11" label="1.1衣服成本占比"></el-table-column>
        <el-table-column prop="i_sendgoods_fee_rate" label="发货费用占比"></el-table-column>
        <el-table-column prop="i_return_goods_cost_rate" label="退货衣服成本占比"></el-table-column>
        <el-table-column prop="i_tg_pat_rate" label="运营付费占比"></el-table-column>
        <el-table-column prop="i_plat_fee_rate" label="平台扣费占比"></el-table-column>
        <el-table-column prop="i_kf_fee_rate" label="客服费用占比"></el-table-column>
        <el-table-column prop="i_huodong_fee_rate" label="活动费用占比"></el-table-column>
        <el-table-column prop="i_tag_fee_rate" label="吊牌费用占比"></el-table-column>
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
        "退款率":"i_refund_rate","补单金额":"i_budan_money",
        "补单率":"i_budan_rate","净销售额":"i_net_sale",
        "1.1净毛利":"i_net_ml_11","1.1净毛利率":"i_net_ml_rate_11",
        "1.1衣服成本占比":"i_clothing_cost_rate_11","发货费用占比":"i_sendgoods_fee_rate",
        "退货衣服成本占比":"i_return_goods_cost_rate","运营付费占比":"i_tg_pat_rate",
        "平台扣费占比":"i_plat_fee_rate","客服费用占比":"i_kf_fee_rate",
        "活动费用占比":"i_huodong_fee_rate","吊牌费用占比":"i_tag_fee_rate"
      },
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
  },
  watch:{
    table_status(newV,oldV){
      this.table_status=newV
    },
    data_all(newV,oldV){
      this.data_all=newV
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
