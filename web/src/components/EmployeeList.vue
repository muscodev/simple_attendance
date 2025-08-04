<template>
  <n-card title="Employees" class="p-4">
    <n-data-table :columns="columns" :data="employees" striped />


    <n-modal v-model:show="clearSessionshowModal" preset="dialog" title="Clear Session of Employee"
      :content="`This action will clear session of  '${selectedEmployee?.name}' Are you sure? \n You need to send the link to '${selectedEmployee?.name}' for activate again`"
      positive-text="Clear Session" negative-text="Cancel" @positive-click="deleteSession" @negative-click="cancelCallback" />

    <n-modal v-model:show="shareLinkshowModal" preset="dialog" title="Create New Login Link" negative-text="Close"
      @negative-click="CloseCreateLink">
      <div v-if="loginLink">
        <p>Link created successfully:</p>
        <n-input v-model:value="loginLink" readonly class="my-2" />
        <n-button @click="copyToClipboard(loginLink)" type="primary" size="small">Copy URL</n-button>
      </div>
      <div v-else>
        <p>Click "Create Link" to generate a login URL.</p>
        <n-button @click="creatLink" type="primary" size="small">Creat Link</n-button>
      </div>
    </n-modal>
  </n-card>
</template>

<script setup>
import { h, ref,defineEmits } from 'vue'
import { NCard, NDataTable,NModal, NButton, NInput, useMessage } from 'naive-ui'
import { clear_employee_session, create_login_link } from '../services/adminService'


const emit = defineEmits(['updated'])

const props = defineProps({
  employees: Array,
})
const message = useMessage()
const clearSessionshowModal = ref(false)
const shareLinkshowModal = ref(false)
const selectedEmployee = ref(null)
const loginLink = ref(null)


function CloseCreateLink(){
  loginLink.value = null;
  selectedEmployee.value = null
}

async function creatLink() {
  // simulate API call
  let linkToken = await create_login_link(selectedEmployee.value.id)
  loginLink.value = window.location.origin + `/e/${linkToken.data}/`
  message.success('link created')
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
  message.success('Copied to clipboard!')
}

async function deleteSession(){
  let response = await clear_employee_session(selectedEmployee.value.id)
  if( response.status == 200){
  message.success(`session deleted for ${selectedEmployee.value.name}`)
  emit('updated');
  }
  else{
      message.error(`session could not be  deleted ${selectedEmployee.value.name}: ${response.data}`)
  }
  selectedEmployee.value = null
  clearSessionshowModal.value = false

}

function cancelCallback(){
    selectedEmployee.value = null
}

function clearSessionOpenModal(row) {
  selectedEmployee.value = row
  clearSessionshowModal.value = true
}

function shareLinkOpenModal(row) {
  selectedEmployee.value = row
  shareLinkshowModal.value = true
}

const columns = [
  { title: 'Status', 
    key: 'last_marked_today',
    render(row) {
      let label = 'X';
      let color = 'text-grey-600';
      if(row.last_marked_today === "IN"){ label='🟢',color='text-green-600' }
      else if(row.last_marked_today === "OUT"){ label='🔴',color='text-red-600' }
      return h('span', { class: color }, label)
    }

  },
  { title: 'Employee No', key: 'employee_no' },
  { title: 'Name', key: 'name' },
  { title: 'Email', key: 'email' },
  { title: 'Phone', key: 'phone' },
  {
    title: 'Active', key: 'is_active', render(row) {
      const color = row.is_active === true ? 'text-blue-600' : 'text-grey-600'
      const label = row.is_active === true ? 'yes' : 'No'
      return h('span', { class: color }, label)
    }
  },  
  {
    title: 'session', key: 'device_locked', render(row) {
      const color = row.device_locked === true ? 'text-blue-600' : 'text-grey-600'
      const label = row.device_locked === true ? '🔒' : '🔓'
      return h('span', {
         class: color,
         onClick: () => {
          row.device_locked === true ? clearSessionOpenModal(row): shareLinkOpenModal(row)
          
         }},
         label
        )
    }
  },  
]
</script>

