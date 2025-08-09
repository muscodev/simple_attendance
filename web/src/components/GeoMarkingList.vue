<template>
  <n-card title="GeoMarking" class="p-4 table-wrapper">

    <div >
      <div class="mb-3">
      <n-button type="primary" size="small" @click="showModal = true">
        Add Marks
      </n-button>
    </div>
      <n-card v-for="mark in geo_markings" class="employee-card" :bordered="true">
        <template #header>
          <div class="header-row">

               {{  mark.name }}
              <a :href="`https://www.google.com/maps?q=${mark.latitude},${mark.longitude}`" target="_blank">
               📍
              </a>
    
          </div>
        </template>
          <n-space>
            {{  mark.latitude }}: {{ mark.longitude }}
          </n-space>
      </n-card>
    </div>

    <n-modal v-model:show="showModal" preset="dialog" title="Add Geo Mark">
      <n-form
        :model="form"
        label-placement="top"
        size="small"
      >
        <n-form-item label="Name" path="name">
          <n-input v-model:value="form.name" placeholder="Enter location name" />
        </n-form-item>
        <n-form-item label="Latitude" path="latitude">
          <n-input-number v-model:value="form.latitude" placeholder="Enter latitude" />
        </n-form-item>
        <n-form-item label="Longitude" path="longitude">
          <n-input-number v-model:value="form.longitude" placeholder="Enter longitude" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showModal = false">Cancel</n-button>
        <n-button type="primary" @click="handleAddMark">Add</n-button>
      </template>
    </n-modal>

  </n-card>
</template>


<script setup>
import { ref,defineEmits, onMounted,reactive } from 'vue'
import { NSpace,NCard, NForm, NFormItem,NInputNumber,NModal, NButton, NInput, useMessage } from 'naive-ui'
import { create_geomarking, get_geomarking  } from '../services/adminService'


const emit = defineEmits(['updated'])

const message = useMessage()

const geo_markings = ref();

const showModal = ref(false)

// Fully reactive form
const form = reactive({
  name: '',
  latitude: null,
  longitude: null
})

async function handleAddMark() {
  if (!form.name || form.latitude === null || form.longitude === null) {
    alert('Please fill in all fields')
    return
  }
  let response = await create_geomarking({...form});
  Object.assign(form, { name: '', latitude: null, longitude: null }) // reset form
  showModal.value = false
  await loadGeoMarkings();
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
  message.success('Copied to clipboard!')
}

async function loadGeoMarkings(params) {
  try{
      geo_markings.value =  (await get_geomarking()).data;
  }
  catch(error){
    message.error(error.data);
  }

}

onMounted(async()=>{
  await loadGeoMarkings()
})


</script>

