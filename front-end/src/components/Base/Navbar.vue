<template>
  <nav class="navbar navbar-expand-lg navbar-light rounded-0 shadow-sm bg-white p-3 mb-3">

      <router-link to="/" class="navbar-brand ml-2">
        <img src="../../assets/logo.png" width="30" height="30" class="d-inline-block align-middle" alt />
        <span class="navbar-brand mb-0 h1">FunCampus</span>
      </router-link>

      <!-- 下拉按钮 -->
      <button
        class="navbar-toggler"
        id="collapse-button"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 菜单栏 -->
      <div id="navbarSupportedContent" class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item activate ml-2" @click="collapseClick">
            <router-link :to="{name: 'SayLove'}" class="nav-link" >表白</router-link>
          </li>
          <li class="nav-item ml-2"  @click="collapseClick">
            <router-link :to="{name: 'LostAndFound'}" class="nav-link">寻物</router-link>
          </li>
          <li class="nav-item ml-2" @click="collapseClick">
            <router-link :to="{name: 'ChangeThings'}" class="nav-link">易物</router-link>
          </li>
          <li class="nav-item ml-2"  @click="collapseClick">
            <router-link :to="{name: 'TeamUp'}" class="nav-link">组队</router-link>
          </li>
          <li class="nav-item ml-2"  @click="collapseClick">
            <router-link :to="{name: 'About'}" class="nav-link">关于</router-link>
          </li>
          <li class="nav-item ml-2" v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')"  @click="collapseClick">
            <router-link to="/admin" class="nav-link">后台</router-link>
          </li>

          <li v-if="sharedState.is_authenticated" class="nav-item ml-2 align-middle">
              <div class="dropdown">
                <img :src="sharedState.user_avatar" class="rounded-circle mb-2" width="40" height="40" id="dropdownMenu2" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">

                <div class="dropdown-menu dropdown-menu-left text-center rounded shadow-sm bg-white mb-3" aria-labelledby="dropdownMenu2" @click="collapseClick" style="max-width: 10%">
                  <el-dropdown-item>
                      <router-link :to="{ name: 'Notifications'}" class="nav-link">
                        <i class="el-icon-chat-line-square"></i>通知
                        <!-- 通知数量角标 -->
                        <!-- <span class="badge badge-pill badge-danger ml-1" id="new_notifications_count" style="visibility: hidden">0</span> -->
                      </router-link>
                  </el-dropdown-item>
                  <el-dropdown-item :divided="true">
                      <router-link :to="{ name: 'Profile', params: { id: sharedState.user_id }}" class="nav-link">
                      <i class="el-icon-user"></i>我的
                      </router-link>
                  </el-dropdown-item>
                  <el-dropdown-item :divided="true">
                      <a @click="handleLogout" class="nav-link" href="#">
                        <i class="el-icon-switch-button"></i>注销
                      </a>
                  </el-dropdown-item>
                </div>   
              </div>
          </li>
        </ul>

        <router-link v-if="sharedState.is_authenticated && sharedState.user_perms.includes('post')" :to="{ name: 'AddPost' }" @click="collapseClick">
          <span class="btn btn-primary rounded mr-2">发布</span>
        </router-link>

        <ul v-else class="nav navbar-nav navbar-right">
          <li v-if="!sharedState.is_authenticated" class="nav-item" @click="collapseClick">
            <router-link to="/login" class="nav-link ml-2">登录</router-link>
          </li>
          <li v-else class="nav-item">
            <span class="mr-3">无发布权限</span>
          </li>
        </ul>
      </div>

  </nav>
</template>

<script>
import store from '../../store.js'
// 在 JQuery 中使用 axios 的话需要重新导入，
// 不能使用 main.js 中定义的 Vue 全局属性 this.$axios
import axios from 'axios'

export default {
  name: "Navbar",
  data() {
    return {
      sharedState: store.state
    }
  },
  methods: {
    handleLogout (e) {
      store.logoutAction()
      this.$router.push('/login')
    },
    collapseClick() {
      if ($(window).width() < 992) {
        $("#collapse-button").click()
       }
    }
  },
  mounted () {
    // 轮询 /api/users/<int:id>/notifications/ 请求用户的新通知
    // $(function() {
    //   let since = 0
    //   let total_notifications_count = 0  // 总通知计数
    //   let unread_received_comments_count = 0  // 收到的新评论通知计数
    //   let unread_likes_count = 0  // 新的喜欢或赞的通知计数

    //   // 每隔20s获取一次用户通知
    //   setInterval(function() {
    //     if (window.localStorage.getItem('funcampus-token')) {
    //       // 如果用户已登录，才开始请求 API
    //       const payload = JSON.parse(atob(window.localStorage.getItem('funcampus-token').split('.')[1]))
    //       const user_id = payload.user_id
    //       const path = `/api/users/${user_id}/notifications/?since=${since}`
    //       axios.get(path)
    //         .then((response) => {
    //           // handle success
    //           for(var i = 0; i < response.data.length; i++) {
    //             console.log(response.data[i].name)
    //             switch (response.data[i].name) {
    //               case 'unread_received_comments_count':
    //                 console.log('get unread receifekofniuerhfge')
    //                 unread_received_comments_count = response.data[i].payload
    //                 break
    //               case 'unread_likes_count':
    //                 unread_likes_count = response.data[i].payload
    //                 break
    //             }
    //             since = response.data[i].timestamp
    //           }

    //           total_notifications_count = unread_received_comments_count + unread_likes_count
    //           // 每一次请求之后，根据 total_notifications_count 的值来显示或隐藏徽标
    //           $('#new_notifications_count').text(total_notifications_count)
    //           $('#new_notifications_count').css('visibility', total_notifications_count ? 'visible' : 'hidden');
    //         })
    //         .catch((error) => {
    //           // handle error
    //           console.error(error)
    //         })
    //     }
    //   }, 20000)
    // })
  }
}
</script>
