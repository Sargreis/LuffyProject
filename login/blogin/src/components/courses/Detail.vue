<template>
  <div class="detail">
    <!--<h1>Detail</h1>-->
    <!--<h4 v-for="(v, k) in detail_info">{{k}}:{{v}}</h4>-->
    <!--<div class="price">-->
    <!--<div class="outer">-->
    <!--<p>￥ 9.9</p>-->
    <!--<p>有限期1个月</p>-->
    <!--</div>-->
    <!--<div class="outer">-->
    <!--<p>￥ 9.9</p>-->
    <!--<p>有限期1个月</p>-->
    <!--</div>-->
    <!--<div class="outer">-->
    <!--<p>￥ 9.9</p>-->
    <!--<p>有限期1个月</p>-->
    <!--</div>-->
    <!--</div>-->


    <div>
      <div>
        <h1 class="title">{{detail_info.course.courses}}</h1>
        <!--<h4 class="desc">{{detail_info.career_improvement}}</h4>-->
      </div>
      <div></div>
    </div>

    <div class="cont-head" style="background: #FFFFFF;box-shadow: 0 1px 0 0 #E8E8E8">
      <ul class="cont-head-wrap">
        <li v-for="v,k in tabDict" :class="{hactive:tabKey==k}" @click="tabChoice(k)">{{v}}</li>
      </ul>
      <div class="content">
        <div v-if="tabKey==1">
          <!--{{detail_info}}-->
          <h2>课程概述</h2>
          {{detail_info.course.brief}}
          <hr>
          <h2>课程价格</h2>
          <div class="price">
            <ul>
                <li v-for="item in detail_info.course.pricePolicy" v-on:click="ChoosePrice(item.id)">
                  <label>
                    <p>{{item.price}}</p>
                    <span>{{item.valid_period}}</span>
                  </label>
                </li>
            </ul>
          </div>
          <div class="button">
            <input type="button" class="btn btn-danger" value="立即购买">
            <input type="button" class="btn btn-warning" value="加入购物车" v-on:click="buy(detail_info.course.id)">
          </div>
        </div>
        <div v-if="tabKey==2">
          <div v-for="i in detail_info.chapter">
            <h3><a href="#">{{i.name}}</a></h3>
            {{i.summary}}
          </div>
        </div>
        <div v-if="tabKey==3">
          <p>双击666.。。。</p>
          <p>功能未开。。。。</p>
        </div>
        <div v-if="tabKey==4">
          <p>功能未开。。。</p>
          <p>没啥问题</p>
        </div>
      </div>
    </div>

    <div class="price">
      <ul>
        <!--<li :class="{pactive:day==item.day}" v-for="item in detail_info.pricePolicy" :day="item.day"-->
            <!--@click="getPrice(item.day)"><p>￥ {{item.price}}</p>-->
          <!--<p>有效期{{item.valid_period}}</p></li>-->
      </ul>
    </div>



  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        detail_info: {},
        day: 0,
        tabDict: {1: '课程概述', 2: '课程章节', 3: '用户评价', 4: '常见问题'},
        tabKey: 1,
        price_id : ''
      }
    },
    mounted: function () {
      this.getDetail()
    },
    methods: {
      getDetail: function () {
        var self = this
        let course_id = this.$route.params.id;
        this.$axios.request({
          url: this.$store.state.apiList.courses + course_id + '/',
          method: 'GET',
        }).then(function (response) {
          self.detail_info = response.data.data
          console.log('111111111111111')
          console.log(response.data.data.course)
//          console.log(response.data.data)
//          console.log(typeof(response.data.data.pricePolicy))
//          self.price = window.JSON.parse(response.data.data.pricePolicy)
        })
      },
      ChoosePrice: function (arg) {
        this.price_id=arg
//        alert(this.$store.state.token)
      },
      buy: function (arg) {
        alert('进入购物和')
        if (this.price_id){
          if (this.$store.state.token){
            alert('有token')
            var data = {'price_id':this.price_id,'course_id':arg}
            this.$axios.request({
              url: this.$store.state.apiList.payment + '?' + 'token=' + this.$store.state.token,
              method: 'POST',
              data: data
            })
          }
        }else {
          alert('选择价格策略')
        }
      },
      getChapter: function () {
        var self = this
      },
      getPrice: function (day) {
        this.day = day
      },
      tabChoice: function (key) {
        this.tabKey = key
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .button input {
    margin: 0 28px;
    padding: 17px 97px;
    border-radius: 27px;
  }

  .price li {
    display: inline-block;
    border: 1px solid black;
    width: 150px;
    padding: 17px 0;
    margin: 23px;
    cursor: pointer;
    font-size: 20px;
    text-align: center;
  }

  .detail > div {
    margin: 25px 0;
  }

  .price ul .pactive {
    background-color: #00d6b2;
    border: 1px solid #00d6b2;
    color: white;
  }

  .price li:hover {
    background-color: #00d6b2;
    border: 0;
    color: white;
  }
  .price li:active {
    background-color: red;
    border: 0;
    color: white;
  }
  .detail {
    margin-top: 60px;
  }

  h4 {
    text-align: center;
    text-indent: 200px;
    margin-top: 35px;
  }

  .outer {
    height: 100px;
    width: 200px;
    display: inline-block;
    background-color: #00d6b2;
    margin: 40px;
    cursor: pointer;
  }

  .outer:hover {
    background-color: #77FFFF;
  }

  .price {
    text-align: center;
  }

  .title {
    font-size: 55px;
    text-align: center;
  }

  .desc {
    font-size: 25px;
    text-align: center;
  }

  .cont-head {
    width: 100%;
    /*height: 80px;*/
    background: #fafbfc;
  }

  .cont-head-wrap {
    width: 590px;
    margin: 0 auto;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
  }

  .cont-head-wrap li {
    height: 80px;
    line-height: 80px;
    font-size: 16px;
    color: #555;
    cursor: pointer;
  }

  li {
    list-style: none;
  }

  ul {
    padding: 0;
  }

  .hactive {
    border-bottom: 2px solid #78c63f;
  }

  p {
    display: block;
  }
  .content{
    /*text-align: center;*/
  }
  .content div{
    width: 600px;
    margin: 20px auto 100px;
    text-align: justify;
  }
</style>
