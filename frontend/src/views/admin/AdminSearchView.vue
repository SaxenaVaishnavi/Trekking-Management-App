<template>
  <div>
    <h3 class="mb-4">Search</h3>

    <div class="row g-2 mb-4">
      <div class="col-md-3">
        <select v-model="searchType" class="form-select">
          <option value="treks">Treks</option>
          <option value="staff">Trekking Staff</option>
          <option value="trekkers">Users (Trekkers)</option>
          <option value="bookings">Bookings</option>
        </select>
      </div>

      <div class="col-md-6">
        <input
          v-model="query"
          type="text"
          class="form-control"
          placeholder="Search..."
          @keyup.enter="handleSearch"
        />
      </div>

      <div class="col-md-3">
        <button class="btn btn-primary w-100" @click="handleSearch" :disabled="loading">
          {{ loading ? 'Searching...' : 'Search' }}
        </button>
      </div>
    </div>

    <div v-if="searched && results.length === 0" class="text-muted">No results found.</div>

    <!-- Treks -->
    <table v-if="searchType === 'treks' && results.length" class="table bg-white">
      <thead><tr><th>Name</th><th>Location</th><th>Status</th><th>Start Date</th></tr></thead>
      <tbody>
        <tr v-for="r in results" :key="r.id">
          <td>{{ r.name }}</td><td>{{ r.location }}</td>
          <td><span class="badge bg-secondary">{{ r.status }}</span></td>
          <td>{{ r.start_date }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Staff / Trekkers -->
    <table v-if="(searchType === 'staff' || searchType === 'trekkers') && results.length" class="table bg-white">
      <thead><tr><th>Name</th><th>Username</th><th>Email</th><th>Status</th></tr></thead>
      <tbody>
        <tr v-for="r in results" :key="r.id">
          <td>{{ r.name }}</td><td>{{ r.username }}</td><td>{{ r.email }}</td>
          <td><span class="badge" :class="r.is_active ? 'bg-success' : 'bg-secondary'">{{ r.is_active ? 'Active' : 'Inactive' }}</span></td>
        </tr>
      </tbody>
    </table>

    <!-- Bookings -->
    <table v-if="searchType === 'bookings' && results.length" class="table bg-white">
      <thead><tr><th>Trekker</th><th>Trek</th><th>Status</th><th>Booking Date</th></tr></thead>
      <tbody>
        <tr v-for="r in results" :key="r.id">
          <td>{{ r.trekker_name }}</td><td>{{ r.trek_name }}</td>
          <td><span class="badge bg-secondary">{{ r.booking_status }}</span></td>
          <td>{{ r.booking_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'AdminSearchView',

  data() {
    return {
      searchType: 'treks',
      query: '',
      results: [],
      loading: false,
      searched: false
    }
  },

  methods: {
    async handleSearch() {
      if (!this.query.trim()) return
      this.loading = true
      this.searched = true
      
      try {
        const token = localStorage.getItem('access_token')
        const res = await axios.get(`${API_BASE_URL}/admin/search`, {
          params: { type: this.searchType, q: this.query },
          headers: { Authorization: `Bearer ${token}` }
        })
        this.results = res.data.data

      } catch (err) {
        console.error('Search failed', err)
        this.results = []
      } finally {
        this.loading = false
      }
    }
  }
}
</script>