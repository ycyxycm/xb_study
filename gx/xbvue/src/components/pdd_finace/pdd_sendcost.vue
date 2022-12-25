<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_店铺款式发退货"
      name="PDD_店铺款式发退货.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="120"></el-table-column>
        <el-table-column prop="stylecode" label="款式编码"></el-table-column>
        <el-table-column prop="send_number" label="发货数量">
          <template slot-scope="scope">
            <p>{{scope.row.send_number|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="refund_number" label="退货数量">
          <template slot-scope="scope">
            <p>{{scope.row.refund_number|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="today_price" label="当天成本价">
          <template slot-scope="scope">
            <p>{{scope.row.today_price|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="today_tag" label="此款当天吊牌价">
          <template slot-scope="scope">
            <p>{{scope.row.today_tag|filterNumber}}</p>
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
        "款式编码":"stylecode","发货数量":"send_number",
        "退货数量":"refund_number","当天成本价":"today_price",
        "此款当天吊牌价":"today_tag"
      },
      //分页数据
      query: {
        pageNum: 1,
        pageSize: 20,
        total: 0
      },
    };
  },
  computed: {
    //table 表数据
    tableData() {
      const { pageNum, pageSize } = this.query;
      return this.data_all.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    }
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
      // console.log(this.table_status)
    },
    data_all(newV,oldV){
      this.data_all=newV
      // console.log(this.data_all.length)
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
