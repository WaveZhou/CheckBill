<template>
  <div class="hello">
    <div class="login_person">
      登陆人：{{user_name}}
    </div>

    <h1>{{ msg }}</h1>
    <hr style="border: #42b983" color="orange" size="5">
    <h2>可点击跳转到对应链接，目前仅对账单可行</h2>

    <ul>
      <li @click="query_bills">
        <a
          href="#"
          target="_blank"
        >对账单未到查询
        </a>
      </li>

      <li @click="manage_accountinfomation">
        <a
          href="#"
          target="_blank"
        >券商信息管理
        </a>
      </li>

      <li @click="integrated_manage">
        <a
          href="#"
          target="_blank"
        >
          净值查询
        </a>
      </li>
      <li>
        <a
          href="#"
          target="_blank"
        >
          持仓汇总查询
        </a>
      </li>
      <li>
        <a
          href="#"
          target="_blank"
        >
          产品嵌套查询
        </a>
      </li>
      <br>
      <li>
        <a
          href="#"
          target="_blank"
        >
          产品规模查询
        </a>
      </li>
    </ul>
    <h2>产品详情</h2>
    <ul>
      <li>
        <a
          href="#"
          target="_blank"
        >
          产品基本信息查询
        </a>
      </li>
      <li>
        <a
          href="#"
          target="_blank"
        >
          产品资产查询
        </a>
      </li>
      <li>
        <a
          href=""
          target="_blank"
        >
         产品历史分析
        </a>
      </li>
      <li>
        <a
          href="#"
          target="_blank"
        >
         投资人信息
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
  import axios from 'axios';
  import Qs from 'qs';
export default {
  name: 'DataManageCenter',
  data () {
    return {
      msg: '',
      user_name:'',
      user_id: this.$route.query.user_id
    }
  },
  mounted() {
    const _this = this;
    this.token = _this.$route.query.token;
    debugger;
    axios.get("http://127.0.0.1:8000/get_users?token="+this.token).then(res=>{
      //alert(res.data.user_obj.user_name);

      if(res.data.status_code === '302'){
            alert(res.data.message);
            _this.$router.push("/");
      }else if(res.data.status_code === '304'){
            alert(res.data.message);
            _this.$router.push("/");
      }
      else {
        _this.msg = '欢迎'+res.data.user_obj.user_name+'来到久铭投资数据维护管理中心'
        _this.user_name = res.data.user_obj.user_name
      }


    }).catch(err=>{
      _this.$router.push("/");
    })

  },
  methods:{
      query_bills(){
        //alert(this.$route.params.token);
        //this.$router.push({name:"Bills",params:{token:this.$route.params.token}});
        let jump_bills_page = this.$router.resolve({path:"/Bills",query:{token:JSON.stringify(this.$route.query.token)}});
        //let jump_page = this.$router.resolve({path:"/Bills", query:{token:this.$route.query.token}});
        window.open(jump_bills_page.href,'_blank');
      },
      manage_accountinfomation(){
        let jump_account_page = this.$router.resolve({path:"AccountInformation"})
        window.open(jump_account_page.href,'_blank');
      },
      integrated_manage(){
        let jump_center_page = this.$router.resolve({path:"IntegratedManage"})
        window.open(jump_center_page.href,'_blank');
      }
    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  color: crimson;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.login_person{
  float: left;
  margin-top: -42px;
  font-size: 30px;
  color: blue;
  line-height: 5px;
  font-style: italic;
  font-weight: bold;
  font-family: Arial,serif;
}
</style>
