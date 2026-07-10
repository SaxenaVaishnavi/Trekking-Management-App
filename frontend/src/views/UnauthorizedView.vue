<template>
  <div class="d-flex flex-column align-items-center justify-content-center text-center" style="min-height: 100vh;">
    <h1 class="display-1 fw-bold text-danger">403</h1>
    <p class="text-muted mb-4">You don't have permission to access this page.</p>
    <router-link to="/login" class="btn btn-primary">Back to Login</router-link>
  </div>
</template>

<script>
export default {
  name: 'UnauthorizedView'
}
</script>