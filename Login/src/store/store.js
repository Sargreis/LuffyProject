/**
 * Created by w1271 on 2017/11/27.
 */
// import Vue from 'vue'
// import Vuex from 'vuex'
// import Cookie from 'vue-cookie'
//
// Vue.use(Vuex)
//
// export default new Vuex.Store({
//   // 组件中通过 this.$store.state.username 调用
//   state: {
//     username: Cookie.get('user'),
//     token: Cookie.get('token'),
//     apiList: {
//       auth: 'http://127.0.0.1:8000/api/v1/auth/',
//       courses: 'http://127.0.0.1:8000/api/v1/courses/'
//     }
//   },
//   mutations: {
//     // 组件中通过 this.$store.commit(saveToken,参数)  调用
//     saveToken: function (state, user, token) {
//       state.username = user
//       Cookie.set('user', user, '20min')
//       Cookie.set('token', token, '20min')
//
//     },
//     clearToken: function (state) {
//       state.username = null
//       Cookie.remove('user')
//       Cookie.remove('token')
//
//     }
//   }
//
// })

import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookie'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    username: Cookie.get('user'),
    token: Cookie.get('tk'),
    code: Cookie.get('code'),
    apiList: {
      auth: 'http://127.0.0.1:8000/login',
      courses: 'http://127.0.0.1:8000/courses',
      CourseInfo: 'http://127.0.0.1:8000/courseinfo/'
    }
  },
  mutations: {
    saveToken: function (state, user) {
      console.log(user)
      state.username = user.user
      Cookie.set('user', user.user, '20min')
      Cookie.set('token', user.token, '20min')
    },
    clearToken: function (state) {
      state.username = null
      Cookie.delete('user')
      Cookie.delete('token')
    }
  }
})
