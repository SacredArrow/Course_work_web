import Vue from 'vue'
import App from './App.vue'
// import './../node_modules/bulma/css/bulma.css';
import './assets/sass/main.scss'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons'


import Axios from 'axios'

library.add(faGithub)
library.add(faUserSecret)

Vue.component('font-awesome-icon', FontAwesomeIcon)
// <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
// import './styles/my-styles.scss'



Vue.prototype.$http = Axios;

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
