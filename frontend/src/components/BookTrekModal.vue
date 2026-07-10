<!-- This modal is supposed ot be shared between Dashboard and Browse Treks -->

<template>
  <div class="modal fade" id="bookTrekModal" tabindex="-1" ref="modalEl">
    <div class="modal-dialog">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">Book Trek</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="trek">
          <h6>{{ trek.name }}</h6>
          <p class="text-muted small mb-2">{{ trek.location }}</p>
          <ul class="list-group mb-3">
            <li class="list-group-item">Dates: {{ trek.start_date }} to {{ trek.end_date }}</li>
            <li class="list-group-item">Duration: {{ trek.duration }} days ({{ trek.length }} km)</li>
            <li class="list-group-item">Difficulty: {{ trek.difficulty }}</li>
            <li class="list-group-item">Age Range: {{ trek.min_age }} - {{ trek.max_age }}</li>
            <li class="list-group-item">Price: ₹{{ trek.price }}</li>
            <li class="list-group-item">Slots left: {{ trek.available_slots }}</li>
          </ul>

          <div v-if="message" class="alert py-2" :class="success ? 'alert-success' : 'alert-danger'">
            {{ message }}
          </div>

          <button class="btn btn-primary w-100" :disabled="booking" @click="confirmBooking">
            {{ booking ? 'Booking...' : 'Confirm Booking' }}
          </button>
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
  name: 'BookTrekModal',

  data() {
    return {
      trek: null,
      booking: false,
      message: '',
      success: false,
      modalInstance: null
    }
  },

  mounted() {
    this.modalInstance = new Modal(this.$refs.modalEl)
  },

  methods: {
    open(trek) {
      this.trek = trek
      this.message = ''
      this.modalInstance.show()
    },

    async confirmBooking() {
      this.booking = true
      this.message = ''
      try {
        const token = localStorage.getItem('access_token')
        await axios.post(`${API_BASE_URL}/bookings`,
          { trek_id: this.trek.id },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        
        this.success = true
        this.message = 'Booking confirmed!'
        this.$emit('booked')   
        setTimeout(() => this.modalInstance.hide(), 1200)
      } 
      catch (err) {
        this.success = false
        this.message = err.response?.data?.message || 'Booking failed.'
      } finally {
        this.booking = false
      }
    }
  }
}
</script>