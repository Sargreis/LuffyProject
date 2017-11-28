// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import cookie from 'vue-cookie'
import store from './store/store'

Vue.config.productionTip = false
Vue.prototype.axios = axios
// this.axios.request({
//   url: this.axios.state.apiList.auth,
//   method: 'POST',
//   data: {
//     username: this.username,
//     password: this.password
//   }
// })
Vue.use(router)
Vue.use(cookie)
/* eslint-disable no-new */
Vue.prototype.HOST = '/api'
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  store
})
