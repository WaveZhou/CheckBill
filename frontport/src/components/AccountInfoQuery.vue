<template>
  <div>
    <h1> 券商账户信息表查询 </h1>
     <el-col :span="2" style="float : right;margin-right: 85px;">
      <el-button
        type="success"
        @click="extract_file"
        icon="el-icon-share"
        size="mini"
        style="margin-left: 34px;"
      >一键导出</el-button>
    </el-col>
    <el-table
      :data="table_data"
      style="width: 100%"
      :header-cell-style="{textAlign:'center'}"
      :cell-style="{textAlign: 'center'}"
      height="520"
      :index="indexMethod"
    >
       <el-table-column label="序 号" type="index"
          width="140" >
      </el-table-column>
      <el-table-column label="产品名称" width="280">
        <template slot-scope="scope">
          <span> {{ scope.row.product}}</span>
        </template>
      </el-table-column>
      <el-table-column label="证券机构" width="280">
        <template slot-scope="scope">
           <span> {{ scope.row.belong }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账户类型" width="280">
        <template slot-scope="scope">
           <span> {{ scope.row.type }}</span>
        </template>
      </el-table-column>
      <el-table-column label="营业部" width="280">
        <template slot-scope="scope">
           <span> {{ scope.row.business_department }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账户状态" width="280">
        <template slot-scope="scope">
            <span> {{options[scope.row.status]['label']}} </span>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="280" >
        <template slot="header" slot-scope="scope">

          <el-input v-model="search"  placeholder="输入关键字搜索" />

        </template>

      </el-table-column>
    </el-table>
    <el-pagination
                          @size-change="handleSizeChange"
                          @current-change="handleCurrentChange"
                          :current-page="currentPage"
                           :page-sizes="[5, 10, 15, 20]"
                          :page-size="pagesize"
                           layout="total, sizes, prev, pager, next, jumper"
                          :total=parseInt(tableDate_length)>
    </el-pagination>
  </div>

</template>

<script>
import axios from "axios";

import * as XLSX from "xlsx";

export default {
  name: "AccountInfoQuery",
  data(){
    return {
      currentPage:1, //初始页
      pagesize:10,
      tableData: [],//   数据总量
      tableDate_length:"",
      dialogFormVisible: false,
      dialogFormVisibles: false,
      formLabelWidth:'',
      tableData_back : [],
      tableDate_length_back : '',
      token: '',
      search: "",
      options:[
        {
          value : "0",
          label : "销户"
        },{
          value : "1",
          label: "正常"
        },{
          value : "2",
          label: "休眠/冻结"
        },{
          value: "3",
          label: "准备销户"
        }
      ],

    }
  },
  created() {
     this.initTable();
  },
  computed:{
    table_data() {
      let search = this.search;
      // 搜索功能且分页
      if (search){
        //{{options[scope.row.status]['label']}}

        let list =this.tableData.filter(data => !search || data.account.toLowerCase().includes(search.toLowerCase()) || data.belong.toLowerCase().includes(search.toLowerCase()) || data.type.toLowerCase().includes(search.toLowerCase()) || data.product.toLowerCase().includes(search.toLowerCase()) || data.business_department.toLowerCase().includes(search.toLowerCase()) || this.options[data.status]['label'].toLowerCase().includes(search.toLowerCase()));

        let fenye = list.slice((this.currentPage-1)*this.pagesize,this.currentPage*this.pagesize);
        // 获取查询的结果，把数组长度赋值给 分页组件中的total
        this.tableDate_length = list.length;
        this.tableData = list;

        return list,fenye
      }
      // 分页功能
     else {
       //所有数据的长度  赋值给分页组件中的total
       //  console.log('no condition_this.tabledata:');
       //  console.log(this.tableData);
        this.tableData = this.tableData_back;
        this.tableDate_length = this.tableDate_length_back
        let total = this.tableData;
        let fenye = total.slice((this.currentPage-1)*this.pagesize,this.currentPage*this.pagesize);

        //this.tableDate_length = total.length;
        return total,fenye
      }
  },
    computedSiteType(){
      return function (status){
        return this.options[status]['label']
      }
    },
  },

  methods :{
      initTable(){
        const _this = this;
        this.token = JSON.parse(this.$route.query.token);
        axios.get("http://192.168.1.151:8000/get_accounts?token="+this.token).then( res => {
        if(res.data.status_code === '200'){
            _this.tableData = res.data.account_list;
            _this.tableData_back = res.data.account_list;
            _this.tableDate_length = res.data.account_list.length;
            _this.tableDate_length_back = res.data.account_list.length;
            _this.pagesize = res.data.page_size;
          }else {
           _this.$router.push("/");
           _this.$message.info("请先登录");
         }
        }
          ).catch(error => {
          console.log(error)
        });

    },
     handleSizeChange: function (size) {
                this.pagesize = size;
                axios.get("http://192.168.1.151:8000/save_pagesize?pagesize="+this.pagesize+"&token="+this.token).then(res=>{
                  if(res.data.code==='200'){
                    //alert(res.data.message);
                  }

                })

        },
        handleCurrentChange: function(currentPage){
                this.currentPage = currentPage;
          //点击第几页
        },
     indexMethod(index) {
        return (index-1)*this.pagesize;
      },
      extract_file(){
      let table_data_list =  this.tableData;
      let array_store_row = [];
      let head_row = [];
      let col_row = [];
      for(let row in table_data_list){
           for(let key in table_data_list[row]) {
             head_row.push(key)
           }
           array_store_row.push(head_row);
           break;
           }
      for(let row in table_data_list){
           for(let key in table_data_list[row]) {
             col_row.push(table_data_list[row][key])
           }
           array_store_row.push(col_row);
           col_row = [];
           }
      let work_book = XLSX.utils.book_new();
      let sheet_product_info = XLSX.utils.aoa_to_sheet(array_store_row);
      XLSX.utils.book_append_sheet(work_book,sheet_product_info,'券商账户信息表');
      XLSX.writeFile(work_book,'券商账户信息表.xlsx');

    },

  }
}
</script>

<style scoped>

</style>
