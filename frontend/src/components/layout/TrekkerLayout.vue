<template>
  <div class="d-flex">
    <!-- Sidebar -->
    <nav class="sidebar bg-white border-end vh-100 p-3" style="width: 240px; position: sticky; top: 0;">
      <h5 class="mb-4">MY TREK APP</h5>
      <ul class="nav nav-pills flex-column gap-1">

        <li class="nav-item">
          <router-link to="/trekker/dashboard" class="nav-link" active-class="active">
            <i class="bi bi-house-door me-2"></i>Dashboard
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/trekker/treks" class="nav-link" active-class="active">
            <i class="bi bi-compass me-2"></i>Browse Treks
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/trekker/my-bookings" class="nav-link" active-class="active">
            <i class="bi bi-calendar-check me-2"></i>My Bookings
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/trekker/history" class="nav-link" active-class="active">
            <i class="bi bi-clock-history me-2"></i>History
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/trekker/profile" class="nav-link" active-class="active">
            <i class="bi bi-person me-2"></i>Profile
          </router-link>
        </li>

        <li class="nav-item mt-3">
          <a href="#" class="nav-link text-danger" @click.prevent="handleLogout">
            <i class="bi bi-box-arrow-right me-2"></i>Logout
          </a>
        </li>

      </ul>
    </nav>

    <!-- Page content -->
    <main class="flex-grow-1 bg-light p-4" style="min-height: 100vh;">
      <router-view />
    </main>

  </div>
</template>


<script>
export default {
  name: 'TrekkerLayout',
  methods: {
    handleLogout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('role')
      localStorage.removeItem('user')
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>