<template>
    <div class="cantainer" header-cell-style="color:red">
      <h1 style="margin-left: -26px">邮箱账户与邮件保存目录关联配置</h1>
      <el-row :gutter="40">

  <el-col :span="4"><div class="grid-content bg-purple"><el-input v-model="jiuming_input" placeholder="请输入久铭邮箱号或机构目录进行搜索"></el-input></div></el-col>
  <el-col :span="4" :offset="1"><div class="grid-content bg-purple"><el-button type="primary" plain @click="search_jiuming">点击搜索久铭邮箱配置</el-button> </div></el-col>

  <el-col :span="4" :offset="7"><div class="grid-content bg-purple"> <el-input v-model="jingjiu_input" placeholder="请输入静久邮箱号或机构目录进行搜索"></el-input> </div></el-col>
  <el-col :span="4"><div class="grid-content bg-purple"><el-button type="primary" plain @click="search_jingjiu">点击搜索静久邮箱配置</el-button></div></el-col>
</el-row>

      <hr style="border: #42b983" color="orange" size="5">

    <div class="parent_div">
       <div class="table_inline_jiuming">
    <el-table
      :data="jiuming_tableData.slice((currentPage_jiu-1)*pagesize_jiu,currentPage_jiu*pagesize_jiu)"
      style="width: 100%;">


      <el-table-column
        prop="mail_account"
        label="邮箱账号"
        width="270">
      </el-table-column>
      <el-table-column
        prop="institution"
        label="关联目录"
        width="250">
      </el-table-column>


      <el-table-column label="操作" class-name="operations">

        <template slot-scope="scope"  >

          <div class="parent_div" style="margin-left: 3px;">

            <div class="button_inline_left">
             <el-button
                :disabled=change_Click
            size="mini"
            @click="handleEdit(scope.$index, scope.row,1)">编辑</el-button>
            </div>
          <div class="button_inline_right">
            <el-button
               :disabled=change_Click
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row,1)">删除</el-button>
          </div>

          </div>
          </template>
      </el-table-column>

    </el-table>
     </div>
  <div class="table_inline_jingjiu">
      <el-table
      :data="jingjiu_tableData.slice((currentPage_jing-1)*pagesize_jing,currentPage_jing*pagesize_jing)"
      style="width: 100%;">
      <el-table-column
        prop="mail_account"
        label="邮箱账号"
        width="270">
      </el-table-column>
      <el-table-column
        prop="institution"
        label="关联目录"
        width="250">
      </el-table-column>
      <el-table-column label="操作" class-name="operations">


        <template slot-scope="scope">

         <div class="parent_div" style="margin-left: 3px;">
          <div class="button_inline_left">
          <el-button
            :disabled=change_Click
            size="mini"
            @click="handleEdit(scope.$index, scope.row,2)">编辑</el-button>
          </div>
           <div class="button_inline_right">
          <el-button
             :disabled=change_Click
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row,2)">删除</el-button>
           </div>

           </div>
</template>
      </el-table-column>
    </el-table>
</div>

</div>

       <hr style="border: #42b983" color="orange" size="5">
      <div class="parent_div">
      <div class="page_inline_jiuming">
     <el-pagination
            background
            @size-change="handleSizeChangeJiu"
            @current-change="handleCurrentChangeJiu"
            :current-page="currentPage_jiu"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pagesize_jiu"
             layout="total,sizes, prev, pager, next"
            :total="jiuming_tableData.length">
    </el-pagination>
    </div>
    <div class="page_inline_jingjiu">
      <el-pagination
            background
            @size-change="handleSizeChangeJing"
            @current-change="handleCurrentChangeJing"
            :current-page="currentPage_jing"
            :page-sizes="[5, 10, 15, 20]"
            :page-size="pagesize_jing"
             layout="total,sizes, prev, pager, next"
            :total="jingjiu_tableData.length">
     </el-pagination>
    </div>
