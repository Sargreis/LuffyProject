<template>
  <div>
    <h1>{{msg}}</h1>
    <h3>
      <p>
      <span>为什么学习:</span>{{detail.why_study}}
        </p>
      <p>
      <span>你将学会什么:</span>{{detail.what_to_study_brief}}
        </p>
      <p>
      <span>对我生涯有啥影响:</span>{{detail.career_improvement}}
      </p>
      <p>
        <span>课程先学要求:</span>{{detail.prerequisite}}
    </p>
    </h3>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        msg: '详情页面',
        detail: []
      }
    },
    mounted: function () {
      this.CourseDetail()
    },
    methods: {
      CourseDetail: function () {
        var self = this
        console.log(this.$route.params.id)
        this.axios.request({
          url: this.$store.state.apiList.CourseInfo + self.$route.params.id,
          method: 'GET',
          responseType: 'json'
        }).then(function (response) {
//          console.log(response.data)
          self.detail = response.data
          console.log(self.detail)
        })
      }
    }
  }
</script>
