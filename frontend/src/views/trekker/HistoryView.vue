<template>
  <div>
    <h3 class="mb-4">History</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else-if="history.length === 0" class="text-muted">No past trek activity yet.</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Location</th>
          <th>Dates</th>
          <th>Price</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="b in history" :key="b.booking_id">
          <td>{{ b.trek_name }}</td>
          <td>{{ b.location }}</td>
          <td>{{ b.start_date }} - {{ b.end_date }}</td>
          <td>₹{{ b.price }}</td>
          <td><span class="badge" :class="statusBadge(b.booking_status)">{{ b.booking_status }}</span></td>
        </tr>
      </tbody>
    </table>

  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'HistoryView',

  data() {
    return { history: [], loading: true }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await axios.get(`${API_BASE_URL}/trekker/history`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.history = res.data.data
    } catch (err) {
      console.error('Failed to load history', err)
    } finally {
      this.loading = false
    }
  },
  
  methods: {
    statusBadge(status) {
      if (status === 'completed') return 'bg-secondary'
      if (status === 'cancelled') return 'bg-danger'
      return 'bg-dark'   // invalidated
    }
  }
}
</script>