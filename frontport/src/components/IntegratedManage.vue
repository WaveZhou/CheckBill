<template>

<el-row>
  <el-button>准备点击按钮</el-button>
  <el-button type="primary"  >第一步：把邮件中的附件放置在服务器的邮件账户分类保存目录中</el-button>
  <el-button type="success">第二步：把服务器的邮件账户分类保存目录中的文件复制到origin目录</el-button>
  <el-button type="info">第三步：把origin目录下的原始对账单数据根据交易日，按产品名和券商名分别进行归档整理</el-button>
</el-row>

<!--   <el-col :span="1">-->
<!--      <el-button-->
<!--        type="success"-->
<!--        @click="addCreate"-->
<!--        @keydown.enter="adddata"-->

<!--        size="mini"-->
<!--      >第一步：把邮件中的附件放置在服务器的邮件账户分类保存目录中</el-button>-->
<!--    </el-col>-->


<!--    <el-col :span="1">
      <el-button
        type="success"
        @click="addCreate"
        @keydown.enter="adddata"

        size="mini"
      >第二步：把服务器的邮件账户分类保存目录中的文件复制到origin目录</el-button>
    </el-col>

      <el-col :span="1">
      <el-button
        type="success"
        @click="addCreate"
        @keydown.enter="adddata"

        size="mini"
      >第三步：把origin目录下的原始对账单数据根据交易日，按产品名和券商名分别进行归档整理</el-button>
    </el-col>-->


</template>


<script>
  export default {
    name: "IntegratedManage",
    data() {
      const item = {
        date: '2021-11-17',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      };
      return {
        tableData: Array(20).fill(item)
        //icon="el-icon-circle-plus-outline"
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





