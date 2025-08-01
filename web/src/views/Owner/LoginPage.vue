<template>
  <div class="login">
    <form @submit.prevent="handleLogin">
      <input v-model="form.username" placeholder="Username" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p v-if="form.error">{{ form.error}}</p>
    </form>
  </div>
</template>

<script setup>
    import { reactive } from 'vue';
    import { ownerLogin } from '../../services/ownerService.js';
    import  router  from '../../router'
    const form = reactive({
        username: '',
        password: '',
        error: ''
    })

    async function handleLogin() {
      try {
        const response = await ownerLogin(form)
        console.log(response);
        router.push("/owner/dashboard"); 
      } catch (err) {
        form.error = err;
      }
    }

</script>
