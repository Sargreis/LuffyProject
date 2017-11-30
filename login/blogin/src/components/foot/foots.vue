<template>
  <div id="foot">
    <div class="footWrap foot">
      <div class="main">
        <ul class="foot-link"> <!--v-for-start-->
          <li>关于我们</li>
          <li>联系我们</li>
          <li>商务合作</li>
          <li>帮助中心</li>
          <li>意见反馈</li>
          <li>新手指南</li><!--v-for-end--> </ul>
        <p class="base-style">Copyright © luffy.com版权所有</p></div>
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
  .main{
    width: 450px;
  }
.footWrap{
    width: 100%;
    height: 128px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    background: #25292e;
}
  .foot-link>li {
    list-style: none;
    width: 14%;
    font-size: 14px;
    color: #fff;
    cursor: pointer;
    float: left;
    margin: 5px;
}
  li {
    display: list-item;
    text-align: -webkit-match-parent;
}
  .base-style {
    font-size: 14px;
    color: #fff;
    /*display: -webkit-box;*/
    /*display: -ms-flexbox;*/
    /*display: flex;*/
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
}
</style>
