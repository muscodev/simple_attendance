
<template>
  <div class="min-h-screen flex flex-col">
  <n-page-header class="bg-white shadow px-4 py-2 flex justify-between items-center">
    <template #title>
      SA ADMIN
      <n-button text @click="showDrawer = true">🗄</n-button>
    </template>
  
    <div class="text-sm font-bold">Hi,{{ me?.email?.split('@')[0] }}</div>

  </n-page-header>
  <n-drawer v-model:show="showDrawer" placement="left" width="200">
    <n-menu :options="menuOptions"    @update:value="handleMenuClick" />
    <span size="small" class="ms-3" @click="handleLogout">Logout</span>
  </n-drawer>      

<NMessageProvider>
        <router-view />
</NMessageProvider>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { logout, get_me } from '../../services/adminService.js';

import { NDrawer, NPageHeader, NLayoutSider, NLayoutContent, NLayoutHeader,NLayout,NMenu, NButton, NMessageProvider } from 'naive-ui'

const router = useRouter()
const route = useRoute()
const me = ref();
const showDrawer = ref(false)

const menuOptions = [
  {
    label: 'Employees',
    key: '/admin/employees',
  },
  {
    label: 'GeoMarking',
    key: '/admin/geomarking',
  },
  {
    label: 'Attendance',
    key: '/admin/employees/attendance',
  },    
]

const activeKey = computed(() => route.path)

const handleMenuClick = (key) => {
  router.push(key)
}

const handleLogout = async () => {
  try {
    await logout()
    router.push('/admin/login')
  } catch (err) {
    console.error('Logout failed:', err)
  }
}
onMounted(async ()=>{
  try {
    const response = await get_me()

    // If your API throws 401/403, this won't run — it'll go to catch
    if (response.status !== 200) {
      router.push('/admin/login');
    }
    me.value = response.data;
    // Optionally use response.data
  } catch (error) {
    // Axios throws on non-2xx status codes unless caught by interceptor
    console.error('Not authenticated:', error);
    router.push('/admin/login');
  }
})
</script>