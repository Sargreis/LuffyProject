import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import shouye from '@/components/shouye'
import courseinfo from '@/components/courseinfo'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'shouye',
      component: shouye
    },
    {
      path: '/courseinfo/:id',
      name: 'courseinfo',
      component: courseinfo
    }
  ]
})
