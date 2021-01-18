import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '*',
      redirect: '/'
    },
    {
      path: '/app',
      name: 'app',
      component: require('@/components/App').default
    },
    {
      path: '/',
      name: 'setup',
      component: require('@/components/SetUp').default
    }
    // {
    //   path: '/',
    //   name: 'start',
    //   component: require('@/components/Start').default
    // }
  ]
})
