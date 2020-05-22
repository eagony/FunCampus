<template>
  <div class="container">
    <div class="row card shadow-sm bg-white mb-5 mt-3">
      <div class="card-body mr-auto ml-auto d-block">
        <!-- 内容输入框 -->
        <div class="row mb-5 ml-5 mr-5 mt-5">
            <textarea v-model="postForm.content" class="form-control" id="message-text" rows="8" placeholder="在这里输入内容......"></textarea>
        </div>
        <div class="row d-flex d-inline justify-content-around mb-5 ml-5 mr-5 mt-5">
          <div class="d-flex flex-column">
            <!-- 类型选择 -->
            <div class="p-3">
              <el-select v-model="postForm.type" placeholder="选择类型">
                <el-option
                  v-for="item in post_type_options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </div>
            <!-- 图片上传 -->
            <div class="p-3 mt-3 mb-3">
              <el-upload
                class="avatar-uploader"
                action="http://funcampus.top:5000/upload/picture"
                :show-file-list="false"
                :before-remove="beforeRemove"
                :on-success="handleSuccess"
                :limit="1"
                :before-upload="beforeUpload">
                <img v-if="postForm.picture_url" :src="postForm.picture_url" class="avatar">
                <i v-else class="el-icon-plus align-middle" style="font-size: 28px; line-height: 178px; text-align: center; align-content: center; display: inline;"></i>
                <!-- <img v-else src="../../assets/segi-icon-plus-64.svg" class="avatar-uploader-icon"> -->
                <div slot="tip" class="el-upload__tip text-center">只能上传jpg/png/gif文件，且不超过5M。<br/>预览图比例可能不正常，<br/>但不影响发布后的显示。</div>
              </el-upload>
            </div>

            <div class="p-3">
              <button class="btn btn-primary btn-block mb-5" @click="onSubmitPost">发布</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddPost',
  data () {
    return {
      file: '',
      postForm: {
        title: '',
        content: '',
        picture_url: '',
        type: '',
        contact_type: '',
        contact_id: '',
      },
      post_type_options: [
        {
          value: 'saylove',
          label: '表白'
        }, 
        {
          value: 'lostandfound',
          label: '寻物'
        }, 
        {
          value: 'teamup',
          label: '组队'
        }, 
        {
          value: 'changethings',
          label: '易物'
        },
      ]
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
      this.postForm.picture_url = response.data.url
      // console.log('AddPost-handleSuccess\n\t', "response: ", response.data, "\nfile: ", file, "\nfile list: ", fileList)
    },
    // 提交表单
    onSubmitPost (e) {
      const payload = {
        content: this.postForm.content,
        picture_url: this.postForm.picture_url,
        type: this.postForm.type || 'saylove',
        contact_type: this.postForm.contact_type,
        contact_id: this.postForm.contact_id
      }
      const path = '/api/posts'
      this.$axios.post(path, payload)
      .then((response) => {
        this.$axios.get('/api/statistics/post')
        this.$notify({
          title: '成功',
          message: this.$createElement('i', { style: 'color: black'}, '发布成功，可以前往查看啦！'),
          type: 'success'
        })
        this.$router.push(`/${this.postForm.type}`)
        this.postForm.content = ''
        this.postForm.picture_url = ''
        this.postForm.type = ''
        this.postForm.contact_type = ''
        this.postForm.contact_id = ''
      })
      .catch((error) => {
        // console.log('AddPost-onSubmitPost-Catch-Error: ', error)
      })
    }
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
    display:block;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #f3d3e7;
    line-height: 178px;
    text-align: center;
    align-content: center;
    display: inline;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>