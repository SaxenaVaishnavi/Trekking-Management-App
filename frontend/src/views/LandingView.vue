<template>
  <div class="container mt-5 text-center">
    <h1 class="mb-3"> Welcome to my Trek App</h1>
    <p class="text-muted mb-4"> Explore options and book your adventure.</p>

    <div>
      <router-link to="/login" class="btn btn-primary me-2">Login</router-link>
      <router-link to="/register" class="btn btn-secondary">Register</router-link>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'LandingView'
}
</script>