<template>
  <div>
    <h1>Add Role</h1>
    <form @submit.prevent="onSubmit">
      <div class="form-group" :class="{'u-has-error-v1': roleForm.slugError}">
        <label for="slug">Slug</label>
        <input type="text" v-model="roleForm.slug" class="form-control" id="slug" placeholder="">
        <small class="form-control-feedback" v-show="roleForm.slugError">{{ roleForm.slugError }}</small>
      </div>
      <div class="form-group" :class="{'u-has-error-v1': roleForm.nameError}">
        <label for="name">Name</label>
        <input type="text" v-model="roleForm.name" class="form-control" id="name" placeholder="">
        <small class="form-control-feedback" v-show="roleForm.nameError">{{ roleForm.nameError }}</small>
      </div>
      <div class="form-group">
        <label for="permissions">Permissions</label>
        <div>
          <div v-for="(perm, index) in perms" :key="index" class="form-check form-check-inline mb-0">
            <label class="form-check-label mr-2">
              <input class="form-check-input mr-1" type="checkbox" :id="perm.dec" :value="perm.dec" v-model="checkPerms">{{ perm.name }}
            </label>
          </div>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'AddRole',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      roleForm: {
        slug: '',
        name: '',
        permissions: [],
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        slugError: null,
        nameError: null
      },
      perms: null,
      checkPerms: []
    }
  },
  methods: {
    getPerms () {
      const path = `/api/roles/perms`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          this.perms = response.data
        })
        .catch((error) => {
          // handle error
          console.error(error)
        })
    },
    onSubmit (e) {
      this.roleForm.errors = 0  // 重置

      if (!this.roleForm.slug) {
        this.roleForm.errors++
        this.roleForm.slugError = 'Slug required.'
      } else {
        this.roleForm.slugError = null
      }

      if (!this.roleForm.name) {
        this.roleForm.errors++
        this.roleForm.nameError = 'Role name required.'
      } else {
        this.roleForm.nameError = null
      }

      if (this.roleForm.errors > 0) {
        // 如果slug或name为空时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = `/api/roles`
      const payload = {
        slug: this.roleForm.slug,
        name: this.roleForm.name,
        permissions: this.checkPerms
      }
      this.$axios.post(path, payload)
        .then((response) => {
          // handle success
          this.$message({
              center: true,
              showClose: true,
              message: 'Successed add a new role.',
              type: 'success'
              })
          this.$router.push({name: 'AdminRoles'})
        })
        .catch((error) => {
          // handle error
          for (var field in error.response.data.message) {
            if (field == 'slug') {
              this.roleForm.slugError = error.response.data.message[field]
            } else if (field == 'name') {
              this.roleForm.nameError = error.response.data.message[field]
            } else {
              this.$message.error({
                center: true,
                showClose: true,
                message: error.response.data.message[field],
              })
            }
          }
        })
    }
  },
  created () {
    this.getPerms()
  },
}
</script>