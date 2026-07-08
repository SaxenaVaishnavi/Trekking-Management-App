<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2 class="mb-4">Login</h2>

    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="text" class="form-control" id="username" v-model="form.username" required>
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" v-model="form.password" required>
      </div>

      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <p class="mt-3 text-center">
      Don't have an account? <router-link to="/register"> Register</router-link>
    </p>

  </div>
</template>


<script>
import axios from 'axios';
const API_BASE_URL = 'http://localhost:5000/api';

export default {
  name: 'LoginView',

  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },

  methods: {
    async handleLogin() {
      try {
        const response = await axios.post(`${API_BASE_URL}/login`, this.form);
        console.log('Login response:', response.data);

        const { username, email, phone, role, age, language, access_token} = response.data.data;
        // Storing token and role for route auth. 
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('role', role);
        localStorage.setItem('user', JSON.stringify({ username, email, phone, age, language }));

        // Redirecting based on role to the appropriate dashboard
        if (role === 'admin') {
          this.$router.push({ name: 'AdminDashboard' });
        } else if (role === 'staff') {
          this.$router.push({ name: 'StaffDashboard' });
        } else {
          this.$router.push({ name: 'TrekkerDashboard' });
        }

      } catch (error){
        console.error('Login error:', error);
        alert('Login failed. Please check your credentials and try again.');
      }
    }
  }
}

</script>