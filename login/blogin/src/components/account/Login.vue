<template>
  <div class="outter">
    <h1 class="title">Login</h1>
    <p>
      <label for="username">Username </label>
      <input class="form-control" type="text" id="username" placeholder="Username" v-model="username">
    </p>
    <p>
      <label for="password">Password</label>
      <input class="form-control" type="password" id="password" placeholder="Password" v-model="password">
    </p>
    <span v-show="show" class="error_info">{{ error_info }}</span>
    <p>
      <input type="button" value="登录" class="btn btn-primary btn-block" v-on:click="login">
    </p>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        username: 'admin',
        password: 'admin',
        error_info: '',
        show: false
      }
    },
    methods: {
      login () {
        var data = {username: this.username, password: this.password}
        var self = this
        this.$axios.request({
          url: this.$store.state.apiList.auth,
          method: 'POST',
          data: data,
          responseType: 'json'
        }).then(function (response) {
          if (response.data.code === 1002) {
            self.show = false

            // 设置cookie
            self.$store.commit('saveToken', {username: response.data.username, token: response.data.tk})
            // 跳转页面
            let backUrl = self.$route.query.backUrl
            if (backUrl){
              self.$router.push(backUrl)
            } else {
              self.$router.push('/homepage')
            }

          } else if (response.data.code === 1001) {
            self.show = true;
            self.error_info = '用户名或密码错误';

          }
        }).catch(function (response) {
          console.log(response)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .outter {
    width: 400px;
    margin: 100px auto 200px;;
    position: relative;
  }

  label {
    float: left;
  }

  p {
    margin-top: 10px;
  }

  #username, #password {
    text-indent: 6px;
  }

  .error_info {
    color: red;
    float: right;
    position: relative;
    top: -5px;
  }
</style>
