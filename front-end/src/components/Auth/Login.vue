<template>
  <div class="container">
    <div class="row justify-content-center pt-5 mt-3">
        <div class="card shadow p-3 mb-5 bg-white rounded">
          <div class="card-body text-center">
            <form @submit.prevent="onSubmit">
              <div class="form-group mb-4">
                <!-- 用户名 -->
                <div class="input-group g-rounded-left-3 mt-3 mb-5">
                  <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                    <i class="icon-user align-middle"></i>
                  </span>
                  <input 
                  class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                  type="text" v-model="loginForm.username" :class="{'is-invalid': loginForm.usernameError}" id="username" placeholder="用户名" style="height: 40px"> 
                  <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.usernameError }}</div>   
                </div>
                <!-- 密码 -->
                <div class="input-group g-rounded-left-3 mb-5">
                  <span class="input-group-addon g-width-45 g-brd-gray-light-v3 bg-white">
                    <i class="icon-lock align-middle"></i>
                  </span>
                  <input class="form-control form-control-md g-color-black g-bg-white--focus g-brd-gray-light-v3 g-rounded-left-0 g-rounded-right-3 g-py-15 g-px-15"
                  type="password" v-model="loginForm.password" :class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="密码" style="height: 40px">    
                  <div v-show="loginForm.passwordError" class="invalid-feedback">{{ loginForm.passwordError }}</div>
                </div>                
              </div>
              <button type="submit" class="btn btn-primary btn-block g-font-size-12 text-uppercase g-py-12 g-px-25 mb-5">登录</button>
            </form>
            <br/>
            <p>新用户？<router-link to="/register">点击注册</router-link></p>
            <p>忘记密码？<a href="#" @click="onAlert">点击找回密码</a></p>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import store from '../../store.js'

export default {
  name: 'Login',
  components: {},
  data() {
    return {
      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        submitted: false,
        errors: 0,
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onAlert() {
      this.$message({
        center: true,
        showClose: true,
        message: '暂未实现此功能。',
        type: 'warning'
      })
    },
    onSubmit (e) {
      this.loginForm.submitted = true // update state
      this.loginForm.errors = 0

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        this.$message.error({
          center: true,
          showClose: true,
          message: '出错，请检查后再试。'
        })
        return false
      }
      const path = '/api/tokens'
      // axios实现Basic Auth需要在config种设置auth这个属性即可
      this.$axios
      .post(path, {}, {
        auth: {
          'username': this.loginForm.username,
          'password': this.loginForm.password
        }
      })
      .then((response) => {
        window.localStorage.setItem('funcampus-token', response.data.token)
        store.loginAction()
        this.$axios.get('/api/statistics/view')
        const username = JSON.parse(atob(response.data.token.split('.')[1])).user_name
        this.$message({
          center: true,
          showClose: true,
          message: `Welcome ${username}!`,
          type: 'success'
        });
        if (typeof this.$route.query.redirect == 'undefined') {
          this.$router.push('/')
        } else {
          this.$router.replace(this.$route.query.redirect)
        }
      })
      .catch((error) => {
        this.$message.error({
          center: true,
          showClose: true,
          message: '账号和密码不匹配，请重试。'
        })
        // console.log('Login-onSubmit-Catch-Error: ', error)
        if (error.response.status == 401) {
          this.loginForm.usernameError = 'Invalid username or password.'
          this.loginForm.passwordError = 'Invalid username or password.'
        } else {
          // console.log('Login-onSubmit-Catch-Error: ', error.response)
        }
      })
    }
  }
}
</script>