</div>
      <div class="parent_div">
      <div class="inline-button-left">
      <el-col :span="1">
      <el-button
         :disabled=change_Click
        type="success"
        @click="addCreate(1)"

        icon="el-icon-circle-plus-outline"
        size="mini"
      >新增配置</el-button>
      </el-col>
        </div>

      <div class="inline-button-right">
      <el-col :span="1">
      <el-button
         :disabled=change_Click
        type="success"
        @click="addCreate(2)"
        icon="el-icon-circle-plus-outline"
        size="mini"
      >新增配置</el-button>
      </el-col>
      </div>

    </div>
    <el-dialog title="新增邮箱账户对应邮件保存目录" :visible.sync = 'emailAddDialog'>
      <el-form :model="ruleForm"  :rules="rules"  ref="ruleForm"   label-width="80px" class="demo-ruleForm">
        <el-form-item label="邮箱账号" prop="mail_account">
          <el-input v-model="ruleForm.mail_account" placeholder="请输入邮箱账号"></el-input>
        </el-form-item>
        <el-form-item label="证券机构" prop="institution">
          <el-input v-model="ruleForm.institution" placeholder="请输入该邮箱账号所发对账单的券商和账户类型，如兴业普通"></el-input>
        </el-form-item>
      </el-form>
       <div slot="footer" class="dialog-footer">
      <el-button @click="emailAddDialog = false">取 消</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
      <el-button type="primary" @click="confirnAdd('ruleForm')">确 定</el-button>
        </div>
    </el-dialog>

      <el-dialog title="编辑邮箱账户与券商对账单保存目录" :visible.sync="emailEditDialog">
      <el-form :model="editForm"  :rules="rules"  ref="editForm"   label-width="80px" class="demo-editForm">
          <el-form-item label="邮箱账户" prop="mail_account">
            <el-input v-model="editForm.mail_account" placeholder="请输入发对账单所属的邮箱账户"></el-input>
          </el-form-item>
          <el-form-item label="保存目录" prop="institution">
            <el-input v-model="editForm.institution" placeholder="请输入该邮箱账户所属券商机构"></el-input>
          </el-form-item>

       </el-form>
       <div slot="footer" class="dialog-footer">
       <el-button @click="emailEditDialog = false">取 消</el-button>
       <el-button type="primary" @click="update('editForm')">确 定</el-button>
       </div>
     </el-dialog>

    </div>
</template>


<script>
import axios from "axios";

