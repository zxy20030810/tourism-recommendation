import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

const app = createApp(App)

// 配置axios
axios.defaults.baseURL = '/api'
axios.defaults.timeout = 10000

app.config.globalProperties.$axios = axios

app.use(router)
app.use(ElementPlus)
app.mount('#app')