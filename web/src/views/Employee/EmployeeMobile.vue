

<template>
  <div class="min-h-screen flex flex-col items-center py-5 ">

      <n-page-header class="w-full bg-blue-600 shadow px-4 py-2 flex justify-between items-center">
        <template #title>
          <p>  SA | {{ tanant?.name }}</p>
          <p>🧑  | {{ employee?.name }}</p>
        </template>
     
      </n-page-header>

      
      <EmployeeDailyAttendance v-if="activeTab=='history'" > </EmployeeDailyAttendance>
      <AttendanceTracker v-else :me="employee" class="border-4 rounded-lg border-indigo-500 " @update="updateMe" />


      <div class="fixed bottom-0 left-0 right-0 bg-white-0 border-t border-gray-200">
      
      <n-tabs v-model:value="activeTab" type="bar" justify-content="space-around" size="small" >
        <n-tab-pane name="home" tab="🏠 Home" />
        <n-tab-pane name="search" tab="🔍 Search" />
        <n-tab-pane name="history" tab="🔄 history"/>
      </n-tabs>
      </div>


  </div>

</template>

<script setup>
import {NPageHeader,  NMessageProvider, NTabs, NTabPane, useMessage} from 'naive-ui';
import AttendanceTracker from '../../components/AttendanceTracker.vue';
import EmployeeDailyAttendance from '../../components/EmployeeDailyAttendance.vue';
import { onMounted, ref } from 'vue';
import { getme, getMyTenant } from '../../services/employeeService'

const employee = ref();
const tanant = ref();
const activeTab = ref('home')

const message = useMessage();

const updateMe = async ()=>{
  try{
    let response =  await getme();
    employee.value = response.data;
    tanant.value = (await getMyTenant()).data;
  }catch(error){
    if(error.response.status == 401){
      message.error(error.response.data.detail);

    }
  }
}

onMounted(async ()=>{
  await updateMe()

})
</script>