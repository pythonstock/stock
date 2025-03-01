import Vue from 'vue'
import Router from 'vue-router'

//Vue全局使用Router
Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import { fetchMenuList } from '@/api/menu'


/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
let constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },

  {
    path: '/stock',
    component: Layout,
    redirect: '#',
    name: 'stock-data-table',
    meta: { title: 'Example', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'table/:tableName',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: 'Table', icon: 'table' }
      }
    ]
  },
 
 
]

fetchMenuList().then(response => {

  let menu_data = response.data
  for (const menu of menu_data) {
    console.info(menu)
    var childrenList = []
    for (const childrenMenu of menu.children) {
      var tmpChildren =   {
        path: childrenMenu.path,
        name: childrenMenu.name,
        component: () => import('@/views/table/index'),
        meta: { title: childrenMenu.name , icon: 'table' }
      }
      childrenList.push(tmpChildren)
    }
    var tmp_menu =   {
      path: '/stock'+menu.name,
      alwaysShow: true, 
      component: Layout,
      name: menu.name,
      redirect: '/#'+menu.name ,
      meta: { title: menu.name , icon: 'el-icon-s-help' },
      children: childrenList
    }

    constantRoutes.push(tmp_menu)
    constantRoutes.push( { path: '*', redirect: '/404', hidden: true })

  }
})

//   // 404 page must be placed at the end !!!
// constantRoutes.push( { path: '*', redirect: '/404', hidden: true })

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
