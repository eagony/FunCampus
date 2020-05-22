<template>
  <div>
    <!-- Panel Header --> 
    <div class="card-header bg-white g-font-size-16 rounded-0 mr-0 mt-0 mb-0 d-flex align-items-center justify-content-between border-0">
      <h3 class="h6 mb-0">
        <i class="icon-people g-pos-rel g-top-1 g-mr-5"></i> 用户列表 <small v-if="users">(共 {{ users._meta.total_items }} 个, {{ users._meta.total_pages }} 页)</small>
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

    <el-table :data="users.items" class="mb-3 ml-2" style="width: 100%">
      <el-table-column fixed prop="id" label="#" width="40"></el-table-column>
      <el-table-column prop="username" label="Username" width="90"></el-table-column>
      <el-table-column prop="name" label="Name"></el-table-column>
      <el-table-column prop="school" label="School"></el-table-column>
      <el-table-column prop="role" label="Role"></el-table-column>
      <el-table-column label="操作" width="150">
        <template slot-scope="scope">
          <el-button size="mini">
            <router-link :to="{ name: 'AdminEditUser', params: { id: scope.row.id } }" >编辑</router-link>
          </el-button>
          <el-button size="mini" type="danger" 
          @click="onDeleteUser(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination #04 -->
    <div v-if="users">
      <pagination
        :cur-page="users._meta.page"
        :per-page="users._meta.per_page"
        :total-pages="users._meta.total_pages">
      </pagination>
    </div>
    <!-- End Pagination #04 -->
  </div>
</template>

<script>
import Pagination from '../Base/Pagination'

export default {
  name: 'Users',  //this is the name of the component
  components: {
    Pagination
  },
  data () {
    return {
      users: ''
    }
  },
  methods: {
    getUsers () {
      let page = 1
      let per_page = 10
      if (typeof this.$route.query.page != 'undefined') {
        page = this.$route.query.page
      }

      if (typeof this.$route.query.per_page != 'undefined') {
        per_page = this.$route.query.per_page
      }

      const path = `/api/users?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.users = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onDeleteUser (user) {
      var username = user.name || user.username

      this.$swal.fire({
        title: "Are you sure?",
        text: "该操作将彻底删除 [ " + username + " ], 请慎重",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!'
      }).then((result) => {
        if(result.value) {
          const path = `/api/users/${user.id}`
          this.$axios.delete(path)
            .then((response) => {
              // handle success
              this.$swal.fire('Deleted', 'You successfully deleted this user', 'success')
              this.getUsers()
            })
            .catch((error) => {
              // handle error
              // console.log('Users-onDeleteUser-Catch-Error: ', error.response.data)
              this.$message.error({          
                center: true,
                showClose: true,
                message: error.response.data.message
              })
            })
        } else {
          this.$swal.fire('Cancelled', 'The user is safe :)', 'error')
        }
      })
    }
  },
  created () {
    this.getUsers()
  },
  // 当路由变化后(比如变更查询参数 page 和 per_page)重新加载数据
  beforeRouteUpdate (to, from, next) {
    next()
    this.getUsers()
  }
}
</script>