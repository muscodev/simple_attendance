<template>

  <n-card title="Attendance" class="p-4">
    <div style="display: flex; gap: 10px; margin-bottom: 10px;">

      <n-select v-model:value="selectedEmployee" :options="options" placeholder="Select Employee"
        style="width: 200px;" />
      <n-date-picker v-model:value="startDate" type="date" format="yyyy-MM-dd" style="width: 200px;" />
      <n-date-picker v-model:value="endDate" type="date" format="yyyy-MM-dd" style="width: 200px;" />
      <n-button type="primary" @click="fetchAttendance">Search</n-button>
      <n-button @click="downloadCsv">Download
      </n-button>
    </div>
    <n-data-table ref="tableRef" :columns="columns" :data="attendanceData" size="small"></n-data-table>
  </n-card>

</template>


<script setup>
import { h,ref,defineEmits, onMounted,watch, computed } from 'vue'
import { NCard,NDatePicker,NDataTable,NSelect, NForm, NFormItem,NInputNumber,NModal, NButton, NInput, useMessage } from 'naive-ui'
import { get_attendance_by_date, get_employees } from '../services/adminService'
import { downloadBlob ,formatAsLocalYYYYMMDD } from '../utils/general.js'
const message = useMessage()
const tableRef = ref();
const employees = ref([])
const attendanceData = ref([])
const selectedEmployee = ref(null)
const startDate = ref(new Date().getTime())
const endDate = ref(new Date().getTime())
const loading = ref(false)

const columns = [
  {
    title: 'EM_NO',
    key: 'employee_employee_no'
  },
  {
    title: 'EM Name',
    key: 'employee_name'
  },  
  {
    title: 'action',
    key: 'status'
  },  
  {
    title: 'time',
    key: 'timestamp',
    render(row) {
      const date = new Date(row.timestamp)
      return date.toLocaleString() // formats to local time
    }
  },
  {
    title: 'Location',
    key: 'latitude',
    render(row) {
      return h(
        'div',
        {},
        [
        
          h(
            'a',
            {
              href: `https://www.google.com/maps?q=${row.latitude},${row.longitude}`,
              target: '_blank',
              class: 'text-blue-500 underline'
            },
            '📍'
          )
        ]
      )
    }
  },
  {
    title: 'marking',
    key: 'geomarking_name'
  },
  {
    title: 'distance(km)',
    key: 'distance_from_marking',
  render(row) {
    return row.distance_from_marking?.toFixed(2) ?? ''
  }    
  }
]

const downloadCsv = () => {
  exportTocsv(
    attendanceData.value,
    `att_${formatAsLocalYYYYMMDD(new Date(startDate.value))}_${formatAsLocalYYYYMMDD(new Date(endDate.value))}_${selectedEmployee.value}.csv`
  );
};

const exportTocsv = (data, filename)=>{
  if(!data.length) return;
  const header = Object.keys(data[0]).join(',');
  const csvRows = data.map(row =>
    Object.values(row).map(val => `"${String(val).replace(/"/g,'""')}"`).join(',')
  );
  console.log(csvRows);
  const csvContent = [header, ...csvRows].join('\n');
  console.log(csvContent);  
  const blob = new Blob([csvContent],{type: "text/csv;charset=utf-8;"});
  downloadBlob(blob,filename);
}

const options = computed(() => {
  return (employees.value || []).map(e => ({
    label: e.name,
    value: e.id
  }))
})
function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
  message.success('Copied to clipboard!')
}
watch([selectedEmployee, startDate, endDate], () => {
  fetchAttendance()
})

async function fetchEmployees() {
   // replace with your API
  employees.value = (await get_employees()).data
}
async function fetchAttendance() {
    
  loading.value = true;
  try {
    attendanceData.value = await (await get_attendance_by_date(
      selectedEmployee.value,
      startDate.value,
      endDate.value
    )
    ).data;
  } finally {
    loading.value = false
  }    
}
onMounted(async()=>{
  await fetchEmployees();
})


</script>

