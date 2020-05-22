<template>
  <div class="container">
      <div class="row justify-content-center pt-5 mt-3">
        <div class="card shadow p-3 mb-5 bg-white rounded">
          <div class="card-body text-center">
            <form @submit.prevent.once="onSubmit">

              <!-- 用户名 -->
              <div class="input-group g-rounded-left-3 mt-3 mb-5">
                <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                  <i class="icon-user align-middle"></i>
                </span>
                <input 
                class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                type="text" v-model="registerForm.username" :class="{'is-invalid': registerForm.usernameError}" id="username" placeholder="用户名(非中文)" style="height: 40px"> 
                <div v-show="registerForm.usernameError" class="invalid-feedback">{{ registerForm.usernameError }}</div>
              </div>

              <!-- 学校 -->
              <div class="input-group g-rounded-left-3 mt-3 mb-5">
                <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                  <i class="el-icon-school align-middle"></i>
                </span>
                <input 
                class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                type="text" v-model="registerForm.school" :class="{'is-valid': registerForm.schoolError}" id="school" placeholder="学校(中文，必填)" style="height: 40px"> 
                <div v-show="registerForm.schoolError" class="invalid-feedback">{{ registerForm.schoolError }}</div>
              </div>

              <!-- 邮箱 -->
              <small v-if="!registerForm.emailError" id="emailHelp" class="form-text text-muted">邮箱仅用于找回密码使用。</small>
              <div class="input-group g-rounded-left-3 mt-3 mb-5">
                <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                  <i class="el-icon-message align-middle"></i>
                </span>
                <input 
                class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                type="email" v-model="registerForm.email" :class="{'is-invalid': registerForm.emailError}" id="email" aria-describedby="emailHelp" placeholder="邮箱(必填)" style="height: 40px"> 
                <div v-show="registerForm.emailError" class="invalid-feedback">{{ registerForm.emailError }}</div>
              </div>

              <!-- 密码 -->
              <div class="input-group g-rounded-left-3 mt-3">
                <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                  <i class="icon-lock align-middle"></i>
                </span>
                <input 
                class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                type="password" v-model="registerForm.password" :class="{'is-valid': registerForm.passwordError}" id="password" placeholder="密码" style="height: 40px"> 
              </div>
              <!-- 确认密码 -->
              <div class="input-group g-rounded-left-3 mt-3 mb-5">
                <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                  <i class="icon-lock align-middle"></i>
                </span>
                <input 
                class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                type="password" v-model="registerForm.password_confirm" :class="{'is-valid': registerForm.passwordError}" id="password-confirm" placeholder="确认密码" style="height: 40px"> 
                <div v-if="registerForm.passwordError" class="invalid-feedback">{{ registerForm.passwordError }}</div>
              </div>
              <button type="submit" class="btn btn-primary btn-block g-font-size-12 text-uppercase g-py-12 g-px-25 mb-5">注册</button>
            </form>
          </div>
        </div>

      </div>
  </div>
</template>

<script>
import store from '../../store.js'

export default {
  name: 'Register',
  data () {
    return {
      registerForm: {
        username: '',
        school: '',
        email: '',
        password: '',
        password_confirm: '',
        submitted: false,
        errors: 0,
        usernameError: null,
        schoolError: null,
        emailError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.registerForm.submitted = true
      this.registerForm.errors = 0
      if (!this.registerForm.username) {
        this.registerForm.errors++
        this.registerForm.usernameError = '用户名必填。'
      } else {
        this.registerForm.usernameError = null
      }
      if (!this.registerForm.school) {
        this.registerForm.errors++
        this.registerForm.schoolError = '学校名必填。'
      } else {
        this.registerForm.schoolError = null
      }
      if (!this.registerForm.email) {
        this.registerForm.errors++
        this.registerForm.emailError = '邮箱必填。'
      } else if (!this.validEmail(this.registerForm.email)) {
        this.registerForm.errors++
        this.registerForm.emailError = '邮箱格式不正确。'
      } else {
        this.registerForm.emailError = null
      }
      if (!this.registerForm.password) {
        this.registerForm.errors++
        this.registerForm.passwordError = '密码必填。'
      } else {
        this.registerForm.passwordError = null
      }
      if (!this.registerForm.password_confirm) {
        this.registerForm.errors++
        this.registerForm.passwordError = '确认密码必填。'
      } else {
        this.registerForm.passwordError = null
      }
      if (this.registerForm.password !== this.registerForm.password_confirm) {
        this.registerForm.errors++
        this.registerForm.passwordError = '两次密码不一致。'
      } else {
        this.registerForm.passwordError = null
      }
      if (this.registerForm.errors > 0) {
        let totalError = ''
        if (this.registerForm.usernameError) {totalError = totalError + this.registerForm.usernameError + ' '}
        if (this.registerForm.schoolError) {totalError = totalError + this.registerForm.schoolError + ' '}
        if (this.registerForm.emailError) {totalError = totalError + this.registerForm.emailError + ' '}
        if (this.registerForm.passwordError) {totalError += this.registerForm.passwordError}

        // console.log(this.registerForm.password, this.registerForm.password_confirm, this.registerForm.password !== this.registerForm.password_confirm, this.registerForm.passwordError)
        this.$message.error({
          center: true,
          showClose: false,
          message: '注册失败：' + totalError + '将重新注册。'
        })
        setTimeout("location.reload()",300);
        return false
      }
      const path = '/api/users'
      const payload = {
        username: this.registerForm.username,
        school: this.registerForm.school,
        email: this.registerForm.email,
        password: this.registerForm.password
      }
      this.$axios
        .post(path, payload)
        .then((response) => {
          // handle success
          // 数据统计user+1
          this.$axios.get('/api/statistics/user')

          this.$message({
            center: true,
            showClose: true,
            message: `注册成功，现在可以登录了...`,
            type: 'success'
            })
          this.$router.push('/login')
        })
        .catch((error) => {
          // handle error
          this.$message.error({
            center: true,
            showClose: false,
            message: '注册失败：' + error.response.data.message,
            })
          for (var field in error.response.data.message) {
            if (field == 'username') {
              this.registerForm.usernameError = error.response.data.message.username
            } else if (field == 'school') {
              this.registerForm.schoolError = error.response.data.message.school
            } else if (field == 'email') {
              this.registerForm.emailError = error.response.data.message.email
            } else if (field == 'password') {
              this.registerForm.passwordError = error.response.data.message.password
            }
          }
        })
    },
    validEmail: function (email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  }
}
</script>
