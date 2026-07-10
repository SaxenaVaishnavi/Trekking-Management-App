<template>
  <div>
    <h3 class="mb-4">My Bookings</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else-if="bookings.length === 0" class="text-muted">You have no active bookings.</div>

    <div class="row g-3" v-else>
      <div class="col-md-4" v-for="b in bookings" :key="b.booking_id">
        <div class="card h-100">

          <div class="card-body">
            <h5 class="card-title">{{ b.trek_name }}</h5>
            <p class="text-muted small mb-1">{{ b.location }}</p>
            <p class="small mb-1">{{ b.start_date }} to {{ b.end_date }}</p>
            <p class="mb-1">₹{{ b.price }}</p>
            <span class="badge" :class="paymentBadge(b.payment_status)">{{ b.payment_status }}</span>
            <span class="badge bg-success ms-1">{{ b.booking_status }}</span>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'MyBookingsView',

  data() {
    return { bookings: [], loading: true }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await axios.get(`${API_BASE_URL}/my-bookings`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.bookings = res.data.data
    } catch (err) {
      console.error('Failed to load bookings', err)
    } finally {
      this.loading = false
    }
  },
  
  methods: {
    paymentBadge(status) {
      if (status === 'successful') return 'bg-success'
      if (status === 'failed') return 'bg-danger'
      return 'bg-warning text-dark'
    }
  }
}
</script>