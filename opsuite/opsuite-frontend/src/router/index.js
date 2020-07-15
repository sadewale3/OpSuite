import Vue from 'vue'
import VueRouter from 'vue-router'
import Jobs from '../views/afish/Jobs'
import Executions from '../views/afish/Executions'
import AuditLogs from '../views/afish/AuditLogs'

Vue.use(VueRouter)

const routes = [
  {
    path: '/afish/jobs',
    name: 'jobs',
    component: Jobs
  },
  {
    path: '/afish/executions',
    name: 'executions',
    component: Executions
  },
  {
    path: '/afish/auditlogs',
    name: 'auditlogs',
    component: AuditLogs
  },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
