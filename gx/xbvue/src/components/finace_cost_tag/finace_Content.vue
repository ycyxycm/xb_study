<template>
  <el-tabs v-model="activeName" type="card" @tab-click="handleClick">

    <el-tab-pane label="店铺成本价" name="first">
      <finace_cost/>
    </el-tab-pane>

    <el-tab-pane label="店铺吊牌价" name="second">
      #
    </el-tab-pane>

  </el-tabs>
</template>
<script>
import finace_cost from "./finace_cost";
import myfunction from '@/utils/myfunction'

export default {
  data() {
    return {
      activeName: 'first'
    };
  },
  mounted() {
    myfunction.check_session(this)
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    }
  },
  components:{
    finace_cost
  }
};
</script>