export default {
  name: "EmailConfig",
  data(){
    return {
          token: this.$route.query.token,
          change_Click: false,
          authentication_code: '',
          currentPage_jiu : 1,
          pagesize_jiu : 10,
          currentPage_jing : 1,
          pagesize_jing : 10,
          emailAddDialog : false,
          emailEditDialog : false,
          jiuming_tableData: [],
          jingjiu_tableData:[],
          jiuming_input:'',
          jingjiu_input:'',
          ruleForm : {
            mail_account: "",
            institution: "",
          },
          editForm :{
            mail_account: "",
            institution: "",
          },

          rules:{
          mail_account:[
          { required: true, message: '请填写符合邮箱格式的字符串', trigger: 'blur'},
          { type: 'email', message: '请输入正确的邮箱号', trigger: ['change','blur']}
        ],institution :[
           { required: true, message: '请输入券商机构名称作为邮件保存目录', trigger: 'blur' },
        ]
      },


        }
  },
  mounted() {
    this.initiateConfig();
  },
  methods :{
        initiateConfig(){
           let  _this = this;
           axios.get("http://192.168.1.151:8000/get_email_config?token="+this.token).then(res=>{
              if(res.data.status_code === 200){
                  this.jiuming_tableData = res.data.result_list_jiuming;
                  this.jingjiu_tableData = res.data.result_list_jingjiu;
                  this.change_Click = res.data.authentication_code === 0;
              }
          }).catch(
            res =>{
            }
          )
        },
      handleEdit(index,row,flag){
          this.emailEditDialog = true;
          this.editForm.mail_account = row['mail_account'];
          this.editForm.institution = row['institution'];
          this.editForm.edit_condition = row['mail_account']+ '_' + row['institution']+'_'+flag;

      },

      handleDelete(index,row,flag){
          let _this = this;
          this.$confirm("确认删除吗").then(
            _ =>{
              axios.get("http://192.168.1.151:8000/delete_jiuming_email_config?mail_account="+row['mail_account']+"&institution="+row['institution']+"&flag="+flag).then(
                res => {
                  if(res.data.status_code === 200){
                    if( flag === '1'){
                      _this.search_jiuming();

                    }else {
                      _this.search_jingjiu();
                    }



                  }
                }
              ).catch(
                res =>{
                  console.log(res);
                }
              )
            }
          ).catch(
            _ =>{
            }

          )


      },
      update(formName) {

      this.$refs[formName].validate((valid) => {
        if(valid){
          axios.post('http://192.168.1.151:8000/update_jiuming_email_config',this.editForm).then(res => {
            if(res.data.status_code === 200){
              this.$message.success(res.data.message);
            }else if(res.data.status_code === 302){
              this.$message.error(res.data.message);
            }

            this.emailEditDialog = false;
            this.initiateConfig();
          }).catch(
            error => {
              console.log('修改异常'+ error);
            }
          )
          this.dialogFormVisible = false;
        }else {
          this.$message.error('表单数据未填写完整，修改失败');
          return false;
        }
        }
      );

    },
             // 初始页currentPage、初始每页数据数pagesize和数据data
        handleSizeChangeJiu: function(size) {
                this.pagesize_jiu = size;
                // axios.get("http://192.168.1.151:8000/save_pagesize?pagesize="+this.pagesize+"&token="+this.token).then(res=>{
                //   if(res.data.code=='200'){
                //     //alert(res.data.message);
                //   }
                //
                // })
        //
        },
        handleCurrentChangeJiu: function(currentPage){
                this.currentPage_jiu = currentPage;
          //点击第几页
        },
        handleSizeChangeJing: function(size) {
                this.pagesize_jing = size;
                // axios.get("http://192.168.1.151:8000/save_pagesize?pagesize="+this.pagesize+"&token="+this.token).then(res=>{
                //   if(res.data.code=='200'){
                //     //alert(res.data.message);
                //   }
                //
                // })
        //
        },
        handleCurrentChangeJing: function(currentPage){
                this.currentPage_jing = currentPage;
          //点击第几页
        },
        addCreate : function(flag){
          this.ruleForm.flag = flag;
          this.emailAddDialog = true;
        },
        resetForm(formName){
          this.$refs[formName].resetFields();
        },
        confirnAdd(formName) {
              //准备把新增数据发往后台
          this.$refs[formName].validate((valid) => {
            if(valid){
              axios.post('http://192.168.1.151:8000/add_email_config?flag='+this.ruleForm.flag,this.ruleForm).then(res => {
                if(res.data.status_code === 200){
                  this.emailAddDialog = false;
                  this.$message.success(res.data.message);
                }else if(res.data.status_code === 302){
                  this.emailAddDialog = true;
                  this.$message.error(res.data.message);
                }
                 this.initiateConfig();

              }).catch(
                error => {
                  console.log('新增异常'+ error);
                }
              )

            }else {
              this.$message.error('表单数据未填写完整，新增失败');
              return false;
            }
            }
          );
        },

        search_jiuming(){
          let _this = this
          axios.get("http://192.168.1.151:8000/search_jiuming?search_words="+this.jiuming_input).then(res=>{
                if(res.data.status_code === 200){
                   _this.$message.success(res.data.message);
                   _this.jiuming_tableData = res.data.result_list;
                   // _this.initiateConfig();
                }

          }).catch()
        },
        search_jingjiu(){
           let _this = this
          axios.get("http://192.168.1.151:8000/search_jingjiu?search_words="+this.jiuming_input).then(res=>{
                if(res.data.status_code === 200){
                  _this.$message.success(res.data.message);
                  _this.jingjiu_tableData = res.data.result_list;
                  // _this.initiateConfig();
                }

          }).catch()
        }
    }
}


</script>

<style scoped>
@import url(../../node_modules/element-ui/lib/theme-chalk/index.css);
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .table_inline_jiuming{
    float: left;
  }
  .table_inline_jingjiu{
    float: right;
  }
  .parent_div{
    overflow: hidden;
  }
  .page_inline_jiuming{
    float: left;
  }
  .page_inline_jingjiu{
    float: right;
  }
  .button_inline_left{
    float: left !important;

  }
  .button_inline_right{
    float: right !important;
  }
  .inline-button-left{
    float: left;
  }
  .inline-button-right{
    float: right;
  }
  #operator{
    /*margin-left: 15px;*/
  }
  /deep/ th.operations{
    padding-left: 15px !important;
}
  /deep/ div.grid-content.bg-purple{
    background-color: white;
  }
</style>
