import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '../components/UserLogin.vue'
import UserRegister from '../components/UserRegister.vue'
import PreferenceForm from '../components/PreferenceForm.vue'
import RecommendationList from '../components/RecommendationList.vue'
import DestinationDetail from '../components/DestinationDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister
  },
  {
    path: '/preference/:userId',
    name: 'Preference',
    component: PreferenceForm,
    props: true
  },
  {
    path: '/recommendations/:userId',
    name: 'Recommendations',
    component: RecommendationList,
    props: true
  },
  {
    path: '/destination/:destinationId',
    name: 'DestinationDetail',
    component: DestinationDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router