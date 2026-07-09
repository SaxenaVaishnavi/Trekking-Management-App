import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

// Trekker Views
import TrekkerLayout from '../components/layouts/TrekkerLayout.vue'
import TrekkerDashboardView from '../views/trekker/TrekkerDashboardView.vue'

// Staff Views
import StaffLayout from '../components/layouts/StaffLayout.vue'
import StaffDashboardView from '../views/staff/StaffDashboardView.vue'

// Admin Views
import AdminLayout from '../components/layouts/AdminLayout.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'

const routes = [
  // Public Routes
  { path: '/', name: 'Landing', component: LandingView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  

  // Trekker Routes (these are nested under layout)
  {
    path: '/trekker',
    component: TrekkerLayout,
    meta: { requiresAuth:true, role: 'trekker' },
    children: [
      { path: '', redirect: { name: 'TrekkerDashboard' }},     // Redirect to dashboard by default
      { path: 'dashboard', name: 'TrekkerDashboard', component: TrekkerDashboardView }
    ]
  },

  // Staff Routes
  {
    path: '/staff',
    component: StaffLayout,
    meta: { requiresAuth:true, role: 'staff' },
    children: [
      { path: '', redirect: { name: 'StaffDashboard' }},     // Redirect to dashboard by default
      { path: 'dashboard', name: 'StaffDashboard', component: StaffDashboardView }
    ]
  },

  // Admin Routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth:true, role: 'admin' },
    children: [
      { path: '', redirect: { name: 'AdminDashboard' }},     // Redirect to dashboard by default
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboardView }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router