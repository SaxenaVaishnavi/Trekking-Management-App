<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Bookings</h3>
      <select v-model="statusFilter" class="form-select w-auto" @change="fetchBookings">
        <option value="">All Statuses</option>
        <option value="booked">Booked</option>
        <option value="cancelled">Cancelled</option>
        <option value="completed">Completed</option>
        <option value="invalidated">Invalidated</option>
      </select>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Booking ID</th>
          <th>Trekker</th>
          <th>Trek</th>
          <th>Booking Date</th>
          <th>Price</th>
          <th>Payment</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td>{{ b.id }}</td>
          <td>{{ b.trekker_name }} ({{ b.trekker_username }})</td>
          <td>{{ b.trek_name }}</td>
          <td>{{ b.booking_date }}</td>
          <td>₹{{ b.price }}</td>
          <td>
            <span class="badge" :class="paymentBadge(b.payment_status)">{{ b.payment_status }}</span>
          </td>
          <td>
            <span class="badge" :class="statusBadge(b.booking_status)">{{ b.booking_status }}</span>
          </td>
          <td>
            <button
              v-if="b.booking_status === 'booked'"
              class="btn btn-sm btn-outline-danger"
              @click="cancelBooking(b)"
            >
              Cancel
            </button>
            <span v-else class="text-muted">—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'AdminBookingsView',
  data() {
    return {
      bookings: [],
      loading: true,
      statusFilter: ''
    }
  },

  async mounted() {
    await this.fetchBookings()
  },

  methods: {
    authHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    },

    statusBadge(status) {
      if (status === 'booked') return 'bg-success'
      if (status === 'cancelled') return 'bg-danger'
      if (status === 'invalidated') return 'bg-dark'
      return 'bg-secondary'   // completed
    },

    paymentBadge(status) {
      if (status === 'successful') return 'bg-success'
      if (status === 'failed') return 'bg-danger'
      return 'bg-warning text-dark'   // pending
    },

    async fetchBookings() {
      this.loading = true
      try {
        const params = this.statusFilter ? `?status=${this.statusFilter}` : ''
        const res = await axios.get(`${API_BASE_URL}/admin/bookings${params}`, this.authHeader())
        this.bookings = res.data.data
      } catch (err) {
        console.error('Failed to load bookings', err)
      } finally {
        this.loading = false
      }
    },
    
    async cancelBooking(booking) {
      if (!confirm(`Cancel booking #${booking.id} for ${booking.trekker_name}?`)) return
      try {
        await axios.put(`${API_BASE_URL}/admin/bookings/${booking.id}/cancel`, {}, this.authHeader())
        await this.fetchBookings()
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to cancel booking')
      }
    }
  }
}
</script>