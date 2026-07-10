<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Trekking Staff</h3>
      <button class="btn btn-primary" @click="openCreateModal">+ Add New Staff</button>
    </div>

    <div v-if="loading" class="text-muted">Loading...</div>

    <table v-else class="table bg-white">
      <thead>
        <tr>
          <th>Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Assigned Treks</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in staff" :key="s.id">
          <td>{{ s.fname }} {{ s.lname }}</td>
          <td>{{ s.username }}</td>
          <td>{{ s.email }}</td>
          <td>{{ s.phone }}</td>
          <td>{{ s.assigned_treks_count }}</td>
          <td><span class="badge" :class="s.is_active ? 'bg-success' : 'bg-secondary'">{{ s.is_active ? 'Active' : 'Inactive' }}</span></td>
          <td>
            <button
              class="btn btn-sm"
              :class="s.is_active ? 'btn-outline-danger' : 'btn-outline-success'"
              @click="toggleStatus(s)"
            >
              {{ s.is_active ? 'Deactivate' : 'Activate' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Create Modal -->
    <div class="modal fade" id="staffModal" tabindex="-1" ref="staffModalEl">
      <div class="modal-dialog">
        <div class="modal-content">

          <div class="modal-header">
            <h5 class="modal-title">Add New Staff Member</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div v-if="formError" class="alert alert-danger py-2">{{ formError }}</div>

            <form @submit.prevent="handleCreate">
              <div class="row">
                <div class="col mb-3">
                  <label class="form-label">First Name</label>
                  <input v-model="form.fname" type="text" class="form-control" required />
                </div>
                <div class="col mb-3">
                  <label class="form-label">Last Name</label>
                  <input v-model="form.lname" type="text" class="form-control" required />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="form.username" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Temporary Password</label>
                <input v-model="form.password" type="text" class="form-control" required />
              </div>

              <div class="row">
                <div class="col mb-3">
                  <label class="form-label">Age (21+)</label>
                  <input v-model.number="form.age" type="number" min="21" class="form-control" required />
                </div>
                <div class="col mb-3">
                  <label class="form-label">Phone</label>
                  <input v-model="form.phone" type="text" class="form-control" required />
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Language</label>
                <input v-model="form.language" type="text" class="form-control" required />
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="saving">
                {{ saving ? 'Creating...' : 'Create Staff Member' }}
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
  name: 'AdminStaffView',

  data() {
    return {
      staff: [],
      loading: true,
      saving: false,
      formError: '',
      modalInstance: null,
      form: this.emptyForm()
    }
  },

  async mounted() {
    await this.fetchStaff()
    this.modalInstance = new Modal(this.$refs.staffModalEl)
  },

  methods: {
    emptyForm() {
      return { fname: '', lname: '', username: '', email: '', password: '', age: null, phone: '', language: '' }
    },

    authHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    },

    async fetchStaff() {
      this.loading = true
      try {
        const res = await axios.get(`${API_BASE_URL}/admin/staff`, this.authHeader())
        this.staff = res.data.data
      } catch (err) {
        console.error('Failed to load staff', err)
      } finally {
        this.loading = false
      }
    },

    openCreateModal() {
      this.form = this.emptyForm()
      this.formError = ''
      this.modalInstance.show()
    },

    async handleCreate() {
      this.saving = true
      this.formError = ''
      try {
        await axios.post(`${API_BASE_URL}/admin/staff`, this.form, this.authHeader())
        this.modalInstance.hide()
        await this.fetchStaff()
      } catch (err) {
        this.formError = err.response?.data?.message || 'Failed to create staff member'
      } finally {
        this.saving = false
      }
    },
    
    async toggleStatus(staffMember) {
      try {
        await axios.put(
          `${API_BASE_URL}/admin/users/${staffMember.id}/status`,
          { is_active: !staffMember.is_active },
          this.authHeader()
        )
        await this.fetchStaff()
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to update status')
      }
    }
  }
}
</script>