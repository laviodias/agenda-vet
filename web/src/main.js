import { createApp } from 'vue'
import './main.scss'
import App from './App.vue'
import '@fortawesome/fontawesome-free/css/all.css'
import router from './router'
import 'bulma/css/bulma.min.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
