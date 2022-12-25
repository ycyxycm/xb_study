<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="data_all"
      :fields="json_fields"
      title="PDD_付费推广明细"
      name="PDD_付费推广明细.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <el-table-column fixed prop="now_date" label="日期" width="120"></el-table-column>
        <el-table-column prop="i_tg_pay_count" label="付费推广合计">
          <template slot-scope="scope">
            <p>{{scope.row.i_tg_pay_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_dd_search_scene" label="多多搜索和场景">
          <template slot-scope="scope">
            <p>{{scope.row.i_dd_search_scene|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_budan_comm" label="补单佣金">
          <template slot-scope="scope">
            <p>{{scope.row.i_budan_comm|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_fxt" label="放心推">
          <template slot-scope="scope">
            <p>{{scope.row.i_fxt|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_dd_jinbao" label="多多进宝">
          <template slot-scope="scope">
            <p>{{scope.row.i_dd_jinbao|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column prop="i_qztg" label="全站推广">
          <template slot-scope="scope">
            <p>{{scope.row.i_qztg|filterNumber}}</p>
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
        "付费推广合计":"i_tg_pay_count","多多搜索和场景":"i_dd_search_scene",
        "补单佣金":"i_budan_comm","放心推":"i_fxt",
        "多多进宝":"i_dd_jinbao","全站推广":"i_qztg"
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
