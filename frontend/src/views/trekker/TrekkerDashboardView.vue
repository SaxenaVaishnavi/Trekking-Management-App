<template>
  <div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Welcome, {{ user.fname || user.username }}!</h3>
    </div>

    <h5 class="mb-3">Available Treks</h5>

    <div v-if="loading" class="text-muted">Loading...</div>

    <div class="row g-3 mb-4" v-else>
      <div class="col-md-4" v-for="trek in availableTreks" :key="trek.id">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="card-title">{{ trek.name }}</h6>
            <p class="text-muted small mb-1">{{ trek.location }}</p>
            <p class="small mb-2">{{ trek.difficulty }} - {{ trek.duration }} Days</p>
            <p class="small mb-3">Slots left: {{ trek.available_slots }}</p>
            <button
              class="btn btn-sm w-100"
              :class="trek.available_slots > 0 ? 'btn-outline-primary' : 'btn-outline-secondary'"
              :disabled="trek.available_slots === 0"
            >
              {{ trek.available_slots > 0 ? 'Book Now' : 'Not Available' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-2">
      <h5>My Bookings</h5>
    </div>
    <table class="table bg-white">
      <thead>
        <tr>
          <th>Trek Name</th>
          <th>Booking Date</th>
          <th>Trek Dates</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in recentBookings" :key="b.booking_id">
          <td>{{ b.trek_name }}</td>
          <td>{{ b.booking_date }}</td>
          <td>{{ b.trek_dates }}</td>
          <td><span class="badge bg-success">{{ b.status }}</span></td>
        </tr>
      </tbody>
    </table>
    <router-link to="/trekker/my-bookings">View All Bookings →</router-link>
  </div>
</template>



<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'TrekkerDashboardView',

  data() {
    return {
      user: JSON.parse(localStorage.getItem('user') || '{}'),
      availableTreks: [],
      recentBookings: [],
      loading: true
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(`${API_BASE_URL}/trekker/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      this.availableTreks = response.data.data.available_treks
      this.recentBookings = response.data.data.recent_bookings
    } catch (err) {
      console.error('Failed to load dashboard', err)
    } finally {
      this.loading = false
    }
  }
}
</script>