<template>
  <div id="index">
<h1>欢迎来到demo界面</h1>
    <p>
    <el-tooltip class="item" effect="dark" content="把邮箱中的附件放置在服务器的邮件账户分类保存目录中" placement="top-start">
        <el-button type="primary" @click="test()" v-preventReClick>第 一 步</el-button>
    </el-tooltip>
   <el-input v-model="input_1" style="width: 447px" disabled></el-input>
  </p>
  <p>{{msg}}
  </p>
    <hr>
    <block v-if="status">
      正确的话，你能看到我
    </block>
    <hr>
    <ol>
      <li v-for="(item,index) in list" :key="index">
        {{item.text}}
      </li>
    </ol>
  </div>
</template>

<script>
    import Vue from 'vue'
    const preventReClick = Vue.directive('preventReClick', {
    inserted: function (el, binding) {
        el.addEventListener('click', () => {
            if (!el.disabled) {
                el.disabled = true
                setTimeout(() => {
                    el.disabled = false
                }, binding.value || 2000)
            }
        })
    }
    });
    export default {
        name: "index",
        data(){
          return{
            msg:"Hello world",
            status:true,
            count : 0,
            list:[
              {text:'javascript'},
              {text:'vue'},
              {text:'示例项目'}
            ],


          }
        },
        mounted() {

        },
        methods :{
          test(){
            console.log(this.count++);
          }
        }
    }
    export{preventReClick}
</script>

<style scoped>

</style>
