<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_活动费用明细"
      name="PDD_活动费用明细.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="120"></el-table-column>
        <el-table-column prop="i_huodong_fee" label="活动费用">
          <template slot-scope="scope">
            <p>{{scope.row.i_huodong_fee|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_bybt" label="百亿补贴">
          <template slot-scope="scope">
            <p>{{scope.row.i_bybt|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_loan" label="贷款充值跨店满减">
          <template slot-scope="scope">
            <p>{{scope.row.i_loan|filterNumber}}</p>
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
        "活动费用":"i_huodong_fee","百亿补贴":"i_bybt",
        "贷款充值跨店满减":"i_loan"
      },
      //分页数据
      query: {
        pageNum: 1,
        pageSize: 15,
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
