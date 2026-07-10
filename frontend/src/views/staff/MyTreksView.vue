<template>
  <div>
    <h3 class="mb-4">My Treks</h3>

    <div v-if="loading" class="text-muted">Loading...</div>
    <div v-else-if="treks.length === 0" class="text-muted">No treks assigned to you yet.</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Trek Name</th>
          <th>Location</th>
          <th>Dates</th>
          <th>Participants</th>
          <th>Slots</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td>{{ t.name }}</td>
          <td>{{ t.location }}</td>
          <td>{{ t.start_date }} - {{ t.end_date }}</td>
          <td>{{ t.participant_count }}</td>
          <td>{{ t.total_slots - t.available_slots }} / {{ t.total_slots }}</td>
          <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>

          <td>
            <button class="btn btn-sm btn-outline-primary" @click="openParticipants(t)">
              More Details
            </button>
          </td>

        </tr>
      </tbody>
    </table>

    <ParticipantsModal ref="participantsModal" />

  </div>
</template>


<script>
import axios from 'axios'
import ParticipantsModal from '../../components/ParticipantsModal.vue'

const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'MyTreksView',

  components: { ParticipantsModal },

  data() {
    return { treks: [], loading: true }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await axios.get(`${API_BASE_URL}/staff/my-treks`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.treks = res.data.data
    } catch (err) {
      console.error('Failed to load treks', err)
    } finally {
      this.loading = false
    }
  },

  methods: {
    statusBadge(status) {
      if (status === 'open') return 'bg-success'
      if (status === 'sold_out') return 'bg-warning text-dark'
      if (status === 'closed') return 'bg-dark'
      return 'bg-secondary'   // completed
    },
    
    openParticipants(trek) {
      this.$refs.participantsModal.open(trek.id)
    }
  }
}
</script>