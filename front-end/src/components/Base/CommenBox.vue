<template>
  <div class="container mt-1">
    <!-- 输入框 -->
    <form id="addCommentForm" v-if="sharedState.is_authenticated" @submit.prevent="onSubmitAddComment" @reset.prevent="onResetAddComment" class="g-mb-40">
      <div class="form-group">
        <textarea v-model="commentForm.content" class="form-control" id="commentFormContent" rows="3" placeholder="输入评论..."></textarea>
        <small class="form-control-feedback" v-show="commentForm.contentError">{{ commentForm.contentError }}</small>
      </div>
      <ul class="d-flex justify-content-end" >
        <button type="reset" class="btn btn-secondary mr-3">重置</button>
        <button type="submit" class="btn btn-primary">提交</button>
      </ul>
    </form>  
    <!-- 评论框  -->
    <div v-for="(comment, index) in this.comments" :key="index" class="shadow-sm p-3 mb-3 bg-light rounded">
      <div class="d-block justify-content-start">
        <div class="d-flex">
          <el-avatar class="mr-3" :src="comment.author.avatar" :size="25"></el-avatar>
          <span class="mb-1 ml-1 align-middle">
          {{ comment.author.name }} ：
          </span> 
        </div>
        <div class="d-flex ml-5">
          <span class="">{{ comment.content }}</span>
          <div v-if="false" class="ml-auto">
            <i class="mr-1 el-icon-apple"></i>
            <i class="mr-1 el-icon-s-comment"></i>
            <i class="mr-1 el-icon-delete-solid"></i>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import store from '../../store'

export default {
  props: ['postID'],
  data () {
    return {
      sharedState: store.state,
      commentForm: {
        content: '',
        post_id: '',
        parent_id: '',
        author_id: '',
        author_name: '',
        contentError: '',
        errors: 0
      },
      comments: {}
    }
  },
  methods: {
    getPostComments (id) { 
      let page = 1
      let per_page = 100
      const path = `/api/posts/${this.postID}/comments?page=${page}&per_page=${per_page}`
      this.$axios.get(path)
      .then((response) => {
        this.comments = response.data.items
      })
      .catch((error) => {
        // console.log('CommentBox-getPostComments-Catch-Error: ', error)
      })
    },
    onResetAddComment () {
      this.commentForm.content = '',
      this.commentForm.post_id = '',
      this.commentForm.parent_id = '',
      this.author_id = '',
      this.author_name = ''
      this.commentForm.contentError = null
    },
    onSubmitAddComment () {
      this.commentForm.contentError = 0
      
      if (!this.commentForm.content) {
        this.commentForm.errors += 1
        this.commentForm.contentError = '评论总得写点儿什么吧......'
      } else {
        this.commentForm.contentError = null
      }

      if (this.commentForm.errors > 0) {
        return false
      }

      const path = '/api/comments'
      let payload = ''
      if (this.commentForm.parent_id) {
        // 回复评论
        const at_who = `<a href="/user/${this.commentForm.author_id}" class="g-text-underline--none--hover">@${this.commentForm.author_name} </a>`
        payload = {
          post_id: this.postID,
          author_id: this.sharedState.user_id,
          parent_id: this.commentForm.parent_id,
          content: at_who + this.commentForm.content
        }
      } else {
        //一级评论
        payload = {
          post_id: this.postID,
          author_id: this.sharedState.user_id,
          content: this.commentForm.content
        }
      }

      this.$axios.post(path, payload)
      .then((response) => {
        this.$axios.get('/api/statistics/comment')
        this.onResetAddComment()
        this.getPostComments(this.post_id)
        this.$message({
          center: true,
          showClose: true,
          message: '成功添加评论。',
          type: 'success'
        })
      })
      .catch((error) => {
        // console.log('CommentBox-onSubmitAddComment-Catch-Error: ', error)
      })
    }
  },
  created () {
    const post_id = this.postID
    this.getPostComments(post_id)
  }
}
</script>