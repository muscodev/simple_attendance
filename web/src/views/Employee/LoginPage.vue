<template>
    <NMessageProvider>
        {{  message  }}
    </NMessageProvider>
</template>

<script setup>

import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { login } from '../../services/employeeService'
import { useMessage, NMessageProvider } from 'naive-ui'
import router from '../../router'

const route = useRoute()
const token = route.params.token
console.log(token);
const message = ref('please wait..')


onMounted(async ()=>{
    try{
    let response = await login(token);
        router.push('/')
    }
    catch(error){
        message.value = error.response.status == 400? 'invalid link , please contact admin, to give new link':'';
    }
    
})
</script>