import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Course from '@/components/index/Course'
import Deep from '@/components/index/Deep'
import Degre from '@/components/index/Degre'
import HomePage from '@/components/index/HomePage'
import Login from '@/components/account/Login'
import Detail from '@/components/courses/Detail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/course',
      name: 'Course',
      component: Course
    },
    {
      path: '/deep',
      name: 'deep',
      component: Deep
    },
    {
      path: '/degre',
      name: 'Degre',
      component: Degre
    },
    {
      path: '/',
      name: 'homepage',
      component: HomePage
    },
    {
      path: '/homepage',
      name: 'homepage',
      component: HomePage
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/course/detail/:id',
      name: 'Detail',
      component: Detail
    }
  ]
})
