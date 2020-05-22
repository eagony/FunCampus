<template>
  <baseview :post-type="'lostandfound'" :update-flag="route_update"></baseview>
</template>

<script>
import BaseView from "./BaseView";

export default {
  name: 'LostAndFound',
  components: {
    baseview: BaseView
  },
  data() {
    return {
      route_update: false 
    }
  },
  beforeRouteUpdate(to, from, next) {
    next()
    this.route_update = !this.route_update
  }
}
</script>