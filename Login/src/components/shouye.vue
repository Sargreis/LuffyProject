<template>
  <div>
    <h1>{{msg}}</h1>
    <!--<ul>-->
      <!--<li v-for="i in course_info">-->
        <!--<p><a href="#">{{i.name}}</a></p>-->
        <!--{{i.level_name}}-->
        <!--{{i.brief}}-->
      <!--</li>-->
    <!--</ul>-->
    <table>
      <tr v-for="i in course_info" style="border: solid 2px black">
        <td style="border: solid 2px black"><router-link :to="{'path':'courseinfo/'+i.id}">{{i.name}}</router-link></td>
        <td style="border: solid 2px black">{{i.level_name}}</td>
        <td style="border: solid 2px black">{{i.brief}}</td>
      </tr>
    </table>
  </div>


</template>


<script>
  export default {
    data () {
      return {
        msg: '这是首页',
        course_info: []
      }
    },
    mounted: function () {
      this.showlist()
    },
    methods: {
      showlist: function () {
        var self = this
        this.axios.request({
          url: this.$store.state.apiList.courses,
          method: 'GET',
          responseType: 'json'
        }).then(function (response) {
          self.course_info = response.data.data
          console.log(response.data)
        })
      }
    }
  }
</script>
