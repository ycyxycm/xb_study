<template>
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">

    <el-tab-pane label="概况" name="first">
      <dy_survey/>
    </el-tab-pane>

    <el-tab-pane label="汇总" name="second">
      <dy_sales/>
    </el-tab-pane>

    <el-tab-pane label="发货退货数据源" name="third">
      <dy_sendcost/>
    </el-tab-pane>

    <el-tab-pane label="店铺订单数据源" name="fourth">
      <dy_sendgoods/>
    </el-tab-pane>

  </el-tabs>
</template>
<script>
import dy_survey from './dy_Survey.vue'
import dy_sales from './dy_sales.vue'
import dy_sendcost from "./dy_sendcost";
import dy_sendgoods from "./dy_sendgoods";

export default {
  data() {
    return {
      activeName: 'first'
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  },
  components:{
    dy_survey,
    dy_sales,
    dy_sendcost,
    dy_sendgoods,
  }
};
</script>
