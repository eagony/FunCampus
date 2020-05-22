<template>
  <div class="container">
    <div class="row card shadow-sm bg-white mb-5 mt-1">
      <div class="card-body  g-bg-gray-light-v5 border-0 g-mb-15">
        <div class="row d-flex d-inline justify-content-around mb-5 ml-5 mr-5 mt-5">
          <div class="d-flex flex-column">
            <div class="p-3 text-center">
              <el-upload
                class="avatar-uploader"
                action="http://funcampus.top:5000/upload/picture"
                :show-file-list="false"
                :before-remove="beforeRemove"
                :on-success="handleSuccess"
                :limit="1"
                :before-upload="beforeUpload">
                <img v-if="profileForm.avatar_url" :src="profileForm.avatar_url" class="avatar">
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                <div slot="tip" class="el-upload__tip text-center">点击图片上传头像，<br/>只能上传jpg/png/gif文件，且不超过5M。</div>
              </el-upload>
            </div>
            <div class="p-3">
              <label for="name">昵称：</label>
              <input type="text" v-model="profileForm.name" class="form-control" id="name" placeholder="">
            </div>
            <div class="p-3">
              <label for="location">学校：</label>
              <input type="text" v-model="profileForm.school" class="form-control" id="school" placeholder="">
            </div>
            <div class="p-3">       
              <label for="about_me">关于：</label>
              <textarea v-model="profileForm.about_me" class="form-control" id="about_me" rows="5" placeholder=""></textarea>     
            </div>
            <div class="p-3">
              <button @click="onSubmit" class="btn btn-primary btn-block g-font-size-12 text-uppercase g-py-12 g-px-25 mb-5">提交</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '../../store.js'

export default {
  name: 'EditProfile',
  data () {
    return {
      sharedState: store.state,
      profileForm: {}
    }
  },
  methods: {
    beforeUpload(file) {
      const isJPG = (file.type === 'image/jpeg' || file.type === 'image/jpg' || file.type === 'image/png' || file.type === 'image/gif')
      const isLt5M = file.size / 1024 / 1024 < 5

      if (!isJPG) {
        this.$message.error({          
          center: true,
          showClose: true,
          message: '图片格式不支持!'
        })
      }
      if (!isLt5M) {
        this.$message.error({          
          center: true,
          showClose: true,
          message: '图片大小超过5MB!'
        })
      }
      return isJPG && isLt5M
    },
    handleExceed(files, fileList) {
      this.$message.warning({          
        center: true,
        showClose: true,
        message: '只能上传一张图哈！'
      })
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`移除${ file.name }？`)
    },
    handleSuccess(response, file, fileList) {
      this.profileForm.avatar_url = response.data.url
    },
    getUser (id) {
      const path = `/api/users/${id}`
      this.$axios.get(path)
      .then((response) => {
        this.profileForm = response.data
      })
      .catch((error) => {
        // console.log('EditProfile-getUser-catch-error: ', error)
      });
    },
    onSubmit (e) {
      const user_id = this.sharedState.user_id
      const path = `/api/users/${user_id}`
      const payload = {
        name: this.profileForm.name,
        school: this.profileForm.school,
        about_me: this.profileForm.about_me,
        avatar_url: this.profileForm.avatar_url
      }
      this.$axios.put(path, payload)
      .then((response) => {
        this.$message({
          center: true,
          showClose: true,
          message: '资料修改成功!',
          type: 'success'
        })
        this.$router.push({
          name: 'Profile',
          params: {id: user_id}
        })
      })
      .catch((error) => {
        // console.log('EditProfile-onSubmit-catch-error: ',error.response.data)
      })
    }
  },
  created() {
    const user_id = this.sharedState.user_id
    this.getUser(user_id)
  }
}
</script>


<style>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 8px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    margin-left: auto; 
    margin-right:auto; 
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>