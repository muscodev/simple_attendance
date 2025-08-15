<template>
  <NConfigProvider>
    <n-message-provider>  
  <router-view/>
    </n-message-provider>
  </NConfigProvider>  
</template>
<script setup>
import {NConfigProvider, NMessageProvider} from 'naive-ui';

</script>