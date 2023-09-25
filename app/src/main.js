import './assets/main.css'
import './assets/style.scss'


import { createApp } from 'vue'
import App from './App.vue'

// createApp(App).mount('#app')

// Import only the Bootstrap components we need
import { Popover } from 'bootstrap';

const app = createApp(App)

fetch("./config.json")
  .then((response) => response.json())
  .then((config) => {
    // either use window.config
    window.config = config
    // or use [Vue Global Config][1]
    app.config.globalProperties.config = config
    // FINALLY, mount the app
    app.mount("#app")
  })



