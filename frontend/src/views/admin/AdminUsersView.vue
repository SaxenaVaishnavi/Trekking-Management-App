<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Users (Trekkers)</h3>
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="showInactive" v-model="showInactive" @change="fetchUsers">
        <label class="form-check-label" for="showInactive">Show inactive users</label>
      </div>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Age</th>
          <th>Total Bookings</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.fname }} {{ u.lname }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.phone }}</td>
          <td>{{ u.age }}</td>
          <td>{{ u.total_bookings }}</td>
          <td><span class="badge" :class="u.is_active ? 'bg-success' : 'bg-secondary'">{{ u.is_active ? 'Active' : 'Inactive' }}</span></td>
          <td>
            <button
              class="btn btn-sm"
              :class="u.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
              @click="toggleStatus(u)"
            >
              {{ u.is_active ? 'Deactivate' : 'Activate' }}
            </button>
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
  name: 'AdminUsersView',

  data() {
    return {
      users: [],
      loading: true,
      showInactive: false
    }
  },

  async mounted() {
    await this.fetchUsers()
  },

  methods: {
    authHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    },

    async fetchUsers() {
      this.loading = true
      try {
        const params = this.showInactive ? '?include_inactive=true' : ''
        const res = await axios.get(`${API_BASE_URL}/admin/users${params}`, this.authHeader())
        this.users = res.data.data
      } catch (err) {
        console.error('Failed to load users', err)
      } finally {
        this.loading = false
      }
    },

    async toggleStatus(user) {
      const action = user.is_active ? 'deactivate' : 'activate'
      if (!confirm(`Are you sure you want to ${action} ${user.fname} ${user.lname}?`)) return
      try {
        const res = await axios.put( `${API_BASE_URL}/admin/users/${user.id}/status`,
          { is_active: !user.is_active },
          this.authHeader()
        )

        alert(res.data.message)
        await this.fetchUsers()
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to update status')
      }
    }
  }
}
</script>