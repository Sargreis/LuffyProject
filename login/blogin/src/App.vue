<template>
  <div id="app">
    <heads></heads>
    <router-view/>
    <foots></foots>
  </div>
</template>

<script>
  import heads from "./components/header/header.vue"
  import foots from "./components/foot/foots.vue"

export default {
    components: {
      heads,
      foots
    },
    name: 'app'

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
