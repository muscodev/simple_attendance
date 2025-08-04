

<template>
  <NConfigProvider class="min-h-screen flex flex-col items-center py-5 bg-gray-100">
    
    <NMessageProvider>

      <AttendanceTracker :me="employee" class="border-4 rounded-lg border-indigo-500 " />

    </NMessageProvider>

  </NConfigProvider>

</template>

<script setup>
import { NConfigProvider, NMessageProvider } from 'naive-ui';
import AttendanceTracker from '../../components/AttendanceTracker.vue';
import { onMounted, ref } from 'vue';
import { getme } from '../../services/employeeService'

const employee = ref();

async function  updateMe(){
  try{
    let response =  await getme();
    employee.value = response.data;

  }catch(error){
    console.error("ss")
  }
}

onMounted(async ()=>{
  await updateMe()

})
</script>