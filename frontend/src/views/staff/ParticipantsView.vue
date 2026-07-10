<template>
  <div>
    <h3 class="mb-4">Participants</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else-if="participants.length === 0" class="text-muted">No participants across your assigned treks yet.</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Trek</th>
          <th>Name</th>
          <th>Age</th>
          <th>Language</th>
          <th>Phone</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(p, index) in participants" :key="index">
          <td>{{ p.trek_name }}</td>
          <td>{{ p.name }}</td>
          <td>{{ p.age }}</td>
          <td>{{ p.language }}</td>
          <td>{{ p.phone }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'ParticipantsView',

  data() {
    return { participants: [], loading: true }
  },
  
  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await axios.get(`${API_BASE_URL}/staff/participants`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.participants = res.data.data
    } catch (err) {
      console.error('Failed to load participants', err)
    } finally {
      this.loading = false
    }
  }
}
</script>