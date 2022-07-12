// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import HeyUI from 'heyui'
import  * as tools from './components/AccountInformation'
Vue.use(ElementUI);
Vue.use(HeyUI);
Vue.prototype.$tools = tools;

Vue.config.productionTip = false;
import VueWechatTitle from 'vue-wechat-title'
Vue.use(VueWechatTitle);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
// router.beforeEach((to, from, next) => {
//   /* 路由发生变化修改页面title */
//   if (to.meta.title) {
//     document.title = to.meta.title
//   }
//   next()
//   })
// router.afterEach(to => {
// 	// 设置title
// 	document.title = to.meta.title;
// })

