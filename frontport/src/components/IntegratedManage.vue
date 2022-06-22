<template>

<el-row>
   <h1 align="center">对账单日常操作流程</h1>
  <br/>
  <p>
    <el-tooltip class="item" effect="dark" content="把邮件中的附件放置在服务器的邮件账户分类保存目录中" placement="top-start">
        <el-button type="primary" @click="firstStep()">第 一 步</el-button>
    </el-tooltip>
   <el-input v-model="input_1" placeholder="请输入内容" style="width: 447px"></el-input>
  </p>

  <br/>
  <p >
     <el-tooltip class="item" effect="dark" content="把服务器的邮件账户分类保存目录中的文件复制到origin目录" placement="top-start">
        <el-button type="success" @click="secondStep()" id="two" >第 二 步</el-button>
    </el-tooltip>
     <el-input v-model="input_2" placeholder="请输入内容" style="width: 447px"></el-input>
  </p>

 <br/>
  <p>
    <el-tooltip class="item" effect="dark" content="把origin目录下的原始对账单数据根据交易日，按产品名和券商名分别进行归档整理" placement="top-start">
        <el-button type="info" @click="thirdStep()" id="three">第 三 步</el-button>
    </el-tooltip>
     <el-input v-model="input_3" placeholder="请输入内容" style="width: 447px"></el-input>
  </p>


</el-row>



</template>


<script>
 import axios from 'axios';

 import Qs from 'qs';
  export default {
    name: "IntegratedManage",
    data() {
      return {
        input_1 : '',
        input_2 : '',
        input_3 : '',

        //icon="el-icon-circle-plus-outline"
      }
    },
    methods:{
      firstStep(){
         this.input_1 = '处理中。。。。。。'
         axios.get("http://127.0.0.1:8000/first_step").then(res=>{
                  if(res.data.code ==='200'){
                    console.log(res.data.message);
                    this.input_1 = res.data.message;
                     document.getElementById('two').disabled = false;
                      //假设这两百是第一次运行成功后，再次请求后台的
                    axios.get("http://127.0.0.1:8000/first_step?flag="+'200').then(
                      res => {
                        if(res.data.code === '200'){
                          this.input_1 = res.data.message;
                        }else {
                           this.input_1 = res.data.message;
                        }

                      }
                    )
                  }else if(res.data.code === '302'){
                     this.input_1 = res.data.message;
                     this.$message.warning("请将文本框显示的报错提交技术人员处理");
                     console.log(res.data.message)

                  }
                })
      },
      secondStep(){
        let first_content = this.input_1
        if(first_content !== '第一步执行成功'){
           document.getElementById('two').disabled = true;
          this.input_2 = '请先完成第一步';
          return;
        }
        this.input_2 = '处理中。。。。。。'
        axios.get("http://127.0.0.1:8000/two_step").then(res =>{
              if(res.data.code === '200'){
                this.input_2 = res.data.message;
              }
        })


        //返回值正常时，把第三步disable的属性值设置为false
      },

      thirdStep(){
        let second_content = this.input_2
        if(second_content !== '第二步执行成功'){
           document.getElementById('three').disabled = true;
          this.input_3 = '请先完成第二步';
          return;
        }
        this.input_3 = '处理中。。。。。。'
        axios.get("http://127.0.0.1:8000/three_step").then(res =>{
             if(res.data.code === '200'){

                this.input_3 = res.data.message;
                this.$message.success('可去对账单未到页面查看了')
              }else if(res.data.code === '302'){
                console.log(res.data.message)
                this.input_3 = res.data.message;
                this.$message.error("报错信息提交给相关技术处理")

             }
        })
      }
    }
  };
</script>



<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }

  .el-aside {
    color: #333;
  }
</style>





