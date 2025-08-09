

<template>
  <NConfigProvider class="min-h-screen flex flex-col items-center py-5 bg-gray-100">

    <NMessageProvider>
      <n-page-header class="w-full bg-blue-600 shadow px-4 py-2 flex justify-between items-center">
        <template #title>
          🧑 SA
        </template>
     
      </n-page-header>
      <AttendanceTracker :me="employee" class="border-4 rounded-lg border-indigo-500 " @update="updateMe" />
      
      <div class="fixed bottom-0 left-0 right-0 bg-white-0 border-t border-gray-200">
      <n-tabs v-model:value="activeTab" type="bar" justify-content="space-around" size="small" >
        <n-tab-pane name="home" tab="🏠 Home" />
        <n-tab-pane name="search" tab="🔍 Search" />
        <n-tab-pane name="profile" tab="👤 Profile" />
      </n-tabs>
      </div>

    </NMessageProvider>

  </NConfigProvider>

</template>

<script setup>
import {NPageHeader, NConfigProvider, NMessageProvider, NTabs, NTabPane} from 'naive-ui';
import AttendanceTracker from '../../components/AttendanceTracker.vue';
import { onMounted, ref } from 'vue';
import { getme } from '../../services/employeeService'

const employee = ref();
const activeTab = ref('home')

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