<template>
  <div>
    <h3 class="mb-4">Dashboard</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else>
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="card p-3"><span class="text-muted small">Total Treks</span><h3>{{ kpis.total_treks }}</h3></div>
        </div>
        <div class="col-md-3">
          <div class="card p-3"><span class="text-muted small">Total Users (Trekkers)</span><h3>{{ kpis.total_trekkers }}</h3></div>
        </div>
        <div class="col-md-3">
          <div class="card p-3"><span class="text-muted small">Total Trekking Staff</span><h3>{{ kpis.total_staff }}</h3></div>
        </div>
        <div class="col-md-3">
          <div class="card p-3"><span class="text-muted small">Total Bookings</span><h3>{{ kpis.total_bookings }}</h3></div>
        </div>
      </div>

      <h5 class="mb-3">Recent Bookings</h5>
      <table class="table bg-white">
        <thead>
          <tr>
            <th>Booking ID</th>
            <th>User (Trekker)</th>
            <th>Trek</th>
            <th>Booking Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in recentBookings" :key="b.booking_id">
            <td>{{ b.booking_id }}</td>
            <td>{{ b.trekker_name }}</td>
            <td>{{ b.trek_name }}</td>
            <td>{{ b.booking_date }}</td>
            <td>
              <span class="badge" :class="b.status === 'booked' ? 'bg-success' : 'bg-danger'">{{ b.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link to="/admin/bookings">View All Bookings →</router-link>
    </div>
  </div>
</template>



<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'AdminDashboardView',

  data() {
    return {
      kpis: { total_treks: 0, total_trekkers: 0, total_staff: 0, total_bookings: 0 },
      recentBookings: [],
      loading: true
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(`${API_BASE_URL}/admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      this.kpis = response.data.data.kpis
      this.recentBookings = response.data.data.recent_bookings
    } catch (err) {
      console.error('Failed to load dashboard', err)
    } finally {
      this.loading = false
    }
  }
}
</script>