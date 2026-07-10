import { createRouter, createWebHistory } from 'vue-router'

// Public Views
import LandingView from '../views/LandingView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import UnauthorizedView from '../views/UnauthorizedView.vue'

// Trekker Views
import TrekkerLayout from '../components/layout/TrekkerLayout.vue'
import TrekkerDashboardView from '../views/trekker/TrekkerDashboardView.vue'
import BrowseTreksView from '../views/trekker/BrowseTreksView.vue'
import MyBookingsView from '../views/trekker/MyBookingsView.vue'
import HistoryView from '../views/trekker/HistoryView.vue'
import TrekkerProfileView from '../views/trekker/TrekkerProfileView.vue'

// Staff Views
import StaffLayout from '../components/layout/StaffLayout.vue'
import StaffDashboardView from '../views/staff/StaffDashboardView.vue'
import MyTreksView from '../views/staff/MyTreksView.vue'
import ParticipantsView from '../views/staff/ParticipantsView.vue'
import StaffProfileView from '../views/staff/StaffProfileView.vue'

// Admin Views
import AdminLayout from '../components/layout/AdminLayout.vue'
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import AdminTreksView from '../views/admin/AdminTreksView.vue'
import AdminUsersView from '../views/admin/AdminUsersView.vue'
import AdminStaffView from '../views/admin/AdminStaffView.vue'
import AdminBookingsView from '../views/admin/AdminBookingsView.vue'
import AdminSearchView from '../views/admin/AdminSearchView.vue'
import AdminReportsView from '../views/admin/AdminReportsView.vue'
import AdminSettingsView from '../views/admin/AdminSettingsView.vue'

const routes = [
  // Public Routes
  { path: '/', name: 'Landing', component: LandingView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },

  // Trekker Routes (these are nested under layout)
  {
    path: '/trekker',
    component: TrekkerLayout,
    meta: { requiresAuth: true, role: 'trekker' },
    children: [
      { path: '', redirect: { name: 'TrekkerDashboard' } },     // Redirect to dashboard by default
      { path: 'dashboard', name: 'TrekkerDashboard', component: TrekkerDashboardView },
      { path: 'treks', name: 'BrowseTreks', component: BrowseTreksView },
      { path: 'my-bookings', name: 'MyBookings', component: MyBookingsView },
      { path: 'history', name: 'History', component: HistoryView },
      { path: 'profile', name: 'TrekkerProfile', component: TrekkerProfileView }
    ]
  },

  // Staff Routes
  {
    path: '/staff',
    component: StaffLayout,
    meta: { requiresAuth: true, role: 'staff' },
    children: [
      { path: '', redirect: { name: 'StaffDashboard' } },     // Redirect to dashboard by default
      { path: 'dashboard', name: 'StaffDashboard', component: StaffDashboardView },
      { path: 'my-treks', name: 'MyTreks', component: MyTreksView },
      { path: 'participants', name: 'Participants', component: ParticipantsView },
      { path: 'profile', name: 'StaffProfile', component: StaffProfileView }
    ]
  },

  // Admin Routes
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', redirect: { name: 'AdminDashboard' } },     // Redirect to dashboard by default
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboardView },
      { path: 'treks', name: 'AdminTreks', component: AdminTreksView },
      { path: 'users', name: 'AdminUsers', component: AdminUsersView },
      { path: 'staff', name: 'AdminStaff', component: AdminStaffView },
      { path: 'bookings', name: 'AdminBookings', component: AdminBookingsView },
      { path: 'search', name: 'AdminSearch', component: AdminSearchView },
      { path: 'reports', name: 'AdminReports', component: AdminReportsView },
      { path: 'settings', name: 'AdminSettings', component: AdminSettingsView }
    ]
  },

  // Error Routes
  { path: '/unauthorized', name: 'Unauthorized', component: UnauthorizedView },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ---------- Navigation Guard ----------
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiredRole = to.matched.find(record => record.meta.role)?.meta.role

  // Route needs auth but no token exists → send to login
  if (requiresAuth && !token) {
    return next({ name: 'Login' })
  }

  // Route needs a specific role, and the logged-in user isn't that role
  if (requiredRole && requiredRole !== role) {
    return next({ name: 'Unauthorized' })
  }

  // Logged-in user manually visits /login or /register → bounce to their dashboard
  if ((to.name === 'Login' || to.name === 'Register') && token) {
    if (role === 'admin') return next({ name: 'AdminDashboard' })
    if (role === 'staff') return next({ name: 'StaffDashboard' })
    if (role === 'trekker') return next({ name: 'TrekkerDashboard' })
  }

  next()
})

export default router