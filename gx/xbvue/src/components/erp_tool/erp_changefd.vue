<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6"><div class="grid-content bg-purple">
        <el-select v-model="selectvalue" clearable placeholder="请选择" @change="seonchange">
          <el-option
            v-for="item in options"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
<!--        <el-button type="primary" @click="requestData">查询</el-button>-->
      </div></el-col>
      <el-col :span="4"><div class="grid-content bg-purple">
        <el-button type="primary" :loading="search_bt_loading" @click="onMatchingStock">查询商品当前可用库存</el-button>
      </div></el-col>
      <el-col :span="6"><div class="grid-content bg-purple">
        <el-button type="success" :loading="fd_matching_bt_loading" @click="onMatchingFD(false)">福袋匹配</el-button>
        <el-switch
          v-model="type_sex"
          active-text="女"
          inactive-text="男">
        </el-switch>
        <el-button type="success" :loading="stock_matching_bt_loading" @click="onMatchingFD(true)">缺货匹配</el-button>
      </div></el-col>
      <el-col :span="4"><div class="grid-content bg-purple">
        <el-button type="success" :loading="many_change_bt_loading" @click="onChangeFD">批量换福袋</el-button>
      </div></el-col>
    </el-row>

  <el-table
    ref="multipleTable"
    v-loading="loading"
    :data="TableData"
    style="width: 100%"
    :row-key="(row)=>row.o_id"
    @selection-change="handleSelectionChange">
    <el-table-column type="expand" fixed>
      <template slot-scope="props">
        <el-table
          :data="props.row.items"
          style="margin-left: 40px"
          border
          :cell-style="{padding:'5px'}"
          :header-cell-style="{padding:'5px'}"
        >
          <el-table-column
            prop="oi_id"
            label="商品id"
            width="100px">
          </el-table-column>
          <el-table-column
            prop="sku_id"
            label="商品编码"
            width="500px">
          </el-table-column>
          <el-table-column
            prop="price"
            label="单价"
            width="80px">
          </el-table-column>
          <el-table-column
            prop="qty"
            label="数量"
            width="80px">
          </el-table-column>
          <el-table-column
            prop="amount"
            label="总价"
            width="80px">
          </el-table-column>
          <el-table-column
            prop="can_stock"
            label="可用库存"
            width="70px">
          </el-table-column>
          <el-table-column label="替换后商品编码" width="500px">
            <template slot-scope="ins">
              <el-input size="small" v-model="ins.row.newsku_id"></el-input>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-table-column>
    <el-table-column
      fixed
      label="序号"
      type="index"
      width="50">
    </el-table-column>
    <el-table-column
      fixed
      type="selection"
      :reserve-selection="true"
      width="55">
    </el-table-column>
    <el-table-column
      fixed
      label="内部订单号"
      prop="o_id">
    </el-table-column>
    <el-table-column
      fixed
      label="标记|多标签"
      prop="labels">
    </el-table-column>
    <el-table-column
      fixed
      label="线上订单号"
      prop="so_id">
    </el-table-column>
    <el-table-column
      fixed
      label="店铺"
      prop="shop_name">
    </el-table-column>
    <el-table-column
      fixed
      label="已付金额"
      prop="paid_amount">
    </el-table-column>
  </el-table>
    <el-row :gutter="10">
      <el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1"><div class="grid-content bg-purple"><span style="font-size: 14px;color: dimgrey">共 {{ this.TableDataCount }} 条数据</span></div></el-col>
      <el-col :xs="8" :sm="6" :md="4" :lg="3" :xl="1"><div class="grid-content bg-purple-light"><span style="font-size: 14px;color: dimgrey">当前选中 {{ this.multipleSelection.length }} 条数据</span></div></el-col>
      <el-col :xs="4" :sm="6" :md="8" :lg="9" :xl="11"><div class="grid-content bg-purple-light"></div></el-col>
      <el-col :xs="4" :sm="6" :md="8" :lg="9" :xl="11"><div class="grid-content bg-purple"></div></el-col>
    </el-row>
  </div>
</template>

<script>
import { request } from "@/utils/request";
import moment from "moment";
import api from '@/utils/api'


