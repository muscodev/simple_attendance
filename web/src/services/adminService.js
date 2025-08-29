
import axios from 'axios';
import { formatAsLocalYYYYMMDD } from '../utils/general.js'
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // dynamic from .env
  withCredentials: true, // if using cookies for auth
});

// api.interceptors.response.use(
//   response => response,
//   error => {
//     // global error handling (e.g., auth)
//     if (error.response?.status === 401) {
//       // Redirect or notify
//     }
//     return Promise.reject(error);
//   }
// );



export async function login(credentials){

    return api.post(
        '/api/admin/login',
        credentials,
        {
            withCredentials: true,
            headers:{
                "Content-Type": "application/json",
            }
        }
    )    
}

export async function logout(){

    return api.post(
        '/api/admin/logout',
        {
            withCredentials: true,
            headers:{
                "Content-Type": "application/json",
            }
        }
    )    
}

export async function get_me(){

    return api.get('/api/admin/me')    
}

export async function get_employees(){

    return api.get('/api/admin/tenant/employees/status')    
}

export async function create_employees(data){

    return api.post('/api/admin/tenant/employee',data)    
}

export async function activate(emp_id){

    return api.put(`/api/admin/tenant/employees/${emp_id}/actvate`)    
}

export async function deactivate(emp_id){

    return api.put(`/api/admin/tenant/employees/${emp_id}/deacivate`)    
}

export async function clear_employee_session(emp_id){

    return api.delete(`/api/admin/tenant/employees/${emp_id}/session`)    
}

export async function create_login_link(emp_id){

    return api.post(`/api/admin/tenant/employees/${emp_id}/idtoken`)    
}

export async function get_geomarking(){

    return api.get('/api/admin/tenant/geomarking')    
}

export async function create_geomarking(data){

    return api.post('/api/admin/tenant/geomarking',data)    
}



export async function get_attendance_by_date(empid,startDate,endDate){
    let start_Date = formatAsLocalYYYYMMDD(startDate);
    let end_Date = formatAsLocalYYYYMMDD(endDate);
    return api.get(
        `/api/admin/tenant/employee/${empid}/attendance/?start_date=${(start_Date)}&end_date=${end_Date}`
    )    
}
