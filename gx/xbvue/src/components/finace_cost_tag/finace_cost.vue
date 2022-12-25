<template>
  <div>
    <el-upload
      ref="uploadv"
      class="upload-demo"
      action="a"
      accept=".xlsx"
      :limit="1"
      :on-change="handleChange"
      :file-list="filelist"
      :http-request="uploadFile"
      :auto-upload="false"

      :before-upload="beforeUpload">
      <template #trigger>
        <el-button type="primary">选择文件</el-button>
      </template>
      <el-button class="ml-3" type="success" @click="submitUpload">上传到服务器</el-button>
      <div slot="tip" style="width: 200px" class="el-upload__tip">只能上传xlsx文件，且不超过1000MB</div>
    </el-upload>
    <el-table
      v-loading="loading"
      :data="tableData.filter(data => !search || data.stylecode.toLowerCase().includes(search.toLowerCase()))"
      style="width: 100%">
      <el-table-column
        label="款式编码"
        prop="stylecode">
      </el-table-column>
      <el-table-column
        label="抖音"
        prop="dy_cost">
      </el-table-column>
      <el-table-column
        label="天猫"
        prop="tm_cost">
      </el-table-column>
      <el-table-column
        label="拼多多"
        prop="pdd_cost">
      </el-table-column>
      <el-table-column
        label="京东"
        prop="jd_cost">
      </el-table-column>
      <el-table-column
        label="淘工厂"
        prop="tgc_cost">
      </el-table-column>
      <el-table-column
        align="right">
        <template slot="header" slot-scope="scope">
          <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索"/>
        </template>
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="left" label-width="80px" :model="dialogform">
        <el-form-item label="款式编码">
          <el-input size="small" disabled v-model="dialogform.stylecode"></el-input>
        </el-form-item>
        <el-form-item label="抖音">
            <el-input-number v-model="dialogform.dy_cost" :precision="4" :step="0.1" :max="9999"></el-input-number>
        </el-form-item>
        <el-form-item label="天猫">
            <el-input-number v-model="dialogform.tm_cost" :precision="4" :step="0.1" :max="9999"></el-input-number>
        </el-form-item>
        <el-form-item label="拼多多">
            <el-input-number v-model="dialogform.pdd_cost" :precision="4" :step="0.1" :max="9999"></el-input-number>
        </el-form-item>
        <el-form-item label="京东">
            <el-input-number v-model="dialogform.jd_cost" :precision="4" :step="0.1" :max="9999"></el-input-number>
        </el-form-item>
        <el-form-item label="淘工厂">
            <el-input-number v-model="dialogform.tgc_cost" :precision="4" :step="0.1" :max="9999"></el-input-number>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @submit="submitdialog">保存</el-button>
  </span>
    </el-dialog>
<!--    <el-pagination-->
<!--      @size-change="handleSizeChange"-->
<!--      @current-change="handleCurrentChange"-->
<!--      :current-page="query.pageNum"-->
<!--      :page-sizes="[5, 10, 15, 20]"-->
<!--      :page-size="query.pageSize"-->
<!--      layout="total, sizes, prev, pager, next, jumper"-->
<!--      :total="tableData.length"-->
<!--    ></el-pagination>-->

  </div>
</template>

<script>
import {request} from "../../utils/request";
import api from "../../utils/api";

export default {
  data(){
    return{
      dialogform: {
        stylecode:"",
        dy_cost:"",
        tm_cost:"",
        pdd_cost:"",
        jd_cost:"",
        tgc_cost:""
      },
      dialogVisible: false,
      loading:true,
      tableData: [],
      query: {
        pageNum: 1,
        pageSize: 15,
        total: 0
      },
      search: '',
      filelist: [],
      file:null,
    }
  },
  computed:{
    //table 表数据
    ftableData() {
      const { pageNum, pageSize } = this.query;
      return this.tableData.slice((pageNum - 1) * pageSize, pageNum * pageSize);
    }
  },
  mounted() {
    this.getData();
  },
  methods:{
    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {});
    },
    requestData() {
      return request.get(api.http+"/finace/fcost").then(res => {
        if (res.data.status!=200){
          this.$notify.error({
            title: '错误',
            message: res.data.msg
          });
        }
        this.loading=false
        return res.data.data;
      });
    },
    getData() {
      this.requestData().then(data => {
        this.tableData = data;
      });
    },
    handleEdit(index, row) {
      this.dialogVisible=true//开弹窗
      this.dialogform.stylecode=""//赋值form表单
      this.dialogform.dy_cost=""
      this.dialogform.tm_cost=""
      this.dialogform.pdd_cost=""
      this.dialogform.jd_cost=""
      this.dialogform.tgc_cost=""//初始化form表单
      console.log(index, row);
      this.dialogform.stylecode=row.stylecode//赋值form表单
      this.dialogform.dy_cost=row.dy_cost
      this.dialogform.tm_cost=row.tm_cost
      this.dialogform.pdd_cost=row.pdd_cost
      this.dialogform.jd_cost=row.jd_cost
      this.dialogform.tgc_cost=row.tgc_cost

    },
    submitdialog(){

    },
    handleDelete(index, row) {
      console.log(index, row);
    },
    beforeUpload(){
      if (this.filelist[0]===null){
        this.$message({
          message: '未选择任何文件',
          type: 'warning'
        });
        return false
      }
      var first=this.filelist[0]
      const FILE_NAME = first.name
      if (FILE_NAME.substring(FILE_NAME.lastIndexOf('.')) !== '.xlsx') {
        this.$message.warning('仅支持.xlsx文件')
        return false
      }
      const isLt1M = first.size / 1024 / 1024 < 1000
      if (isLt1M) {
        this.file = first
        return true
      }
      this.$message.warning('请上传不超过1000M的文件.')
      return false
    },
    handleChange(file, fileList){
      this.filelist = fileList;
      console.log(this.filelist)
    },
    submitUpload(){
      this.$refs.uploadv.submit();
      let data = new FormData();
      let config = []
      data.append('file', this.file.raw);

      request.post(api.http+'/finace/newfcost', data, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(res => {
        if (res.data.status!=200){
          this.$message({
            message: res.data.msg,
            type: 'warning'
          });
        }else {
          this.$message({
            message: res.data.msg,
            type: 'success'
          });
        }

      })


    },
    uploadFile(){},
    handleSizeChange(val) {
      this.query.pageSize = val;
      this.query.pageNum = 1;
    },
    //切换页数，执行方法
    handleCurrentChange(val) {
      this.query.pageNum = val;
    },
  }


}
</script>

<style scoped>

</style>
