<template>
  <div class="d-flex flex-column align-items-center justify-content-center text-center" style="min-height: 100vh;">
    <h1 class="display-1 fw-bold text-primary">404</h1>
    <p class="text-muted mb-4">The page you're looking for doesn't exist.</p>
    <router-link to="/" class="btn btn-primary">Go to Home</router-link>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>