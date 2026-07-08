<template>
  <div class="container mt-5" style="max-width: 450px;">
    <h2 class="mb-4">Register</h2>

    <form @submit.prevent="handleRegister">
      <div class="row">
        <div class="col mb-3">
          <label for="fname" class="form-label">First Name</label>
          <input v-model="form.fname" type="text" class="form-control" id="fname" required />
        </div>
        <div class="col mb-3">
          <label for="lname" class="form-label">Last Name</label>
          <input v-model="form.lname" type="text" class="form-control" id="lname" required />
        </div>
      </div>

      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="form.username" type="text" class="form-control" id="username" required />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input v-model="form.email" type="email" class="form-control" id="email" required />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" id="password" required />
      </div>

      <div class="row">
        <div class="col mb-3">
          <label for="age" class="form-label">Age</label>
          <input v-model.number="form.age" type="number" class="form-control" id="age" required />
        </div>
        <div class="col mb-3">
          <label class="form-label">Phone</label>
          <input v-model="form.phone" type="text" class="form-control" required />
        </div>
      </div>

      <div class="mb-3">
        <label for="language" class="form-label">Preferred Language</label>
        <input v-model="form.language" type="text" class="form-control" id="language" required />
      </div>

      <button type="submit" class="btn btn-primary w-100"> Register </button>
    </form>

    <p class="mt-3 text-center">
      Already have an account? <router-link to="/login"> Login</router-link>
    </p>

  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        fname: '',
        lname: '',
        username: '',
        email: '',
        password: '',
        age: null,
        phone: '',
        language: '',
        role: 'trekker'   // self-registration is always as trekker
      }
    }
  },

  methods: {
    async handleRegister() {
      try {
        await axios.post(`${API_BASE_URL}/register`, this.form)
        alert('Registration successful! Redirecting to login...')

        setTimeout(() => {
          this.$router.push({ name: 'Login' })
        }, 1500)

      } catch (err) {
        console.error('Registration error:', err)
        alert('Registration failed. Please try again.')
      }
    }
  }
}
</script>