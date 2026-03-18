import { createRouter, createWebHistory } from 'vue-router'
import UserLogin from '../components/UserLogin.vue'
import UserRegister from '../components/UserRegister.vue'
import PreferenceForm from '../components/PreferenceForm.vue'
import RecommendationList from '../components/RecommendationList.vue'
import DestinationDetail from '../components/DestinationDetail.vue'
import FoodRecommendation from '../components/FoodRecommendation.vue'
import SceneryIntroduction from '../components/SceneryIntroduction.vue'
import TravelGuide from '../components/TravelGuide.vue'
import WeatherQuery from '../components/WeatherQuery.vue'
import GroupBuyDeals from '../components/GroupBuyDeals.vue'
import DeepLearningShowcase from '../components/DeepLearningShowcase.vue'
import HomePage from '../components/HomePage.vue'

const routes = [
  {
    path: '/',
    redirect: '/recommendations'
  },
  {
    path: '/home',
    name: 'Home',
    redirect: '/recommendations'
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
    path: '/preference/:userId?',
    name: 'Preference',
    component: PreferenceForm,
    props: true
  },
  {
    path: '/recommendations/:userId?',
    name: 'Recommendations',
    component: RecommendationList,
    props: true
  },
  {
    path: '/destination/:destinationId',
    name: 'DestinationDetail',
    component: DestinationDetail,
    props: true
  },
  {
    path: '/food',
    name: 'FoodRecommendation',
    component: FoodRecommendation
  },
  {
    path: '/scenery',
    name: 'SceneryIntroduction',
    component: SceneryIntroduction
  },
  {
    path: '/guide',
    name: 'TravelGuide',
    component: TravelGuide
  },
  {
    path: '/weather',
    name: 'WeatherQuery',
    component: WeatherQuery
  },
  {
    path: '/groupbuy',
    name: 'GroupBuyDeals',
    component: GroupBuyDeals
  },
  {
    path: '/deeplearning',
    name: 'DeepLearningShowcase',
    component: DeepLearningShowcase
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router