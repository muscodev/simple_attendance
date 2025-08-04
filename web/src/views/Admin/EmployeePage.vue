<template>
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded shadow-lg p-6 w-[500px] relative">
      <EmployeeForm @success="handleSuccess" @cancel="closeModal" />

      <button @click="closeModal" class="absolute top-2 right-2 text-gray-500 hover:text-black text-2xl">&times;</button>
    </div>
  </div>    
  <div class="p-4 space-y-4">
    <button @click="openModal" class="btn btn-primary">Add Employee</button>
    <employee-list :employees="employees" @updated="loadEmployees"/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { get_employees } from '../../services/adminService'
import EmployeeForm from '../../components/EmployeeForm.vue'
import EmployeeList from '../../components/EmployeeList.vue'

const employees = ref([])
const showModal = ref(false)

function openModal() {
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}


const loadEmployees = async () => {
  const res = await get_employees()
  employees.value = res.data
}

async function handleSuccess() {
  closeModal()
  await loadEmployees() 
}


onMounted(loadEmployees);
</script>