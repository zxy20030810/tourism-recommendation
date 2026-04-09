import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

const app = createApp(App)

// 配置axios
axios.defaults.timeout = 10000

app.config.globalProperties.$axios = axios

// 全局样式 - 修复导航栏文字颜色
const style = document.createElement('style')
style.textContent = `
  .nav-menu.el-menu--horizontal > .el-sub-menu .el-sub-menu__title {
    color: white !important;
  }
  .nav-menu .el-sub-menu__title .el-sub-menu__icon-arrow {
    color: white !important;
  }
`
document.head.appendChild(style)

app.use(router)
app.use(ElementPlus)
app.mount('#app')