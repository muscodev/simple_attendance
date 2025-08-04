<template>
  <n-card title="Login" class="max-w-md mx-auto mt-20 p-6">
    <n-form :model="form" class="space-y-4">
      <n-form-item label="Username">
        <n-input v-model:value="form.username" placeholder="Enter username" />
      </n-form-item>

      <n-form-item label="Password">
        <n-input
          v-model:value="form.password"
          type="password"
          show-password-on="mousedown"
          placeholder="Enter password"
        />
      </n-form-item>

      <n-button type="primary" block :loading="loading" @click="handleLogin">
        Login
      </n-button>

      <n-alert v-if="error" type="error" class="mt-4">
        {{ error }}
      </n-alert>
    </n-form>
  </n-card>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { NForm, NCard, NAlert,NFormItem, NButton, NInput } from 'naive-ui'
import { login } from '../services/adminService.js'

const form = reactive({
  username: '',
  password: '',
})

const loading = ref(false)
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await login(form);

    if (response.status == 200) {
      router.push('/admin/') // redirect to home or dashboard
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
