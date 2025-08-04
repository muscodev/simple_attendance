
<template>
  <div class="min-h-screen flex flex-col">
    <!-- Top Navigation Bar -->
    <n-layout-header class="bg-white shadow px-4 py-2 flex justify-between items-center">
      <div class="text-lg font-bold">Admin Panel</div>
      <div >
        <div class="text-sm font-bold">Hi,{{ me?.email?.split('@')[0] }}</div>
         <n-button size="small" @click="handleLogout">Logout</n-button>
      </div>
     
    </n-layout-header>

    <n-layout has-sider class="flex-1">
      <!-- Sidebar Navigation -->
      <n-layout-sider width="200" class="bg-gray-50 border-r">
        <n-menu
          :options="menuOptions"
          :value="activeKey"
          @update:value="handleMenuClick"
        />
      </n-layout-sider>

      <!-- Main Content Area -->
      <n-layout-content class="p-4 bg-gray-100">
<NMessageProvider>
        <router-view />
</NMessageProvider>

        
      </n-layout-content>
    </n-layout>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { logout, get_me } from '../../services/adminService.js';
import { NLayoutSider, NLayoutContent, NLayoutHeader, NLayout,NMenu, NButton, NMessageProvider } from 'naive-ui'

const router = useRouter()
const route = useRoute()
const me = ref();

const menuOptions = [
  {
    label: 'Employees',
    key: '/admin/employees',
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