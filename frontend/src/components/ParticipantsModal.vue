<template>
  <div class="modal fade" id="participantsModal" tabindex="-1" ref="modalEl">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">Participants — {{ trekName }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body">
          <div v-if="loading" class="text-muted">Loading...</div>
          <div v-else-if="participants.length === 0" class="text-muted">No participants registered yet.</div>
          <table v-else class="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Language</th>
                <th>Phone</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="p in participants" :key="p.booking_id">
                <td>{{ p.name }}</td>
                <td>{{ p.age }}</td>
                <td>{{ p.language }}</td>
                <td>{{ p.phone }}</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import { Modal } from 'bootstrap'

const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'ParticipantsModal',

  data() {
    return {
      trekName: '',
      participants: [],
      loading: false,
      modalInstance: null
    }
  },

  mounted() {
    this.modalInstance = new Modal(this.$refs.modalEl)
  },
  
  methods: {
    async open(trekId) {
      this.loading = true
      this.participants = []
      this.modalInstance.show()

      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`${API_BASE_URL}/staff/treks/${trekId}/participants`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.trekName = res.data.data.trek_name
        this.participants = res.data.data.participants
      } catch (err) {
        console.error('Failed to load participants', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>