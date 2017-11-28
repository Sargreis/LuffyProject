<template>
  <div class="hello">
    <!--<h1>{{ msg }}</h1>-->
    <!--<h2>Essential Links</h2>-->
    <!--<ul>-->
      <!--<li><a href="https://vuejs.org" target="_blank">Core Docs</a></li>-->
      <!--<li><a href="https://forum.vuejs.org" target="_blank">Forum</a></li>-->
      <!--<li><a href="https://chat.vuejs.org" target="_blank">Community Chat</a></li>-->
      <!--<li><a href="https://twitter.com/vuejs" target="_blank">Twitter</a></li>-->
      <!--<br>-->
      <!--<li><a href="http://vuejs-templates.github.io/webpack/" target="_blank">Docs for This Template</a></li>-->
    <!--</ul>-->
    <!--<h2>Ecosystem</h2>-->
    <!--<ul>-->
      <!--<li><a href="http://router.vuejs.org/" target="_blank">vue-router</a></li>-->
      <!--<li><a href="http://vuex.vuejs.org/" target="_blank">vuex</a></li>-->
      <!--<li><a href="http://vue-loader.vuejs.org/" target="_blank">vue-loader</a></li>-->
      <!--<li><a href="https://github.com/vuejs/awesome-vue" target="_blank">awesome-vue</a></li>-->
    <!--</ul>-->
    <p v-for="item in arr">{{item}}</p>
    <h1>{{$store.state.username}}</h1>
    <p>用户名：<input type="text" placeholder="username" id="username" v-model="username"></p>
    <p>密码：  <input type="password" placeholder="password" id="password" v-model="password"></p>
    <p><input type="button" value="sign in" id="sign" v-on:click="login"></p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
//      msg: 'Welcome to Your Vue.js App'
      arr: [],
      username: 'alex',
      password: '123'
    }
  },
  mounted: function () {
    this.sign()
  },
  methods: {
    sign: function () {
      var url = this.HOST + '/test/'
      var self = this
      this.axios.get(url).then(function (response) {
        self.arr = response.data
        console.log(response.data)
      })
    },
    login: function () {
      var data = {username: this.username, password: this.password}
      var self = this
      this.axios.request({
        url: this.$store.state.apiList.auth,
        method: 'POST',
        data: data,
        responseType: 'json'
      }).then(function (response) {
        if (response.data.code === 200) {
          console.log(response.data)
//          self.$store.commit('saveToken', response.data.username, response.data.token)
          self.$store.commit('saveToken', {'user': response.data.username, 'token': response.data.token})
          let backUrl = self.$route.query.backurl
          self.$router.push(backUrl)
        } else {
          alert(response.data.msg)
        }
      })
    }
//    login: function () {
//      var url = this.HOST + '/login/'
//      var self = this
//      this.axios.post(url, {'username': self.username, 'password': self.password}).then(function (response) {
//        console.log(response.data.token)
//        console.log(response.data.code)
//        self.$cookie.set('tk', response.data.token)
//        self.$cookie.set('user', self.username)
//        self.$cookie.set('code', response.data.code)
//        console.log(self.$store)
//      })
//    }





//      sign: function () {
//        var url = 'api/index/'
//        var self = this
//        this.axios.get(url).then(function (response) {
//          self.arr = response.data
//          console.log(self.arr)
//        })
//      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
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
</style>
