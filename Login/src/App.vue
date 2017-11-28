<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <h3>
      <span v-if="this.$store.state.username">
      <router-link to="#">{{this.$store.state.username}}</router-link>
      <a href="#" v-on:click="logout">注销</a>
      </span>
      <span v-else>
        <router-link :to="{name:'HelloWorld',query:{backurl: this.$route.path}}">login</router-link>

      </span>
    </h3>
    <router-link to="/">shouye</router-link>
    {{$store.state.code}}
    <router-view/>


  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      msg: 'vue'
    }
  },
  methods: {
    logout: function () {
      this.$store.commit('clearToken')
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
