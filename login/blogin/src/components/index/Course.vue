<template>

  <div class="container">
    <!--<img class="img" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1511789653026&di=48c894a35c2fed9aca7d4c7f5ffd4308&imgtype=0&src=http%3A%2F%2Fg.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F8d5494eef01f3a29638ade289325bc315d607c91.jpg" alt="">-->
    <!--<img class="img" src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1511801423966&di=8e2ab0321b8ae48bfdfcd226f33d784e&imgtype=0&src=http%3A%2F%2Fwww.dngsw.cn%2Fuploads%2Fallimg%2F160810%2F287-150G31936155U363.jpg" alt="仙剑图片">-->

    <router-link style="margin: 15px; display: inline-block; justify-content: space-between" v-for="item in course_list" :to="{'path':'/course/detail/'+item.id}">
      <div style="width:350px; cursor: pointer">
        <div style="width:350px; height:238px">
          <div style="width:350px; height:238px; clear: both;overflow: hidden; zoom: 1"><img
            class="sub-img" src="http://luffy.oldboyedu.com/static/img/course-img1.f4ba499.png" width="350" height="238"></div>
        </div>
        <div style="width:350px; height:180px; display: flex; justify-content: center; box-shadow: 0 4px 2px 0 #E8E8E8">
          <div style="width: 301px; text-align: center"><h4 class="course-tit">{{item.name}}</h4>
            <p class="course-dec">{{item.brief}}</p> <span
              class="course-lever">难度：{{item.level}}</span></div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        course_list: []
      }
    },
    mounted: function () {
      this.getCourse()
    },
    methods: {
      getCourse: function () {
        var self = this
        this.$axios.request({
          url: this.$store.state.apiList.courses,
          method: 'GET'
        }).then(function (response) {
          self.course_list = response.data.data
        }).catch(function (response) {
          console.log(response)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .container{
    margin-top: 60px;
  }
  img{
    border-bottom: 3px solid #369;
  }
  li * {
    display: inline-block;
    margin-left: 20px;
  }
  a{
    color: black;
    text-decoration: none;
  }
  .img{
    width: 100%;
    display: block;
    text-align: center;
    margin: 15px auto;
  }

</style>
