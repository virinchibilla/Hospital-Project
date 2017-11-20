import Vue from 'vue'
import VueRouter from 'vue-router'
import Signin from '@/components/Signin'
import Signup from '@/components/Signup'
import Welcome from '@/components/Welcome'

Vue.use(VueRouter)

const routes = [
{ path: '/signup', name: 'Signup', component: Signup },
{ path: '/welcome', name: 'Welcome', component: Welcome },
{ path: '/*', name: 'Signin', component: Signin }
]

const router = new VueRouter({
  // mode: 'history',
  routes
})

export default router
