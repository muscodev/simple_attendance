<template>

  <NCard class="flex flex-col items-center justify-between">
    <div class="mb-4 text-center">
      <h1 class="text-2xl font-bold">
        <p v-if="me?.state?.status=='IN'" class="px-6 py-2 rounded hover:bg-green-200 border border-green-600">{{
          me?.name }}</p>
        <p v-else-if="me?.state?.status=='OUT'" class="px-6 py-2 rounded hover:bg-red-200 border border-red-600">{{
          me?.name }}</p>
        <p v-else class="px-6 py-2 rounded hover:bg-yellow-200 border border-yellow-600">{{ me?.name }}</p>
      </h1>
      <p v-if="me?.today_in.timestamp" class="text-sm text-gray-600">
        <span>IN : {{ new Date(me.today_in.timestamp).toLocaleTimeString() }}
        <a :href="`https://www.google.com/maps?q=${me.today_in.latitude},${me.today_in.longitude}`" target="_blank">
          <template v-if="me.today_in.timestamp">
            [{{ me?.today_in_near.name }}({{
            me.today_in.distance_from_marking.toFixed(2) }} Km)]
            </template>
        </a></span>
      </p>
      <p v-if="me?.state?.status == 'OUT'" class="text-sm text-gray-600">
       <span> OUT: {{ new Date(me.state.timestamp).toLocaleTimeString() }}
        <a :href="`https://www.google.com/maps?q=${me?.state?.latitude},${me?.state?.latitude}`" target="_blank">
         
            [{{ me?.state_near.name }}({{
            me?.state.distance_from_marking.toFixed(2) }} Km)]
   
        </a></span>
      </p>      
    </div>

    <!-- IN/OUT Buttons -->
    <div class="text-center">
      <button v-if="me?.state?.status!='IN'"
        class="px-6 py-2 rounded font-semibold text-white bg-green-500" @click="markIn">
        IN
      </button>
      <button v-if="me?.state?.status=='IN'"
        class="px-6 py-2 rounded font-semibold text-white bg-red-500 "
        @click="markOut">
        OUT
      </button>
    </div>

  </NCard>


</template>

<script setup>
import { ref,onMounted,reactive,computed, defineEmits } from 'vue'
import { NCard ,useMessage} from 'naive-ui'
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
            message.error(error.message);
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
    // on success response update 
    // if (employee.state == 'None' && !employee.todayIn.time){
    //   employee.todayIn.time = new Date(response.data.time);
    //   employee.todayIn.location.lat = latitude.value;
    //   employee.todayIn.location.lon = longitude.value;
    //   employee.todayIn.locationDetails = response.data.nearest;
    // }
    // employee.state =  response.data.state
    // employee.time = new Date(response.data.time);
    // employee.location.lat = latitude.value;
    // employee.location.lon = longitude.value;
    

    // employee.todayOut.time = null;
    // employee.todayOut.location.lat = null;
    // employee.todayOut.location.lon = null;      
    // employee.todayOut.locationDetails =  {
    //   place: null,
    //   dist: null
    // };      
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
    // previous state
    // if (employee.state == 'IN' && !employee.todayOut.time){
    //   employee.todayOut.time = new Date(response.data.time);
    //   employee.todayOut.location.lat = latitude.value;
    //   employee.todayOut.location.lon = longitude.value;
    //   employee.todayOut.locationDetails = response.data.nearest;

    // }    
    // // on success response update 
    // employee.state =  response.data.state
    // employee.time = new Date(response.data.time);
    // employee.location.lat = latitude.value;
    // employee.location.lon = longitude.value; 
  }
}

onMounted(async () => {   
  getUserLocation();
  // await updateEmployee();
});    
</script>
