<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Treks</h3>
      <button class="btn btn-primary" @click="openCreateModal">+ Add New Trek</button>
    </div>

    <div class="mb-3">
      <select v-model="statusFilter" class="form-select w-auto" @change="fetchTreks">
        <option value="">All Statuses</option>
        <option value="open">Open</option>
        <option value="sold_out">Sold Out</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Name</th>
          <th>Location</th>
          <th>Dates</th>
          <th>Staff</th>
          <th>Slots</th>
          <th>Price</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in treks" :key="t.id">
          <td>{{ t.name }}</td>
          <td>{{ t.location }}</td>
          <td>{{ t.start_date }} - {{ t.end_date }}</td>
          <td>{{ t.assigned_staff_name || '—' }}</td>
          <td>{{ t.available_slots }} / {{ t.total_slots }}</td>
          <td>₹{{ t.price }}</td>
          <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
          <td>
            <button class="btn btn-sm btn-outline-primary me-1" @click="openEditModal(t)">Edit</button>
            <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(t)">Close</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Create/Edit Modal -->
    <div class="modal fade" id="trekModal" tabindex="-1" ref="trekModalEl">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">{{ editingTrek ? 'Edit Trek' : 'Add New Trek' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div v-if="formError" class="alert alert-danger py-2">{{ formError }}</div>
            <form @submit.prevent="handleSave">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Name</label>
                  <input v-model="form.name" type="text" class="form-control" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Location</label>
                  <input v-model="form.location" type="text" class="form-control" required />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="form.description" class="form-control" rows="2"></textarea>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Start Date</label>
                  <input v-model="form.start_date" type="date" class="form-control" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">End Date</label>
                  <input v-model="form.end_date" type="date" class="form-control" required />
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Duration (days)</label>
                  <input v-model.number="form.duration" type="number" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Length (km)</label>
                  <input v-model.number="form.length" type="number" step="0.1" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Difficulty</label>
                  <select v-model="form.difficulty" class="form-select" required>
                    <option value="easy">Easy</option>
                    <option value="moderate">Moderate</option>
                    <option value="difficult">Difficult</option>
                  </select>
                </div>
              </div>

              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Min Age</label>
                  <input v-model.number="form.min_age" type="number" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Max Age</label>
                  <input v-model.number="form.max_age" type="number" class="form-control" required />
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Price (₹)</label>
                  <input v-model.number="form.price" type="number" class="form-control" required />
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Total Slots</label>
                  <input v-model.number="form.total_slots" type="number" class="form-control" required />
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Assign Staff</label>
                  <select v-model="form.assigned_staff_id" class="form-select">
                    <option :value="null">Unassigned</option>
                    <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.fname }} {{ s.lname }}</option>
                  </select>
                </div>
              </div>

              <div class="mb-3" v-if="editingTrek">
                <label class="form-label">Status</label>
                <select v-model="form.status" class="form-select">
                  <option value="open">Open</option>
                  <option value="sold_out">Sold Out</option>
                  <option value="completed">Completed</option>
                </select>
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="saving">
                {{ saving ? 'Saving...' : (editingTrek ? 'Update Trek' : 'Create Trek') }}
              </button>
            </form>
          </div>
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
  name: 'AdminTreksView',

  data() {
    return {
      treks: [],
      staffList: [],
      loading: true,
      statusFilter: '',
      editingTrek: null,
      saving: false,
      formError: '',
      modalInstance: null,
      form: this.emptyForm()
    }
  },

  async mounted() {
    await this.fetchTreks()
    await this.fetchStaffList()
    this.modalInstance = new Modal(this.$refs.trekModalEl)
  },

  methods: {
    emptyForm() {
      return {
        name: '', location: '', description: '', start_date: '', end_date: '',
        duration: null, length: null, difficulty: 'easy', min_age: null, max_age: null,
        price: null, total_slots: null, assigned_staff_id: null, status: 'open'
      }
    },

    authHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    },

    statusBadge(status) {
      if (status === 'open') return 'bg-success'
      if (status === 'sold_out') return 'bg-warning text-dark'
      return 'bg-secondary'
    },

    async fetchTreks() {
      this.loading = true
      try {
        const params = this.statusFilter ? `?status=${this.statusFilter}` : ''
        const res = await axios.get(`${API_BASE_URL}/admin/treks${params}`, this.authHeader())
        this.treks = res.data.data
      } catch (err) {
        console.error('Failed to load treks', err)
      } finally {
        this.loading = false
      }
    },

    async fetchStaffList() {
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/staff`, this.authHeader())
        this.staffList = res.data.data
      } catch (err) {
        console.error('Failed to load staff list', err)
      }
    },

    openCreateModal() {
      this.editingTrek = null
      this.form = this.emptyForm()
      this.formError = ''
      this.modalInstance.show()
    },

    openEditModal(trek) {
      this.editingTrek = trek
      this.form = { ...trek }
      this.formError = ''
      this.modalInstance.show()
    },

    async handleSave() {
      this.saving = true
      this.formError = ''
      try {
        if (this.editingTrek) {
          await axios.put(`${API_BASE_URL}/admin/treks/${this.editingTrek.id}`, this.form, this.authHeader())
        } else {
          await axios.post(`${API_BASE_URL}/admin/treks`, this.form, this.authHeader())
        }
        this.modalInstance.hide()
        await this.fetchTreks()
      } catch (err) {
        this.formError = err.response?.data?.message || 'Failed to save trek'
      } finally {
        this.saving = false
      }
    },

    async deleteTrek(trek) {
      if (!confirm(`Close "${trek.name}"? It will no longer be bookable, and any active bookings for it will be invalidated.`)) return
        try {
            const res = await axios.put(`${API_BASE_URL}/admin/treks/${trek.id}/close`, {}, this.authHeader())
            alert(res.data.message)
            await this.fetchTreks()
        } catch (err) {
            alert(err.response?.data?.message || 'Failed to close trek')
        }
    }   
  }
}
</script>