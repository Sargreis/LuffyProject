/**
 * Created by Administrator on 2017/11/27.
 */
import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookies'

Vue.use(Vuex)

export default new Vuex.Store({
  // 组件中通过 this.$store.state.username 调用
  state: {
    username: Cookie.get('user'),
    token: Cookie.get('token'),
    apiList: {
      auth: 'http://127.0.0.1:8000/api/v1/auth/',
      courses: 'http://127.0.0.1:8000/api/v1/courses/',
      payment: 'http://127.0.0.1:8000/api/v1/shopping_cart/'
    }
  },
  mutations: {
    // 组件中通过 this.$store.commit(saveToken,参数)  调用
    saveToken: function (state, logInfo) {
      state.username = logInfo.username
      Cookie.set("user", logInfo.username, "20min")
      Cookie.set("token", logInfo.token, "20min")

    },
    clearToken: function (state) {
      state.username = null
      Cookie.remove('user')
      Cookie.remove('token')

    }
  },

})
