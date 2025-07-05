import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'  // 导入全局样式

const app = createApp(App)

app.use(createPinia())
    .use(router)
    .use(ElementPlus)
    .mount('#app') 