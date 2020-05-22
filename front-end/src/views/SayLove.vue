<template>
  <baseview :post-type="'saylove'" :update-flag="route_update"></baseview>
</template>

<script>
import BaseView from "./BaseView";

export default {
  name: 'SayLove',
  components: {
    baseview: BaseView
  },
  data() {
    return {
      route_update: false // 在true和false之间反复横跳，只要跟之前的变量不一样即可
    }
  },

  // 由于子组件不能正确检测到路由变化，由父组件监测路由
  // 并传给子组件一个标识路由变化的变量让子组件watch
  beforeRouteUpdate(to, from, next) {
  // 注意：要先执行next()不然this.$route.query还是之前的
    next()
    this.route_update = !this.route_update
  }
}
</script>