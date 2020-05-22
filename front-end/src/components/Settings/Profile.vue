<template>
  <section>
    <div class="container">
      <div class="g-brd-around g-brd-gray-light-v4 g-pa-20 g-mb-40">
        <div class="row">
          <div class="col-sm-3 g-mb-40 g-mb-0--lg">
            <!-- 头像 -->
            <div class="g-mb-20">
              <img class="img-fluid w-100 rounded" :src="user.avatar_url" alt="Profile Picture"/>
            </div>

            <!-- 修改资料 -->
            <router-link v-if="$route.params.id == sharedState.user_id" :to="{ name: 'EditProfile' }"  class="btn btn-block u-btn-outline-primary g-rounded-50 g-py-12 g-mb-10">
              <i class="icon-user-follow g-pos-rel g-top-1 g-mr-5"></i> 编辑资料
            </router-link>
          </div>

          <div class="col-sm-9">
            <!-- 用户名 -->
            <div class="d-flex align-items-center justify-content-sm-between g-mb-5">
              <h2 v-if="user.name" class="g-font-weight-300 g-mr-10">{{ user.name }}</h2>
              <h2 v-else class="g-font-weight-300 g-mr-10">{{ user.username }}</h2>
            </div>

            <!-- 学校 -->
            <h4 v-if="user.school" class="h6 g-font-weight-300 g-mb-10">
              <i class="icon-home g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>学校：{{ user.school }}
            </h4>

            <!-- 上次登录 -->
            <h4 v-if="user.last_seen" class="h6 g-font-weight-300 g-mb-10">
              <i class="icon-eye g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>上次登录：{{ $moment(user.last_seen).format('LLL') }}
            </h4>

            <!-- 注册时间 -->
            <h4 v-if="user.registration_date" class="h6 g-font-weight-300 g-mb-10">
              <i class="icon-badge g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>注册时间：{{ $moment(user.registration_date).format('LLL') }}
            </h4>

            <!-- 邮箱 -->
            <ul class="list-inline g-font-weight-300">
              <li class="list-inline-item g-mr-20">
                <i class="icon-check g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i>已验证用户
              </li>
              <li v-if="user.email" class="list-inline-item g-mr-20">
                <i class="icon-link g-pos-rel g-top-1 g-color-gray-dark-v5 g-mr-5"></i> <a class="g-color-main g-color-primary--hover" :href="'mailto:' + user.email"> {{ user.email }}</a>
              </li>
            </ul>

            <!-- 关于 -->
            <div v-if="user.about_me">
              <div class="u-divider u-divider-db-dashed u-divider-center g-brd-gray-light-v2 g-mt-50 g-mb-20">
                <i class="u-divider__icon u-divider__icon---indented g-bg-gray-light-v4 g-color-gray-light-v1 rounded-circle">ME</i>
              </div>
              <p class="lead g-line-height-1_8">{{ user.about_me }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import store from '../../store.js'
import EditProfile from './EditProfile'

export default {
  name: 'Profile',
  components: {
    EditProfile
  },
  data() {
    return {
      sharedState: store.state,
      user: {}
    }
  },
  methods: {
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
      .then((response) => {
        this.user = response.data
      })
      .catch((error) => {
        // console.log('Profile-getUser-catch-error: ',error)
      });
    }
  },
  created() {
    const user_id = this.$route.params.id
    this.getUser(user_id)
  },
  // 当id变化后重新加载数据
  beforeRouteUpdate(to, from, next) {
    this.getUser(to.params.id)
    next()
  }
}
</script>
