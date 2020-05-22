<template>
  <baseview :post-type="'teamup'" :update-flag="route_update"></baseview>
</template>

<script>
import BaseView from "./BaseView";

export default {
  name: 'TeamUp',
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