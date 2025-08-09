import { createRouter, createWebHistory } from 'vue-router'
// import AdminPage from '../views/Admin/AdminPage.vue'
import AdminLogin from '../views/Admin/AdminLogin.vue'
import EmployeePage from '../views/Admin/EmployeePage.vue'
import EmployeeMobile from '../views/Employee/EmployeeMobile.vue'
import GeoMarkingList from '../components/GeoMarkingList.vue'
import { getDeviceType  } from '../utlis/device.js'
import NotAllowed from '../components/NotAllowed.vue'
import OwnerLoginPage from '../views/Owner/LoginPage.vue'
import OwnerDashBoard from '../views/Owner/DashBoard.vue'
import AdminLayout from '../views/Admin/AdminLayout.vue'
import EmpLoginPage from '../views/Employee/LoginPage.vue'

let device = getDeviceType();
console.log(device);
let routes = [
    {
    path: '/admin/login',
    component: AdminLogin
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: 'geomarking',         
        component: GeoMarkingList,
      },
      {
        path: 'employees',      
        component: EmployeePage,
      },

    ],
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
      component: EmployeeMobile
    },
    {
      path: '/e/:token',
      component: EmpLoginPage
    }
)
}else{
  routes.push(
      {
      path: '/',
      redirect: '/admin',
    }
)
}



const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router

