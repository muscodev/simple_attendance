import api from "../utlis/api"

export function getme(){
    return api.get(`/api/employee/`);
}


export function empMarkIn(coordinate){

    return api.post(`/api/employee/markin`,coordinate);
}


export function empMarkOut(coordinate){
    return api.post(`/api/employee/markout`,coordinate);
}


export function get_near_locations(){
    return api.get(`/api/employee/nears`);
}

export function authenticateEmployee(token){
    return api.post(token);
}

export function login(token) {
    return api.get(
        `/api/e/t/${token}`, null,
        {
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
            }
        }
    );
}