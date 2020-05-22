<template>
  <div class="container g-pt-20">
    <div class="row">
      <!-- 左边菜单栏 -->
      <div class="col-lg-3 g-mb-50">
        <aside class="g-brd-around g-brd-gray-light-v4 rounded g-px-20 g-py-30">
          <!-- 用户头像 -->
          <div v-if="user" class="text-center g-pos-rel g-mb-30">
            <div class="g-width-100 g-height-100 mx-auto mb-3">
              <img class="img-fluid rounded" :src="user.avatar_url" alt="用户头像">
            </div>

            <span class="d-block mt-5">{{ user.name || user.username }}</span>

            <router-link :to="{ path: `/user/${sharedState.user_id}` }">
              <span class="" title="Go To Your Profile"
                    data-toggle="tooltip"
                    data-placement="top">
                <i class=""></i>
              </span>
            </router-link>
          </div>
          <!-- End 用户头像 -->

          <hr class="g-brd-gray-light-v4 g-my-30">

          <!-- 菜单列表 -->
          <ul class="list-unstyled mb-0 text-center">
            <li class="g-pb-3">
              <router-link :to="{ name: 'RecivedComments' }" class="d-block align-middle rounded">
                <span><i class=""></i></span>
                评论
                <span v-if="notifications.unread_recived_comments_count" class="">{{ notifications.unread_recived_comments_count }}</span>
              </router-link>
            </li>
            <el-divider></el-divider>
            <li class="g-py-3">
              <router-link :to="{ name: 'RecivedMessages' }" class="d-block align-middle rounded">
                <span ><i class=""></i></span>
                消息
              </router-link>
            </li>
            <el-divider></el-divider>
            <li class="g-py-3">
              <router-link :to="{ name: 'Follows' }" class="d-block align-middle rounded">
                <span ><i class=""></i></span>
                关注
                <span v-if="notifications.unread_follows_count" >{{ notifications.unread_follows_count }}</span>
              </router-link>
            </li>
            <el-divider></el-divider>
            <li class="g-py-3">
              <router-link :to="{ name: 'Likes' }" class="d-block align-middle rounded">
                <span ><i class=""></i></span>
                点赞
                <span v-if="notifications.unread_likes_count" >{{ notifications.unread_likes_count }}</span>
              </router-link>
            </li>
            <el-divider></el-divider>
            <li class="g-py-3">
              <router-link :to="{ name: 'FollowingPosts' }" class="d-block align-middle rounded">
                <span><i class=""></i></span>
                动态
                <span v-if="notifications.unread_followeds_posts_count" >{{ notifications.unread_followeds_posts_count }}</span>
              </router-link>
            </li>
          </ul>
          <!-- End 菜单列表 -->
        </aside>
      </div>
      <!-- End 左边菜单栏 -->

      <!-- 右边子路由匹配后，显示对应的组件 -->
      <div class="col-lg-9 g-mb-50">

        <!-- <router-view></router-view> -->
        <div class="text-center align-middle mt-5">
          <span>开发中......</span>
        </div>

      </div>
      <!-- End 嵌套路由 -->
    </div>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Notifications',  
  data () {
    return {
      sharedState: store.state,
      user: '',
      notifications: {
        unread_recived_comments_count: 0,
        unread_follows_count: 0,
        unread_likes_count: 0,
        unread_followeds_posts_count: 0
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
    },
    getUserNotifications (id) {
      let since = 0
      const path = `/api/users/${id}/notifications/?since=${since}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          const len = response.data.length
          for(var i = 0; i < len; i++) {
            switch (response.data[i].name) {
              case 'unread_recived_comments_count':
                this.notifications.unread_recived_comments_count = response.data[i].payload
                break
              
              case 'unread_follows_count':
                this.notifications.unread_follows_count = response.data[i].payload
                break
              
              case 'unread_likes_count':
                this.notifications.unread_likes_count = response.data[i].payload
                break
              
              case 'unread_followeds_posts_count':
                this.notifications.unread_followeds_posts_count = response.data[i].payload
                break
            }
            since = response.data[i].timestamp
          }
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
    this.getUserNotifications(user_id)
    // tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip(); 
    })

  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUserNotifications(this.sharedState.user_id)
  }
}
</script>