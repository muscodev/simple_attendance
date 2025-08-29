<template>

  <NCard class="flex flex-col items-center justify-between">
    <div class="mb-4">
      <!-- <h1 class="text-2xl font-bold">
        <p v-if="me?.state?.status=='IN'" class="px-6 py-2 rounded hover:bg-green-200 border border-green-600">{{
          me?.name }}</p>
        <p v-else-if="me?.state?.status=='OUT'" class="px-6 py-2 rounded hover:bg-red-200 border border-red-600">{{
          me?.name }}</p>
        <p v-else class="px-6 py-2 rounded hover:bg-yellow-200 border border-yellow-600">{{ me?.name }}</p>
      </h1> -->

      <!-- MARK IN -->
      <n-card class="bg-green-50 text-green-700 mb-2">
        <n-flex justify="space-around">
          <div>
            <p> ✅ Mark In</p>

          </div>
          <div v-if="me?.today_in?.timestamp" class="text-sm text-gray-600">
            <p> {{ new Date(me.today_in?.timestamp).toLocaleTimeString() }}</p>
            <p>
              <a :href="`https://www.google.com/maps?q=${me?.state?.latitude},${me?.state?.latitude}`" target="_blank">

                {{ me?.state_near?.name }}({{
                me?.state?.distance_from_marking?.toFixed(2) }} Km)

              </a>
            </p>

          </div>
        </n-flex>
      </n-card>

      <!-- MARK OUT -->
      <n-card class="bg-red-50  text-red-600 mb-2">
        <n-flex justify="space-around">
          <div>
            <p> ❌ Mark Out</p>

          </div>
          <div v-if="me?.state?.status == 'OUT'" class="text-sm text-gray-600">
            <p> {{ new Date(me.state?.timestamp).toLocaleTimeString() }}</p>
            <p>
              <a :href="`https://www.google.com/maps?q=${me?.state?.latitude},${me?.state?.latitude}`" target="_blank">

                {{ me?.state_near?.name }}({{
                me?.state?.distance_from_marking?.toFixed(2) }} Km)

              </a>
            </p>

          </div>
        </n-flex>
      </n-card>
      <n-card class="bg-blue-50 text-blue-700 mb-2">
        <n-flex justify="space-around">
          <div>
            <p> 🕒 Work Duration</p>

          </div>
          <div>
            <p v-if="me?.state?.status == 'OUT'" class="text-sm text-gray-600">
              {{ calculateWorkDuration(new Date(me?.today_in?.timestamp), new Date(me?.state?.timestamp)) }}
            </p>
          </div>
        </n-flex>
      </n-card>


    </div>

    <!-- IN/OUT Buttons -->
    <div class=" text-center" v-if="locationError == null">
      <button v-if="me?.state?.status!='IN'" class="w-full px-6 py-2 rounded font-semibold text-white bg-green-500"
        @click="markIn">
        MARK IN
      </button>
      <button v-if="me?.state?.status=='IN'" class="w-full px-6 py-2 rounded font-semibold text-white bg-red-500 "
        @click="markOut">
       MARK OUT
      </button>
    </div>

  </NCard>


</template>

<script setup>
import { ref,onMounted,reactive,computed, defineEmits } from 'vue'
import { NCard ,useMessage, NFlex} from 'naive-ui'
import { empMarkIn, empMarkOut  } from '../services/employeeService.js'


const props = defineProps({
  me: Object
});

const emits = defineEmits(['update'])

const employee = reactive({
  id: '',
  name: '',
  state: 'None', // 'IN' | 'OUT' | 'None'
  location: {
    lat: null,
    lon: null
  },
  time: '', // Latest punch time

  // Grouped structure for first IN
  todayIn: {
    time: null,
    location: {
      lat: null,
      lon: null
    },
    locationDetails: {
      place: null,
      dist: null // in meters
    }
  },

  // Grouped structure for last OUT
  todayOut: {
    time: null,
    location: {
      lat: null,
      lon: null
    },
    locationDetails: {
      place: null,
      dist: null
    }
  }
})

const latitude = ref(null);
const longitude = ref(null);
const locationError = ref(null);
const message = useMessage()


const getUserLocation = () => {

      if ('geolocation' in navigator) {

        navigator.geolocation.getCurrentPosition(
          (position) => {

            locationError.value = null;
            latitude.value = position.coords.latitude;
            longitude.value = position.coords.longitude;
          },
          (error) => {

            latitude.value = null;
            longitude.value = null;              
            locationError.value = error.message;
            message.error(`${error.message}`);
            message.warning(`plese enable location access`);
            console.error('Error getting location:', error.message);
            
          }
        );
      } else {
        message.error('Geolocation is not supported by your browser.');
        locationError.value = 'Geolocation is not supported by your browser.';
      }
    };

// async function updateEmployee(){
//   const response = await getme();
//   employee.name = response.data.name;    
//   employee.id = response.data.id;    

// }

// Calculate work duration
const calculateWorkDuration = (start, end) => {
  const diff = end - start;
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
};


async function markIn() {

  getUserLocation();
  if(latitude.value && longitude.value && locationError.value==null){
    // send mark in 
    let coordinate = {
      lat:latitude.value,
      lon:longitude.value
    }
    let response = await empMarkIn(coordinate);
    message.success("Markin Success");
    emits('update');

  }
    
}

async function markOut() {
  getUserLocation();
  console.log("markout",latitude.value, longitude.value,locationError.value);

  if(latitude.value && longitude.value && locationError.value==null){
    // send mark in 
    let coordinate = {
      lat:latitude.value,
      lon:longitude.value
    }
    
    let response = await empMarkOut(coordinate);
    message.success("MarkOut Success");
    console.log("markout");
    emits('update');
  }
}

onMounted(async () => {   
  getUserLocation();
  // await updateEmployee();
});    
</script>
