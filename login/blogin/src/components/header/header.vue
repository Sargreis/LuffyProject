<template>
  <div class="outer">
    <div id="header">

      <!-- 导航栏-start -->
      <div class="resetBar">
        <div class="navbar navbar-inverse navbar-static-top">
          <div class="container">
            <div class="navbar-header">
              <button class="navbar-toggle" data-toggle="collapse" data-target="#togglemenu">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>

              <!--<a href="#" class="navbar-brand">LOGO</a>-->
              <a href="#/" class="navbar-brand">LOGO</a>
            </div>
            <div class="collapse navbar-collapse" id="togglemenu">
              <ul class="nav navbar-nav">
                <li>
                  <router-link to="/">首页</router-link>
                </li>
                <li>
                  <router-link to="/course">课程</router-link>
                </li>
                <li>
                  <router-link to="/degre">X学位</router-link>
                </li>
                <li>
                  <router-link to="/deep">深技术</router-link>
                </li>
              </ul>
              <!-- <button class="btn btn-default navbar-btn">按钮</button> -->
              <form class="navbar-form navbar-right">
                <div class="form-group">   <!-- 设定按钮组 -->
                  <div class="input-group">
                    <!-- 搜索框 -->
                    <!--<input type="text" name="" class="form-control" placeholder="Searching">-->
                                    <!--<span class="input-group-btn">-->
                                        <!--<button class="btn btn-default"><span class="glyphicon glyphicon-search"></span>-->
                                        <!--</button>-->
                                    <!--</span>-->
                    <!-- 搜索框 -->

                    <ul v-if="this.$store.state.username" class="loginButton">
                      <li>
                        <router-link to="#">{{ this.$store.state.username }}</router-link>
                      </li>
                      <li>
                        <a href="#" @click="logout()">注销</a>
                      </li>
                    </ul>

                    <ul v-else class="loginButton">
                      <li>
                        <router-link :to="{name:'Login', query:{backUrl: this.$route.path}}">登录</router-link>
                      </li>
                      <li>
                        <a href="#">注册</a>
                      </li>
                    </ul>
                  </div>

                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!-- 导航栏-over -->

    </div>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    },
    methods: {
      logout: function () {
        this.$store.commit('clearToken')
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .loginButton li{
    float:left;
    list-style: none;
  }
  .loginButton li a{
    display: inline-block;
    margin:0 5px;
    font-size: 17px;
    line-height: 35px;
    text-decoration: none;
  }
  .loginButton li a:hover{
    color: greenyellow;
  }
  #header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
  }

  .navbar-brand {
    color: white;
  }

  .router-link-exact-active {
    color: white !important;
    border-bottom: 2px solid red;
  }

  a {
    cursor: pointer;
  }

  .outer {
    height: 60px;
  }
</style>
