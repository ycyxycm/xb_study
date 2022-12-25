<template>
  <div class="wrap">
    <download-excel
      class="export-excel"
      :data="cur_data"
      :fields="json_fields"
      title="PDD_1.1汇总"
      name="PDD_1.1汇总.xls">
      <el-button type="primary" size="mini" round>
        导出Excel
      </el-button>
    </download-excel>
    <el-card>
      <el-table v-loading="table_status" height="1000" :data="tableData" border stripe style="width: 100%" :row-style="{height:'20px'}"
                :cell-style="{padding:'4px'}">
        <el-table-column fixed :show-overflow-tooltip="true" prop="shop" label="店铺" width="250"></el-table-column>
        <!--        <el-table-column fixed prop="now_date" label="日期" width="100"></el-table-column>-->
        <el-table-column fixed prop="i_net_sale_count" label="净销售额">
          <template slot-scope="scope">
            <p>{{scope.row.i_net_sale_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column fixed prop="i_net_ml_11_count" label="1.1净毛利">
          <template slot-scope="scope">
            <p>{{scope.row.i_net_ml_11_count|filterNumber}}</p>
          </template>
        </el-table-column>
        <el-table-column fixed prop="i_net_ml_rate_11_count" label="1.1净毛利率"></el-table-column>
        <el-table-column
          v-for="item in dateInfo.interval"
          :key="item"
          :label="item"
          v-if="show(item)"
          :render-header="renderHeader"
        >
          <template v-slot="ins">
            <div>
              {{ findTrueItem(ins, item) || "0" }}
            </div>
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
      json_fields:{},
      cur_interval:[],
      cur_data:[],
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
      return this.cur_data.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    },
    dateInfo() {
      const allDateInfo = this.data_all.flatMap(i =>
        moment(i.now_date).valueOf()
      );

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

  },
  methods: {
    renderHeader (h,{column}) { // h即为cerateElement的简写，具体可看vue官方文档
      return h(
        'div',
        [
          h('span', column.label),
          h('el-checkbox',{
            style:'margin-left:5px',
            on:{
              change:checked=>this.select(checked,column.label) // 选中事件
            }
          })
        ],
      );
    },
    // 添加选中事件
    select (e,b) {
      if (e){
        this.cur_interval.push(b)
      }
    },
    show(item){
      if (this.cur_interval.length===0){
        return true
      }else{
        var a=this.cur_interval.indexOf(item)
        if(a>=0){
          return false
        }else {
          return true
        }
      }

    },
    //切换当前页显示的数据条数，执行方法
    handleSizeChange(val) {
      this.query.pageSize = val;
      this.query.pageNum = 1;
    },
    findTrueItem(item, key) {
      // console.log(item)
      // console.log(key)
      var cur_strr=String(item.row[key]).replace(/\B(?=(\d{3})+(?!\d))/g,',')
      if (item.row[key]==null||cur_strr===0||cur_strr==="0"){
        return "--"
      }else {
        return cur_strr
      }
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
      var cur_data2=[]
      var cur_map= {}
      this.data_all.forEach(function (item){
        if(!cur_map.hasOwnProperty(item.shop)){
          cur_map[item.shop]={'shop':item.shop}
        }
        if (!cur_map[item.shop].hasOwnProperty('i_net_ml_11_count')){
          cur_map[item.shop]['i_net_ml_11_count']=0
        }
        if (!cur_map[item.shop].hasOwnProperty('i_net_sale_count')){
          cur_map[item.shop]['i_net_sale_count']=0
        }
        cur_map[item.shop]['i_net_ml_11_count']+=item.i_net_ml_11
        cur_map[item.shop]['i_net_sale_count']+=item.i_net_sale
        if(cur_map[item.shop]['i_net_ml_11_count']==0||cur_map[item.shop]['i_net_sale_count']==0){
          cur_map[item.shop]['i_net_ml_rate_11_count']="0%"
        }else {
          cur_map[item.shop]['i_net_ml_rate_11_count']=(Math.round((cur_map[item.shop]['i_net_ml_11_count']/cur_map[item.shop]['i_net_sale_count'])*10000)/100).toString()+'%'
        }
        cur_map[item.shop][item.now_date]=Math.round(item.i_net_ml_11*100)/100




        cur_map[item.shop]['i_net_ml_11_count']=Math.round(cur_map[item.shop]['i_net_ml_11_count']*100)/100
        cur_map[item.shop]['i_net_sale_count']=Math.round(cur_map[item.shop]['i_net_sale_count']*100)/100

      })
      for(let key in cur_map){
        var cur2_map=cur_map[key]
        // cur2_map['shop']=key
        cur_data2.push(cur2_map)
      }
      this.cur_data=cur_data2

      this.json_fields={}
      for(let i in this.cur_data[0]){
        if (i==="i_net_ml_11_count"){
          var k="1.1净毛利 合计"
        }else if(i==="i_net_sale_count"){
          var k="净销售额 合计"
        }else if(i==="i_net_ml_rate_11_count"){
          var k="1.1净毛利率 合计"
        }else if(i==="shop"){
          var k="店铺"
        }else{
          var k=i
        }
        var y=i
        this.json_fields[k]=y
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
