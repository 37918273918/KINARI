import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Manage',
    component: () => import(/* webpackChunkName: "about" */ '../views/Manage.vue'),
    redirect:"/home",
    children:[
      {
        path: 'home',
        name: 'Home',
        component: () => import(/* webpackChunkName: "about" */ '../views/home1.vue')
      },
     /* // {
      //   path: 'protein',
      //   name: 'protein',
      //   component: () => import(/!* webpackChunkName: "about" *!/ '../views/Home.vue'),
      //
      // },*/
      {
        path: 'data',
        name: 'data',
        component: () => import(/* webpackChunkName: "about" */ '../views/data.vue'),

      }
    ]
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
