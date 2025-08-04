<template>
  <n-card title="Employee Form" class="p-4">
    <n-form :model="form" label-placement="left" label-width="120">
      <n-form-item label="Employee No">
        <n-input v-model:value="form.employee_no" placeholder="EMP001" />
      </n-form-item>

      <n-form-item label="Name">
        <n-input v-model:value="form.name" placeholder="John Doe" />
      </n-form-item>

      <n-form-item label="Email">
        <n-input v-model:value="form.email" type="email" />
      </n-form-item>

      <n-form-item label="Phone">
        <n-input v-model:value="form.phone" type="tel" />
      </n-form-item>

      <n-form-item label="Active">
        <n-switch v-model:value="form.is_active" />
      </n-form-item>

      <div class="flex gap-2">
        <n-button type="primary" @click="handleSubmit">Save</n-button>
        <n-button @click="resetForm">Reset</n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import { create_employees, activate, deactivate } from '../services/adminService'
import { NForm,NFormItem,NButton,NInput,NCard,NSwitch } from 'naive-ui'


const emit = defineEmits(['success','cancel'])


function submitForm() {
  // your save logic here
  emit('success')
}

function cancel() {
  emit('cancel')
}

const form = ref({
  employee_no: '',
  name: '',
  email: '',
  phone: '',
  is_active: true,
})


const handleSubmit = async () => {
  const data = { ...form.value }
  try {

    await create_employees(data);
    resetForm();
    submitForm();
  } catch (err) {
    console.error(err)
  }
}

const resetForm = () => {
  form.value = {
    employee_no: '',
    name: '',
    email: '',
    phone: '',
    is_active: true,
  }
}
</script>
