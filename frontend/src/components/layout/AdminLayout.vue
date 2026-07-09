<template>
  <div class="d-flex">
    <nav class="sidebar bg-white border-end vh-100 p-3" style="width: 240px; position: sticky; top: 0;">
      <h6 class="mb-4">☰ Admin Panel</h6>
      <ul class="nav nav-pills flex-column gap-1">

        <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link" active-class="active">
                <i class="bi bi-grid me-2"></i>Dashboard
            </router-link>
        </li>
        
        <li class="nav-item">
            <router-link to="/admin/treks" class="nav-link" active-class="active">
                <i class="bi bi-map me-2"></i>Treks
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/staff" class="nav-link" active-class="active">
                <i class="bi bi-person-badge me-2"></i>Trekking Staff
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/users" class="nav-link" active-class="active">
                <i class="bi bi-people me-2"></i>Users (Trekkers)
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/bookings" class="nav-link" active-class="active">
                <i class="bi bi-calendar-check me-2"></i>Bookings
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/search" class="nav-link" active-class="active">
                <i class="bi bi-search me-2"></i>Search
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/reports" class="nav-link" active-class="active">
                <i class="bi bi-bar-chart me-2"></i>Reports
            </router-link>
        </li>

        <li class="nav-item">
            <router-link to="/admin/settings" class="nav-link" active-class="active">
                <i class="bi bi-gear me-2"></i>Settings
            </router-link>
        </li>

        <li class="nav-item mt-3">
            <a href="#" class="nav-link text-danger" @click.prevent="handleLogout">
                <i class="bi bi-box-arrow-right me-2"></i>Logout
            </a>
        </li>

      </ul>
    </nav>

    <div class="flex-grow-1">

      <header class="d-flex justify-content-between align-items-center bg-white border-bottom px-4 py-2">
        <span class="fw-semibold">Trekking Management Application</span>
        <span><i class="bi bi-person-circle me-1"></i>{{ user.username || 'Admin' }}</span>
      </header>

      <main class="bg-light p-4" style="min-height: calc(100vh - 50px);">
        <router-view />
      </main>

    </div>
  </div>
</template>


<script>
export default {
  name: 'AdminLayout',

  data() {
    return { user: JSON.parse(localStorage.getItem('user') || '{}') }
  },
  
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