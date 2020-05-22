<template>
  <div class="container g-pt-20">
    <div class="row">
      <!-- 左边菜单栏 -->
      <div class="col-md-3 g-mb-50 mb-3">
        <aside class="g-brd-around g-brd-gray-light-v4 rounded g-px-20 g-py-30">
          <!-- 用户头像 -->
          <div v-if="user" class="text-center g-pos-rel g-mb-30">
            <div class="g-width-100 g-height-100 mx-auto mb-3">
              <!-- <img class="img-fluid rounded-circle g-brd-around g-brd-gray-light-v4 g-pa-2" v-bind:src="user._links.avatar" v-bind:alt="user.name || user.username"> -->
              <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" :size="'large'" class="mt-3"></el-avatar>
            </div>
            <span class="d-block g-font-weight-500">{{ user.name || user.username }}</span>
            <router-link :to="{ path: `/user/${sharedState.user_id}` }">
              <span class="u-icon-v3 u-icon-size--xs g-color-white--hover g-bg-primary--hover rounded-circle g-pos-abs g-top-0 g-right-15 g-cursor-pointer" title="Go To Your Profile"
                    data-toggle="tooltip"
                    data-placement="top">
                <i class="icon-finance-067 u-line-icon-pro"></i>
              </span>
            </router-link>
          </div>
          <!-- End 用户头像 -->

          <!-- 菜单列表 -->
          <div class="text-center">
            <div class="shadow-sm p-3 bg-white rounded">
              <router-link :to="{ name: 'AdminRoles' }" :active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" :class="isAdminRoles" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-user u-line-icon-pro"></i></span>
                Roles
              </router-link>
            </div>
            <div class="shadow-sm p-3 bg-white rounded">
              <router-link :to="{ name: 'AdminUsers' }" :active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" :class="isAdminUsers" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-people u-line-icon-pro"></i></span>
                Users
              </router-link>
            </div>
            <div class="shadow-sm p-3 bg-white rounded">
              <router-link :to="{ name: 'AdminPosts' }" :active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-notebook u-line-icon-pro"></i></span>
                Posts
              </router-link>
            </div>
            <div class="shadow-sm p-3 bg-white rounded">
              <router-link :to="{ name: 'AdminComments' }" :active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-speech u-line-icon-pro"></i></span>
                Comments
              </router-link>
            </div>
            <div class="shadow-sm p-3 bg-white rounded">
              <router-link :to="{ name: 'AdminOverview' }" :active-class="'active g-color-primary--active g-bg-gray-light-v5--active'" :class="isAdminRoles" class="d-block align-middle u-link-v5 g-color-text g-color-primary--hover g-bg-gray-light-v5--hover rounded g-pa-3">
                <span class="u-icon-v1 g-color-gray-dark-v5 mr-2"><i class="icon-eye u-line-icon-pro"></i></span>
                Overview
              </router-link>
            </div>
          </div>
          <!-- End 菜单列表 -->
        </aside>
      </div>
      <!-- End 左边菜单栏 -->

      <!-- 右边子路由匹配后，显示对应的组件 -->
      <div class="col-md-9 g-mb-50">
        <div class="rounded g-brd-around g-brd-gray-light-v4 g-overflow-x-scroll g-overflow-x-visible--lg g-pa-30">
          <router-view></router-view>
        </div>
      </div>
      <!-- End 嵌套路由 -->
    </div>
  </div>
</template>

<script>
import store from '../../store'


export default {
  name: 'Admin',  // this is the name of the component
  data () {
    return {
      sharedState: store.state,
      user: ''
    }
  },
  computed: {
    isAdminRoles: function () {
      const tabs = ['AdminRoles', 'AdminUsers', 'AdminEditUser', 'AdminPosts', 'AdminComments']
      if (tabs.indexOf(this.$route.name) == -1) {
        return 'active g-color-primary--active g-bg-gray-light-v5--active'
      } else {
        return ''
      }
    },
    isAdminUsers: function () {
      if (this.$route.name == 'AdminEditUser') {
        return 'active g-color-primary--active g-bg-gray-light-v5--active'
      } else {
        return ''
      }
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.user = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    }
  },
  created () {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
    })
  }
}
</script>