export default {
  data() {
    return {
      type_sex:false,//false=男 true=女
      search_bt_loading:false,
      fd_matching_bt_loading:false,
      stock_matching_bt_loading:false,
      many_change_bt_loading:false,
      outtime:0,
      selectvalue:'',
      TableDataCount:0,
      TableData:[],
      multipleSelection: [],
      loading:false,
      options:['女装程序换福袋','男装程序换福袋','测试订单','红包卡单','福袋缺货','商品资料不存在']
    }
  },
  mounted() {
    // this.getData();
  },
  methods: {
    requestData() {//获取erp异常类型的订单
      this.loading=true
      return request.post(api.http+"/erp/get_orders",{abn:this.selectvalue}).then(res => {
        if (res.data.status!=200){
          this.$notify.error({
            title: '错误',
            message: res.data.msg
          });
        }
        this.loading=false
        this.TableData=res.data.data.data
        this.TableDataCount=res.data.data.datacount
      });
    },
    // getData() {
    //   this.requestData().then(data => {
    //     this.TableData = data.data
    //     this.TableDataCount =data.datacount
    //   });
    // },
    ToggleSelection(rows) {
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = (val || []).map( i => i.o_id);
      console.log((val || []).map( i => i.o_id))
    },
    async onChangeFD(){

      if (this.multipleSelection.length<=0){
        this.$notify({title: '警告', message: '未选中任何订单', type: 'warning'});
      }else {
        var err_change_array=[]
        this.many_change_bt_loading=true
        var cur_array=this.get_table_data()
        var index=0
        for (const item of cur_array) {
          index+=1
          await this.sleep(2000)
          await request.post(api.http + '/erp/change_sku', item).then(res => {
            if (res.data.status != 200) {
              this.$notify.error({
                title: '内部订单号' + item.o_id + '错误' + res.data.status,
                message: res.data.msg,
                duration: 0
              })
              err_change_array.push(item.o_id)
            } else {
              this.$notify({title: " 第"+index+" 个成功", message: res.data.msg, type: 'success'})
            }
          })
        }
        //
        var alert_msg="全部替换成功!"
        if (err_change_array.length>0){
          alert_msg="部分替换失败,请检阅:"+err_change_array.join(",")
        }
        this.$alert('更换完成!', '已完成', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: '提示',
              message: `页面重载中......`
            });
            this.many_change_bt_loading=false
            this.requestData()
          }
        });
        //

      }
    },
    onMatchingFD(stock_type){//福袋匹配
      if (this.multipleSelection.length<=0){
        this.$notify({title: '警告', message: '未选中任何订单', type: 'warning'});
      }else{
        this.fd_matching_bt_loading=true
        var cur_array=this.get_table_data()
        request.post(api.http+'/erp/matching_sku',{'data':cur_array,'stock_type':stock_type,'type_sex':this.type_sex}).then(res=>{
          if(res.data.status!=200){
            this.$notify.error({title:'错误',message:res.data.msg,duration:0})
          }else{
            this.$notify({title:"成功",message:res.data.msg,type:'success'})
            //重新渲染
            res.data.data.forEach((item,index)=>{
              var idx=this.TableData.findIndex((i)=>{
                return i.o_id===item.o_id
              })
              if (idx!=-1){
                this.$set(this.TableData,idx,item)
              }else{
                this.$notify.error({title:'错误',message:'没有找到oid对应行',duration:0})
              }
            })

          }
          // this.multipleSelection=res.data.data
        })
        this.fd_matching_bt_loading=false
        // this.requestData()
      }
    },
    getRowKeys(row){
      return row.o_id
    },
    sleep(time) {
      return new Promise(resolve => setTimeout(resolve, time))
    },
    seonchange(){
      this.$refs.multipleTable.clearSelection();
      this.TableData=[]
      this.requestData()
    },
    onMatchingStock(){
      if (this.multipleSelection.length<=0){
        this.$notify({title: '警告', message: '未选中任何订单', type: 'warning'});
      }else{
        this.search_bt_loading=true
        var cur_array=this.get_table_data()
        request.post(api.http+'/erp/matching_stock',cur_array).then(res=>{
          if (res.data.status!=200){
            this.$notify.error({title:'错误'+res.data.status,message:res.data.msg,duration:0})
          }else{
            this.$notify({title:"成功",message:res.data.msg,type:'success'})
            //重新渲染
            res.data.data.forEach((item,index)=>{
              var idx=this.TableData.findIndex((i)=>{
                return i.o_id===item.o_id
              })
              if (idx!=-1){
                this.$set(this.TableData,idx,item)
              }else{
                this.$notify.error({title:'错误',message:'没有找到oid对应行',duration:0})
              }
            })
          }
          // this.multipleSelection=res.data.data
          this.search_bt_loading=false
        })

        // this.requestData()
      }
    },
    get_table_data(){
      var re_arry=[]
      this.multipleSelection.forEach((v1,index)=>{
        this.TableData.forEach((value,index)=>{
          if (value.o_id===v1){
            re_arry.push(value)
          }
        });
      });
      if (this.multipleSelection.length!=re_arry.length){
        alert("错误原因未知,联系管理员")
        return null
      }else {
        console.log(re_arry)
        return re_arry
      }



    }
  },
}
</script>
<style scoped>
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
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
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
