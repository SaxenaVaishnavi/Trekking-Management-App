<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Browse Treks</h3>
      <div class="d-flex gap-2">
        <select v-model="difficultyFilter" class="form-select w-auto">
          <option value="">Difficulty: All</option>
          <option value="easy">Easy</option>
          <option value="moderate">Moderate</option>
          <option value="difficult">Difficult</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading treks...</div>
    <div v-else-if="filteredTreks.length === 0" class="text-muted">No treks match your filters.</div>

    <div class="row g-3">
      <div class="col-md-4" v-for="trek in filteredTreks" :key="trek.id">
        <div class="card h-100">

          <div class="card-body">
            <h5 class="card-title">{{ trek.name }}</h5>
            <p class="text-muted small mb-1">{{ trek.location }}</p>
            <span class="badge bg-secondary mb-2">{{ trek.difficulty }}</span>
            <p class="small mb-1">{{ trek.duration }} days · {{ trek.length }} km</p>
            <p class="small mb-1">Age: {{ trek.min_age }}-{{ trek.max_age }}</p>
            <p class="mb-1"><strong>₹{{ trek.price }}</strong></p>
            <p class="small text-muted mb-3">Slots left: {{ trek.available_slots }}</p>

            <button
              class="btn btn-sm w-100"
              :class="trek.available_slots > 0 ? 'btn-primary' : 'btn-outline-secondary'"
              :disabled="trek.available_slots === 0"
              @click="openBookingModal(trek)"
            >
              {{ trek.available_slots > 0 ? 'Book Now' : 'Not Available' }}
            </button>

          </div>

        </div>
      </div>
    </div>

    <BookTrekModal ref="bookModal" @booked="fetchTreks" />
  </div>
</template>

<script>
import axios from 'axios'
import BookTrekModal from '../../components/BookTrekModal.vue'

const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'BrowseTreksView',

  components: { BookTrekModal },

  data() {
    return {
      treks: [],
      loading: true,
      difficultyFilter: ''
    }
  },

  computed: {
    filteredTreks() {
      if (!this.difficultyFilter) return this.treks
      return this.treks.filter(t => t.difficulty === this.difficultyFilter)
    }
  },

  async mounted() {
    await this.fetchTreks()
  },

  methods: {
    async fetchTreks() {
      this.loading = true
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`${API_BASE_URL}/treks`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.treks = res.data.data
      } catch (err) {
        console.error('Failed to load treks', err)
      } finally {
        this.loading = false
      }
    },
    
    openBookingModal(trek) {
      this.$refs.bookModal.open(trek)
    }
  }
}
</script>