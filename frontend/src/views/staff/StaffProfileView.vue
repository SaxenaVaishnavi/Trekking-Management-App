<template>
  <div>
    <h3 class="mb-4">My Profile</h3>

    <div class="row">
      <div class="col-md-6">

        <div class="card p-4 mb-4">
          <h5 class="mb-3">Profile Details</h5>
          <div v-if="profileMessage" class="alert py-2" :class="profileSuccess ? 'alert-success' : 'alert-danger'">
            {{ profileMessage }}
          </div>

          <form @submit.prevent="handleProfileUpdate">
            <div class="row">
              <div class="col mb-3">
                <label class="form-label">First Name</label>
                <input v-model="profile.fname" type="text" class="form-control" required />
              </div>

              <div class="col mb-3">
                <label class="form-label">Last Name</label>
                <input v-model="profile.lname" type="text" class="form-control" required />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Username</label>
              <input :value="profile.username" type="text" class="form-control" disabled />
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="profile.email" type="email" class="form-control" required />
            </div>

            <div class="row">
              <div class="col mb-3">
                <label class="form-label">Phone</label>
                <input v-model="profile.phone" type="text" class="form-control" />
              </div>

              <div class="col mb-3">
                <label class="form-label">Age</label>
                <input v-model.number="profile.age" type="number" min="21" class="form-control" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label">Preferred Language</label>
              <input v-model="profile.language" type="text" class="form-control" />
            </div>

            <button type="submit" class="btn btn-primary" :disabled="savingProfile">
              {{ savingProfile ? 'Saving...' : 'Save Changes' }}
            </button>

          </form>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card p-4 mb-4">
          <h5 class="mb-3">Change Password</h5>
          <div v-if="passwordMessage" class="alert py-2" :class="passwordSuccess ? 'alert-success' : 'alert-danger'">
            {{ passwordMessage }}
          </div>

          <form @submit.prevent="handlePasswordChange">
            <div class="mb-3">
              <label class="form-label">Current Password</label>
              <input v-model="passwordForm.current_password" type="password" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label">New Password</label>
              <input v-model="passwordForm.new_password" type="password" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label">Confirm New Password</label>
              <input v-model="confirmPassword" type="password" class="form-control" required />
            </div>

            <button type="submit" class="btn btn-primary" :disabled="savingPassword">
              {{ savingPassword ? 'Updating...' : 'Change Password' }}
            </button>

          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000/api'

export default {
  name: 'StaffProfileView',

  data() {
    return {
      profile: { username: '', fname: '', lname: '', email: '', phone: '', age: null, language: '' },
      passwordForm: { current_password: '', new_password: '' },
      confirmPassword: '',
      savingProfile: false,
      savingPassword: false,
      profileMessage: '',
      profileSuccess: false,
      passwordMessage: '',
      passwordSuccess: false
    }
  },

  async mounted() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await axios.get(`${API_BASE_URL}/staff/profile`, this.authHeader())
      this.profile = res.data.data
    } catch (err) {
      console.error('Failed to load profile', err)
    }
  },

  methods: {
    authHeader() {
      return { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } }
    },

    async handleProfileUpdate() {
      this.savingProfile = true
      this.profileMessage = ''
      try {
        await axios.put(`${API_BASE_URL}/staff/profile`, this.profile, this.authHeader())
        this.profileSuccess = true
        this.profileMessage = 'Profile updated successfully.'

        const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
        localStorage.setItem('user', JSON.stringify({ ...storedUser, ...this.profile }))
      } catch (err) {
        this.profileSuccess = false
        this.profileMessage = err.response?.data?.message || 'Failed to update profile'
      } finally {
        this.savingProfile = false
      }
    },
    
    async handlePasswordChange() {
      this.passwordMessage = ''
      if (this.passwordForm.new_password !== this.confirmPassword) {
        this.passwordSuccess = false
        this.passwordMessage = 'New password and confirmation do not match.'
        return
      }
      this.savingPassword = true
      try {
        await axios.put(`${API_BASE_URL}/staff/profile/password`, this.passwordForm, this.authHeader())
        this.passwordSuccess = true
        this.passwordMessage = 'Password changed successfully.'
        this.passwordForm = { current_password: '', new_password: '' }
        this.confirmPassword = ''
      } catch (err) {
        this.passwordSuccess = false
        this.passwordMessage = err.response?.data?.message || 'Failed to change password'
      } finally {
        this.savingPassword = false
      }
    }
  }
}
</script>