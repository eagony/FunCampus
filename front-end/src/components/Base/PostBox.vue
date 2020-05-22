<template>
  <div class="container mb-3 mt-3">
    <el-card class="box-card">
      <div slot="header">
        <el-avatar class="mr-3 align-middle" :src="userAvatar || 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'" :size="25"></el-avatar>
        
        <router-link style="color: black;" :to="{ name: 'Profile', params: { id: userID }}">
          <span>{{ userName }}</span>
        </router-link>

        <el-divider direction="vertical"></el-divider>
      
        <span>{{ userSchool }}</span>
        <div class="d-inline">
          
        </div>
        <el-button  @click="onDeletePost"
        v-if="sharedState.is_authenticated && sharedState.user_perms.includes('admin')" 
        type="text" icon="el-icon-delete" class="align-middle ml-1" size="small" circle
        style="float: right"></el-button>

        <el-button @click="onLikeOrUnlike" class="align-middle" icon="icon-like" size="small" type="text" circle style="float: right"> {{ likes }}</el-button>
      </div>

      <div class="text item ">
        <p>{{ postContent }}</p>
        <div class="d-flex justify-content-center">
          <el-button v-if="!showCommentBox" type="text" size="small" round icon="el-icon-arrow-down" @click="onShowCommentBox"></el-button>
          <!-- <el-button v-else type="text" size="small" round icon="el-icon-arrow-up" @click="onShowCommentBox"></el-button> -->
        </div>
        <div v-if="this.showCommentBox" class="justify-content-center">

          <el-divider><i class="el-icon-picture"></i></el-divider>

          <div class="align-middle text-center">
            <el-image v-if="postPictureURL" :src="postPictureURL"></el-image>
            <span v-else>没有图片哦</span>
          </div>

          <el-divider><i class="el-icon-s-comment"></i></el-divider>
          
          <commentbox :postID="this.postID"></commentbox>

          <el-divider class="mt-5">
            <el-button v-if="showCommentBox" type="text" size="small" circle icon="el-icon-arrow-up" @click="onShowCommentBox"></el-button>
          </el-divider>

        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import store from '../../store'
import CommentBox from './CommenBox'

export default {
  props: ['userID', 'userAvatar', 'userName', 'userSchool', 'postLikes', 'postID', 'postContent', 'postPictureURL', 'postTime', 'hasPicture', 'contactID'],
  components: {
    commentbox: CommentBox
  },
  data() {
    return {
      likes: 0,
      comments: {},
      showCommentBox: false,
      sharedState: store.state
    }
  },
  methods: {
    onShowCommentBox () {
      if (this.showCommentBox == false) {              
        this.showCommentBox = true
      } else {
        this.showCommentBox = false
      }
    },
    // 获取Post的评论
    getPostComments (id) { 
      let page = 1
      let per_page = 100
      const path = `/api/posts/${this.postID}/comments?page=${page}&per_page=${per_page}`
      this.$axios
          .get(path)
          .then((response) => {
            this.comments = response.data.items
          })
          .catch((error) => {
            // console.log('PostBox-getPostComments-Catch-Error: ', error)
          })
    },
    getPostLikes() {
      const path = `/api/posts/${this.postID}/likes`
      this.$axios.get(path).then((response) => {
        this.likes = response.data.likes
      }).catch((error) => {
        // console.log('PostBox-getPostLikes-Catch-Error: ', error)
      })
    },
    onDeletePost() {
      const path = `/api/posts/${this.postID}`
      this.$axios.delete(path)
      .then((response) => {
        // handle success
        this.$message({
          center: true,
          showClose: true,
          message: '删除成功！',
          type: 'success'
        })

        // this.$notify({
        //   title: '成功',
        //   message: this.$createElement('i', { style: 'color: black'}, '删除成功！'),
        //   type: 'success'
        // })

        setTimeout("location.reload()",500);
        // this.$destroy()

      })
      .catch((error) => {
        // handle error
        this.$message.error({          
        center: true,
        showClose: true,
        message: '错误' + error.response
        })
      })
    },
    onLikeOrUnlike () {
      // 用户需要先登录
      if (!this.sharedState.is_authenticated) {
        this.$message.error({        
          center: true,
          showClose: true,
          message: '需要先登录才能点赞...'
        })
        this.$router.push('/login')
      }
      // let path = ''
      // if (comment.likers_id.indexOf(this.sharedState.user_id) != -1) {
      //   // 当前登录用户已点过赞，再次点击则取消赞
      //   path = `/api/comments/${comment.id}/unlike`
      // } else {
      //   path = `/api/comments/${comment.id}/like`
      // }
      const path = `api/posts/${this.postID}/likeorunlike`
      this.$axios.get(path)
        .then((response) => {
          // handle success
          // console.log('PostBox-onLikeOrUnlike-handle-success: ', response.data)
          this.likes = response.data.current_likes
          // this.getPostComments(this.$route.params.id)
          // this.getPostLikes()
          this.$message({
            center: true,
            showClose: true,
            message: '点赞/取消点赞成功！', 
            type: 'success' 
            })
        })
        .catch((error) => {
          // handle error
          // console.log('PostBox-onLikeOrUnlike-catch-error: ', error)
          this.$message.error({        
            center: true,
            showClose: true,
            message: error.response.data.message
          })
        })
    }
  },
  created () {
    this.getPostComments(this.postID)
    this.getPostLikes()
  },
  watch: {
    postID: function (val, oldVal) {
      this.showCommentBox = false
      this.likes = this.getPostLikes()
    }
  },

}
</script>
