import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Main',
    component: () => import('../views/Main.vue'),
    children: [
      {
        path: 'home',
        alias: '',
        name: 'Home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'ranking',
        name: 'Ranking',
        component: () => import('../views/Ranking.vue')
      },
      {
        path: 'classify',
        name: 'Classify',
        component: () => import('../views/Classify.vue')
      },
      {
        path: 'my',
        name: 'My',
        component: () => import('../views/My.vue')
      }   
    ]
  },
  {
    path: '/detail/:pid',
    name: 'Detail',
    component: () => import('../views/Detail.vue')
  },
  {
    path: '/cartoon/:cid/:id',
    name: 'Cartoon',
    component: () => import('../views/Cartoon.vue')
  },
  {
    path: '/myLogin',
    name: 'MyLogin',
    component: () => import('../views/loginCom.vue')
  },
]

const router = new VueRouter({
  routes
})

export default router
