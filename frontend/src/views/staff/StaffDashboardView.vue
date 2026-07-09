<template>
  <div>
    <h3 class="mb-4">My Dashboard</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else>
      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card p-3">
            <span class="text-muted small">Assigned Treks</span>
            <h3>{{ kpis.assigned_treks }}</h3>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card p-3">
            <span class="text-muted small">Total Participants</span>
            <h3>{{ kpis.total_participants }}</h3>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card p-3">
            <span class="text-muted small">Ongoing Treks</span>
            <h3>{{ kpis.ongoing_treks }}</h3>
          </div>
        </div>
      </div>

      <h5 class="mb-3">My Assigned Treks</h5>
      <table class="table bg-white">
        <thead>
          <tr>
            <th>Trek Name</th>
            <th>Dates</th>
            <th>Participants</th>
            <th>Slots</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="t in assignedTreks" :key="t.id">
            <td>{{ t.name }}</td>
            <td>{{ t.dates }}</td>
            <td>{{ t.participants }}</td>
            <td>{{ t.total_slots }}</td>
            <td>
              <span class="badge" :class="t.status === 'open' ? 'bg-success' : 'bg-secondary'">{{ t.status }}</span>
            </td>
            <td>
              <router-link to="/staff/my-treks" class="btn btn-sm btn-primary">
                {{ t.status === 'open' ? 'Manage' : 'View' }}
              </router-link>
            </td>
          </tr>
        </tbody>

      </table>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'StaffDashboardView',

  data() {
    return {
      kpis: { assigned_treks: 0, total_participants: 0, ongoing_treks: 0 },
      assignedTreks: [],
      loading: true
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(`${API_BASE_URL}/staff/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      this.kpis = response.data.data.kpis
      this.assignedTreks = response.data.data.assigned_treks
    } catch (err) {
      console.error('Failed to load dashboard', err)
    } finally {
      this.loading = false
    }
  }
}
</script>