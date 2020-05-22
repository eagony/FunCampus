<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
    <myfooter></myfooter>
  </div>
</template>

<script>
import Navbar from './components/Base/Navbar'
import Footer from "./components/Base/Footer";

export default {
  name: 'App',
  components: {
    navbar: Navbar,
    myfooter: Footer
  },
  created() {
    console.log(
      '❤ 参与维护请联系qq130199716. ❤')
  }
}
</script>

