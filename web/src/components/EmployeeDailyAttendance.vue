
<!-- AttendanceTracker.vue Component -->
<template>
  <div class="w-full max-w-7xl mx-auto p-6">
    <!-- Header -->
    <div class="mb-8 text-center">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">Daily Attendance</h1>
      <p class="text-gray-600">{{ monthYearDisplay }}</p>
    </div>

    <!-- Summary Cards
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <n-card class="bg-green-500 text-white">
        <div class="text-center">
          <div class="text-2xl font-bold">{{ totalPresent }}</div>
          <div class="text-green-100">Present Days</div>
        </div>
      </n-card>
      <n-card class="bg-red-500 text-white">
        <div class="text-center">
          <div class="text-2xl font-bold">{{ totalAbsent }}</div>
          <div class="text-red-100">Absent Days</div>
        </div>
      </n-card>
      <n-card class="bg-blue-500 text-white">
        <div class="text-center">
          <div class="text-2xl font-bold">{{ averageDuration }}</div>
          <div class="text-blue-100">Avg Duration</div>
        </div>
      </n-card>
      <n-card class="bg-purple-500 text-white">
        <div class="text-center">
          <div class="text-2xl font-bold">{{ totalInCount }}</div>
          <div class="text-purple-100">Total Check-ins</div>
        </div>
      </n-card>
    </div> -->

    <!-- Attendance Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <n-card 
        v-for="day in attendanceData" 
        :key="day.date"
        :class="['attendance-card', getCardClass(day)]"
        hoverable
      >
        <template #header>
          <div class="flex justify-between items-center">
            <div class="font-semibold text-lg">
              {{ formatDate(day.date) }}
            </div>
            <n-tag 
              :type="day.completed === 'COMPLETE' ? 'success' : 'error'"
              size="small"
            >
              {{ day.completed === 'COMPLETE' ? 'COMPLETED' : 'INCOMPLETE' }}
            </n-tag>            
            <n-tag 
              :type="day.status === 'present' ? 'success' : day.status === 'absent' ? 'error' : 'default'"
              size="small"
            >
              {{ day.status.toUpperCase() }}
            </n-tag>
          </div>
        </template>
        <div v-if="day.status === 'present'" class="space-y-4">
          <!-- Check In -->
          <div class="flex items-start gap-3">
            <div class="w-3 h-3 bg-green-500 rounded-full mt-1.5"></div>
            <div class="flex-1">
              <div class="font-medium text-green-700">Check In</div>
              <div class="text-sm text-gray-600">{{ day.checkIn.time }}</div>
              <div class="text-xs text-gray-500">{{ day.checkIn.location }}</div>
            </div>
          </div>

          <!-- Check Out -->
          <div class="flex items-start gap-3" v-if="day.checkOut">
            <div class="w-3 h-3 bg-red-500 rounded-full mt-1.5"></div>
            <div class="flex-1">
              <div class="font-medium text-red-700">Check Out</div>
              <div class="text-sm text-gray-600">{{ day.checkOut.time }}</div>
              <div class="text-xs text-gray-500">{{ day.checkOut.location }}</div>
            </div>
          </div>

          <!-- Duration & Count -->
          <div class="pt-3 border-t border-gray-200">
            <div class="flex justify-between items-center">
              <div>
                <div class="text-sm font-medium text-gray-700">Duration</div>
                <div class="text-lg font-bold text-blue-600">{{ day.duration }}</div>
              </div>
              <div class="text-right">
                <div class="text-sm font-medium text-gray-700">Check-ins</div>
                <div class="text-lg font-bold text-purple-600">{{ day.totalInCount }}</div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="day.status === 'absent'" class="text-center py-4">
          <div class="text-gray-400 text-lg">No attendance recorded</div>
        </div>

        <div v-else class="text-center py-4">
          <div class="text-gray-400 text-lg">Weekend</div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup>
import { NCard, NTag, NDatePicker } from 'naive-ui';
import { ref, computed, onMounted, watch } from 'vue';
import { get_attendance_card } from '../services/employeeService';
import { calculateWorkDuration } from '../utils/general';
// Props
const props = defineProps({
  me: {
    type: Object,
    default: () => ({})
  }
});

// Emits
const emit = defineEmits(['update']);

// Reactive data
// const selectedMonth = ref(new Date().getTime());
// const currentMonth = new Date().getTime();
const attendanceData = ref([]);
const attendancerow = ref([]);

// Computed properties
const monthYearDisplay = computed(() => {
  const date = new Date();
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
});

const totalPresent = computed(() => {
  return attendanceData.value.filter(day => day.status === 'present').length;
});

const totalAbsent = computed(() => {
  return attendanceData.value.filter(day => day.status === 'absent').length;
});

const averageDuration = computed(() => {
  const presentDays = attendanceData.value.filter(day => day.status === 'present' && day.duration);
  if (presentDays.length === 0) return '0h 0m';
  
  const totalMinutes = presentDays.reduce((sum, day) => {
    const [hours, minutes] = day.duration.split('h ').map(part => 
      parseInt(part.replace('m', '')) || 0
    );
    return sum + (hours * 60) + minutes;
  }, 0);
  
  const avgMinutes = Math.round(totalMinutes / presentDays.length);
  const avgHours = Math.floor(avgMinutes / 60);
  const remainingMinutes = avgMinutes % 60;
  
  return `${avgHours}h ${remainingMinutes}m`;
});

const totalInCount = computed(() => {
  return attendanceData.value.reduce((sum, day) => sum + (day.totalInCount || 0), 0);
});

// Methods
const updateMonth = () => {
  generateAttendanceData();
};

const getCardClass = (day) => {
  if (day.status === 'present') return 'border-l-4 border-green-500';
  if (day.status === 'absent') return 'border-l-4 border-red-500';
  return 'border-l-4 border-gray-300';
};

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const day = date.getDate();
  const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
  return `${day} ${dayName}`;
};

const generateDummyAttendance = (date) => {

    let record = attendancerow.value.find(row => new Date(row.attendance_date).toDateString() === date.toDateString())

    if (!record){
        return { status: 'absent' };
    }
  return {
    status: 'present',
    record: record,
    completed: record.day_status,
    checkIn: {
      time: new Date(record.first_in_time).toLocaleTimeString(),
      location: `${record.first_in_location}(${record.first_in_distance.toFixed(2)} Km)`
    },
    checkOut: {
      time: record.day_status == 'COMPLETE'? new Date(record.last_out_time).toLocaleTimeString(): null,
      location: record.day_status == 'COMPLETE'? `${record.last_out_location}(${record.last_out_distance.toFixed(2)} Km)`: null, 
    },
    duration: record.day_status == 'COMPLETE'? calculateWorkDuration(new Date(record.first_in_time),new Date(record.last_out_time)): null,
    totalInCount: record.total_in_count || 0
  };
};

const generateAttendanceData = () => {
  const selectedDate = new Date();
  const year = selectedDate.getFullYear();
  const month = selectedDate.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  attendanceData.value = [];
  
  for (let day = 1; day <= daysInMonth; day++) {
    const currentDate = new Date(year, month, day);
    const attendance = generateDummyAttendance(currentDate);
    
    attendanceData.value.push({
      date: currentDate.toLocaleDateString(),
      ...attendance
    });
  }
  
  // Emit update event to parent
  emit('update');
};

const get_attendanc_card_current_month = async ()=>{
    let data = (await get_attendance_card()).data;
    attendancerow.value = data;
}
// Lifecycle
onMounted( async () => {

  await get_attendanc_card_current_month();
  generateAttendanceData();
});
</script>

<style scoped>
.attendance-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.attendance-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
</style>