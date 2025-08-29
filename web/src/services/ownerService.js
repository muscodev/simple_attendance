import api from "../utils/api"

export function ownerLogin(credentials){
    api.post(
        '/api/owner/login',
        credentials,
        {
            withCredentials: true,
            headers:{
                "Content-Type": "application/json",
            }
        }
    )

}