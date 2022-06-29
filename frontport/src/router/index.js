import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import Login from '@/components/Login'
import DataManageCenter from "../components/DataManageCenter";
import Bills from "../components/Bills";
import AccountInformation from "../components/AccountInformation";
import IntegratedManage from "../components/IntegratedManage";
import AccountDetail from "../components/AccountDetail";
import EmailConfig from "../components/EmailConfig";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
       meta: {
        title: '登录界面'
      }
    },
    {
      path:'/Index',
      name:'Index',
      component:index,
      meta: {
        title: 'demo界面'
      }
    },
    {
      path: '/DataManageCenter',
      name:'DataManageCenter',
      component: DataManageCenter,
      meta: {
        title: '数据管理中心'
      }

    },
    {
      path: '/Bills',
      name:'Bills',
      component: Bills,
      meta: {
        title: '未到对账单管理'
      }
    }, {
      path: '/AccountInformation',
      name:'AccountInformation',
      component: AccountInformation,
      meta: {
        title: '券商账户信息维护'
      }},
     {
      path: '/AccountDetail',
      name:'AccountDetail',
      component: AccountDetail,
      meta: {
        title: '账户与对账单文件名配置'
      }},
    {
      path: '/IntegratedManage',
      name:'IntegratedManage',
      component: IntegratedManage,
      meta: {
        title: '对账单日常操作流程'
      }
    },
       {
      path: '/EmailConfig',
      name:'EmailConfig',
      component: EmailConfig,
      meta: {
        title: '邮箱地址配置'
      }
    },
  ],
    mode:'history',
})
