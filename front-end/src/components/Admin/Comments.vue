<template>
  <div>
    <!-- Panel Header -->
    <div class="card-header bg-white g-font-size-16 rounded-0 mr-0 mt-0 mb-0 d-flex align-items-center justify-content-between border-0">
      <h3 class="h6 mb-0">
        <i class="icon-notebook g-pos-rel g-top-1 g-mr-5"></i> Comment列表 <small v-if="comments">(共 {{ comments._meta.total_items }} 个, {{ comments._meta.total_pages }} 页)</small>
      </h3>

      <div class="dropdown g-mb-10 g-mb-0--md">
        <span class="d-block g-color-primary--hover g-cursor-pointer g-mr-minus-5 g-pa-5" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="icon-options-vertical g-pos-rel g-top-1"></i>
        </span>
        <div class="dropdown-menu dropdown-menu-right rounded-0 g-mt-10">
          <router-link :to="{ path: $route.path, query: { page: 1, per_page: 1 }}" class="dropdown-item g-px-10">
            <i class="icon-plus g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 1 个
          </router-link>
          <router-link :to="{ path: $route.path, query: { page: 1, per_page: 5 }}" class="dropdown-item g-px-10">
            <i class="icon-layers g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 5 个
          </router-link>
          <router-link :to="{ path: $route.path, query: { page: 1, per_page: 10 }}" class="dropdown-item g-px-10">
            <i class="icon-wallet g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 10 个
          </router-link>

          <div class="dropdown-divider"></div>

          <router-link :to="{ path: $route.path, query: { page: 1, per_page: 20 }}" class="dropdown-item g-px-10">
            <i class="icon-fire g-font-size-12 g-color-gray-dark-v5 g-mr-5"></i> 每页 20 个
          </router-link>
        </div>
      </div>
    </div>
    <!-- End Panel Header -->

    <!-- Striped Rows -->
    <el-table :data="comments.items" class="mb-3 ml-2" style="width: 100%">
      <el-table-column fixed prop="id" label="#" width="80"></el-table-column>

      <el-table-column prop="content" label="Content" width="500"></el-table-column>
      <el-table-column label="Author" width="100">
        <template slot-scope="scope">
          <router-link :to="{ path: `/user/${scope.row.author.id}` }">{{ scope.row.author.name || scope.row.author.username }}</router-link>
        </template>
      </el-table-column>             
      <el-table-column label="操作" width="80">
        <template slot-scope="scope">
          <el-button size="mini" type="danger" 
          @click="onDeleteComment(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- End Striped Rows -->

    <!-- Pagination #04 -->
    <div v-if="comments">
      <pagination
        :cur-page="comments._meta.page"
        :per-page="comments._meta.per_page"
        :total-pages="comments._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import Pagination from '../Base/Pagination'

export default {
  name: 'comments',  //this is the name of the component
  components: {
    Pagination
  },
  data () {
    return {
      comments: ''
    }
  },
  methods: {
    getComments () {
      let page = 1
      let per_page = 10
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      const path = `/api/comments?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.comments = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onDeleteComment (comment) {
      this.$swal.fire({
        title: "Are you sure?",
        text: "删除操作还会删除该评论的所有子孙评论，建议使用 [屏蔽] 功能仅禁止该评论显示",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/comments/${comment.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal.fire('Deleted', 'You successfully deleted this comment', 'success')
              this.getComments()
            })
            .catch((error) => {
              // handle error
              // console.log('Comments-onDelete-Catch-Error: ',error.response.data)
              this.$message.error({
                center: true,
                showClose: true,
                message: error.response.data.message
                })
            })
        } else {
          this.$swal.fire('Cancelled', 'The comment is safe :)', 'error')
        }
      })
    },
    onDisabledComment (comment) {
      const path = `/api/comments/${comment.id}`
      this.$axios.put(path, { "disabled": true })
        .then((response) => {
          // handle success
          this.$swal.fire('Success', 'You successfully disabled this comment', 'success')
          this.getComments()
        })
        .catch((error) => {
          // handle error
          // console.log('Comments-onDisabledComment-Catch-Error: ', error.response.data)
          this.$message.error({
            center: true,
            showClose: true,
            message: error.response.data.message
            })
        })
    },
    onEnabledComment (comment) {
      const path = `/api/comments/${comment.id}`
      this.$axios.put(path, { "disabled": false })
        .then((response) => {
          // handle success
          this.$swal.fire('Success', 'You successfully enabled this comment', 'success')
          this.getComments()
        })
        .catch((error) => {
          // handle error
          // console.log('Comments-onEnabledComment-Catch-Error: ', error.response.data)
          this.$message.error({          
            center: true,
            showClose: true,
            message: error.response.data.message
          })
        })
    }
  },
  created () {
    this.getComments()
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getComments()
  }
}
</script>