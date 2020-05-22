import Vue from 'vue'
import Router from 'vue-router'
import { Message } from 'element-ui'

// Views
import SayLove from '../views/SayLove'
import LostAndFound from '../views/LostAndFound'
import ChangeThings from '../views/ChangeThings'
import TeamUp from '../views/TeamUp'
import About from '../views/About'

// 添加POST
import AddPost from '@/components/Base/AddPost'

// 账号管理
import Login from '@/components/Auth/Login'
import Register from '@/components/Auth/Register'
import Profile from '@/components/Settings/Profile'
import EditProfile from '@/components/Settings/EditProfile'

// 用户通知
import Notifications from '@/components/Notifications/Notifications'

// 管理后台
import Admin from '@/components/Admin/Admin'
//  概览
import Overview from '@/components/Admin/Overview'
//  角色
import AdminRoles from '@/components/Admin/Roles'
import AdminAddRole from '@/components/Admin/AddRole'
import AdminEditRole from '@/components/Admin/EditRole'
//  用户
import AdminUsers from '@/components/Admin/Users'
import AdminEditUser from '@/components/Admin/EditUser'
//  发布
import AdminPosts from '@/components/Admin/Posts'
//  评论
import AdminComments from '@/components/Admin/Comments'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      component: SayLove
    },
    {
      path: '/saylove', 
      name: 'SayLove',
      component: SayLove
    },
    {
      path: '/lostandfound', 
      name: 'LostAndFound',
      component: LostAndFound
    },
    { 
      path: '/changethings', 
      name: 'ChangeThings', 
      component: ChangeThings 
    },
    { 
      path: '/teamup', 
      name: 'TeamUp', 
      component: TeamUp 
    },
    { 
      path: '/about', 
      name: 'About', 
      component: About 
    },

    { path: '/addpost',
      name: 'AddPost',
      component: AddPost
    },

    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user/:id',
      name: 'Profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/edit-profile',
      name: 'EditProfile',
      component: EditProfile,
      meta: {
        requiresAuth: true
      }
    },

    {
      // 用户通知
      path: '/notifications',
      name: 'Notifications',
      component: Notifications,
      meta: {
        requiresAuth: true
      }
    },
    
    {
      path: '/admin',
      component: Admin,
      children: [
        { path: '', component: Overview },
        { path: 'overview', name: 'AdminOverview', component: Overview },
        { path: 'roles', name: 'AdminRoles', component: AdminRoles },
        { path: 'add-role', name: 'AdminAddRole', component: AdminAddRole },
        { path: 'edit-role/:id', name: 'AdminEditRole', component: AdminEditRole },
        { path: 'users', name: 'AdminUsers', component: AdminUsers },
        { path: 'edit-user/:id', name: 'AdminEditUser', component: AdminEditUser },
        { path: 'posts', name: 'AdminPosts', component: AdminPosts },
        { path: 'comments', name: 'AdminComments', component: AdminComments }
      ],
      meta: {
        requiresAuth: true,
        requiresAdmin: true
      }
    }
  ],
  // 刷新页面后回到顶部
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('funcampus-token')
  if (token) {
    var payload = JSON.parse(atob(token.split('.')[1]))

    var user_perms = payload.permissions.split(",")
  }

  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    // 1. 用户未登录，但想访问需要认证的相关路由时，跳转到 登录 页
    Message.error({
      message: '请先登录...',
      center: true
    })
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } 
  // 懒得确认邮箱了
  // else if (token && !payload.confirmed && to.name != 'Unconfirmed') {
  //   // 2. 用户刚注册，但是还没确认邮箱地址时，全部跳转到 认证提示 页面
  //   next({
  //     path: '/unconfirmed',
  //     query: { redirect: to.fullPath }
  //   })
  // } else if (token && payload.confirmed && to.name == 'Unconfirmed') {
  //   // 3. 用户账户已确认，但又去访问 认证提示 页面时不让他过去
  //   next({
  //     path: '/'
  //   })
  // } 
  else if (token && (to.name == 'Login' || to.name == 'Register' || to.name == 'ResetPasswordRequest' || to.name == 'ResetPassword')) {
    // 4. 用户已登录，但又去访问 登录/注册/请求重置密码/重置密码 页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.some(record => record.meta.requiresAdmin) && token && !user_perms.includes('admin')) {
    // 5. 普通用户想在浏览器地址中直接访问 /admin ，提示他没有权限，并跳转到首页
    Message.error({
      message: '没有管理员权限...',
      center: true
    })
    next({
      path: '/'
    })
  } else if (to.matched.length === 0) {
    // 6. 要前往的路由不存在时
    Message.error({
      message: '404！网址不存在...',
      center: true
    })
    if (from.name) {
      next({
        name: from.name
      })
    } else {
      next({
        path: '/'
      })
    }
  } else {
    // 7. 正常路由出口
    next()
  }
})

export default router
