import { createRouter, createWebHistory } from 'vue-router'
import AdminPage from '../views/AdminPage.vue'
import { getDeviceType  } from '../utlis/device.js'
import EmployeePage from '../views/EmployeePage.vue'
import NotAllowed from '../components/NotAllowed.vue'
import OwnerLoginPage from '../views/Owner/LoginPage.vue'
import OwnerDashBoard from '../views/Owner/DashBoard.vue'

let device = getDeviceType();

let routes = [
  {
    path: '/admin',
    component: AdminPage
  },
  {
    path: '/owner/login',
    component: OwnerLoginPage
  },
  {
    path: '/owner/dashboard',
    component: OwnerDashBoard
  }  
  ]



if (device=='mobile'){
routes.push(
      {
      path: '/',
      component: EmployeePage
    }
)
}else{
  routes.push(
      {
      path: '/',
      component: NotAllowed
    }
)
}



const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router

