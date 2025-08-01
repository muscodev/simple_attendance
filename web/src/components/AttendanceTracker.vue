<template>

  <NCard class="flex flex-col items-center justify-between">
    <div class="mb-4 text-center">
      <h1 class="text-2xl font-bold">
        <p v-if="employee.state=='IN'" class="px-6 py-2 rounded hover:bg-green-200 border border-green-600">{{
          employee.name }}</p>
        <p v-else-if="employee.state=='OUT'" class="px-6 py-2 rounded hover:bg-red-200 border border-red-600">{{
          employee.name }}</p>
        <p v-else class="px-6 py-2 rounded hover:bg-yellow-200 border border-yellow-600">{{ employee.name }}</p>
      </h1>
      <p v-if="employee.todayIn.time" class="text-sm text-gray-600">
        <span>IN : {{ employee.todayIn.time.toLocaleTimeString() }}
        <a :href="`https://www.google.com/maps?q=${employee.todayIn.location.lat},${employee.todayIn.location.lon}`" target="_blank">
          <template v-if="employee.todayIn.time">
            [{{ employee.todayIn.locationDetails.place.name }}({{
            employee.todayIn.locationDetails.dist.toFixed(2) }} Km)]
            </template>
        </a></span>
      </p>
      <p v-if="employee.todayOut.time" class="text-sm text-gray-600">
       <span> OUT: {{ employee.todayOut.time.toLocaleTimeString() }}
        <a :href="`https://www.google.com/maps?q=${employee.todayOut.location.lat},${employee.todayOut.location.lon}`" target="_blank">
         
            [{{ employee.todayOut.locationDetails.place.name }}({{
            employee.todayOut.locationDetails.dist.toFixed(2) }} Km)]
   
        </a></span>
      </p>      
    </div>

    <!-- IN/OUT Buttons -->
    <div class="text-center">
      <button v-if="employee.state!='IN'"
        class="px-6 py-2 rounded font-semibold text-white bg-green-500 hover:bg-green-600" @click="markIn">
        IN
      </button>
      <button v-if="employee.state=='IN'"
        class="px-6 py-2 rounded font-semibold text-white bg-red-500 hover:bg-red-600 " @click="markOut">
        OUT
      </button>
    </div>

  </NCard>


</template>

<script setup>
import { ref,onMounted,reactive,computed } from 'vue'
import { NCard ,useMessage} from 'naive-ui'
import { getme,empMarkIn,empMarkOut  } from '../services/employeeService.js'


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
            message.error(error.message);
            console.error('Error getting location:', error.message);
            
          }
        );
      } else {
        message.error('Geolocation is not supported by your browser.');
        locationError.value = 'Geolocation is not supported by your browser.';
      }
    };

async function updateEmployee(){
  const response = await getme();
  employee.name = response.data.name;    
  employee.id = response.data.id;    

}

async function markIn() {

  getUserLocation();
  if(latitude.value && longitude.value && locationError.value==null){
    // send mark in 
    let coordinate = {
      lat:latitude.value,
      lon:longitude.value
    }
    let response = await empMarkIn(coordinate);
    // on success response update 
    if (employee.state == 'None' && !employee.todayIn.time){
      employee.todayIn.time = new Date(response.data.time);
      employee.todayIn.location.lat = latitude.value;
      employee.todayIn.location.lon = longitude.value;
      employee.todayIn.locationDetails = response.data.nearest;
    }
    employee.state =  response.data.state
    employee.time = new Date(response.data.time);
    employee.location.lat = latitude.value;
    employee.location.lon = longitude.value;
    

    employee.todayOut.time = null;
    employee.todayOut.location.lat = null;
    employee.todayOut.location.lon = null;      
    employee.todayOut.locationDetails =  {
      place: null,
      dist: null
    };      
  }
    
}

async function markOut() {
  getUserLocation();

  if(latitude.value && longitude.value && locationError.value==null){
    // send mark in 
    let coordinate = {
      lat:latitude.value,
      lon:longitude.value
    }
    
    let response = await empMarkOut(coordinate);
    // previous state
    if (employee.state == 'IN' && !employee.todayOut.time){
      employee.todayOut.time = new Date(response.data.time);
      employee.todayOut.location.lat = latitude.value;
      employee.todayOut.location.lon = longitude.value;
      employee.todayOut.locationDetails = response.data.nearest;

    }    
    // on success response update 
    employee.state =  response.data.state
    employee.time = new Date(response.data.time);
    employee.location.lat = latitude.value;
    employee.location.lon = longitude.value; 
  }
}



onMounted(async () => {   
  getUserLocation();
  await updateEmployee();
});    
</script>
