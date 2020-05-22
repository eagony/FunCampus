<template>
  <div v-if="posts" class="container">
    <div class="row card shadow-sm bg-white mb-5 mt-3">
      <!-- Panel Header -->
      <div class="row card-body d-flex align-items-center justify-content-between g-bg-gray-light-v5 border-0 ml-2">
        <h3 class="h6 mb-0">
          <i class="el-icon-postcard g-pos-rel g-top-1 g-mr-5"></i> All Posts <small v-if="posts">(共 {{ posts._meta.total_items || 0 }} 篇, {{ posts._meta.total_pages || 0}} 页)</small>
        </h3>
        <div class="dropdown g-mb-10 g-mb-0--md">
          <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="icon-options-vertical g-pos-rel g-top-1"></i>
          </span>
          <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
            <router-link :to="{ path: $route.path, query: { type: postType, page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
              <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 篇
            </router-link>
            <router-link :to="{ path: $route.path, query: { type: postType, page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
              <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 篇
            </router-link>
            <router-link :to="{ path: $route.path, query: { type: postType, page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
              <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 篇
            </router-link>
            <div class="dropdown-divider"></div>
            <router-link :to="{ path: $route.path, query: { type: postType, page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
              <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 篇
            </router-link>
          </div>
        </div>
      </div>
      <!-- End Panel Header -->

      <!-- Panel Body -->
      <div v-if="posts" class="row d-inline justify-content-center ml-0 mr-0">
        <postbox
        v-for="(post, index) in posts.items"
        :key="index"
        :postID="post.id"
        :userID="post.author.id"
        :userName="post.author.name || post.author.username"
        :user-avatar="post.author.avatar"
        :post-likes="post.likes"
        :postContent="post.content"
        :postPictureURL="post.picture_url"
        :userSchool="post.author.school"
        :postTime="$moment(post.timestamp).fromNow()"
        :contactID="post.contact_id"
        :hasPicture="false"
        ></postbox>
      </div>
      <!-- End Panel Body -->

      <!-- Pagination #04 -->
      <div class="row ml-auto mr-auto d-block mt-4 mb-3">
        <nav aria-label="Page navigation" class="">
          <ul class="pagination pagination-lg justify-content-center">
            <li class="page-item">
                <router-link
                :to="{ path: $route.path, query: { type: postType, page: posts._meta.page - 1, per_page: posts._meta.per_page }}"
                class="page-link"
                aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
                </router-link>
            </li>
            <li
            v-if="page != 'NaN'"
            v-for="(page, index) in iter_pages"
            :key="index"
            class="page-item">
              <router-link :to="{ path: $route.path, query: { type: postType, page: page, per_page: posts._meta.per_page} }" class="page-link">
                {{ page }}
              </router-link>
            </li>
            <li v-else class="page-item">
              <span class="g-pa-12-19 page-link">...</span>
            </li>
            <li class="page-item">
              <router-link
              :to="{ path: $route.path, query: { type: postType, page: posts._meta.page + 1, per_page: posts._meta.per_page} }"
              aria-label="Next"
              class="page-link">
                <span aria-hidden="true">&raquo;</span>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>
      <!-- End Pagination #04 -->
    </div>
  </div>
</template>

<script>
import store from '../store.js'
import PostBox from '../components/Base/PostBox'

export default {
    name: 'BaseView',
    props: ['postType', 'updateFlag'],
    components: {
        postbox: PostBox
    },
    data() {
      return {
        iter_pages: [], //分页导航栏
        posts: 
        {
          _meta: 
          {
            page: '',
            per_page: ''
          }
        },
        isRouterAlive: true,
        sharedState: store.state
      }
    },
    methods: {
      getPosts () {
        let page = this.$route.query.page || 1
        let per_page = this.$route.query.per_page || 7
        
        const path = `/api/posts?type=${this.postType}&page=${page}&per_page=${per_page}`
        this.$axios.get(path)
        .then((response) => {
          // handle success
          this.posts = response.data
          // 构建分页导航，当前页左右各显示2页，like 1, 2, ... 7, 8, 9, 10, 11 ... 30, 31
          let arr = [1, 2, this.posts._meta.page-2, this.posts._meta.page-1, this.posts._meta.page, this.posts._meta.page+1, this.posts._meta.page+2, this.posts._meta.total_pages-1, this.posts._meta.total_pages]
          // 小于1或者大雨最大页数的都是非法的需要去除
          arr = arr.filter(item => item > 0 && item <= this.posts._meta.total_pages)
          // 去除重复项
          this.iter_pages = [...new Set(arr)]
          // 假设当前页为1，总页数为6或6以上时，在倒数第2个位置插入特殊标记  1, 2, 3 ... 5, 6
          if (this.posts._meta.page + 2 < this.posts._meta.total_pages - 2) {
            this.iter_pages.splice(-2, 0, 'NaN')
          }
          // 当前页为6或6以上时，在第3个位置插入特殊标记  1, 2 ... 4, 5, 6
          if (this.posts._meta.page - 3 > 2) {
            this.iter_pages.splice(2, 0, 'NaN')
          }
        })
        .catch((error) => {
          // console.log('BaseView-getPosts-catch-error: ', error)
        })
      }
    },
    created () {
      this.getPosts()
    },
    watch: {
      updateFlag() {
        this.getPosts()
      }
    }
}
</script>
