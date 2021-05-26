<template>
  <v-app id="container">
      <TopBar />
      <div></div>
      <v-main style="position: relative; top: 56px !important; padding:0px">
        <router-view />
      </v-main>
      <BottomBar />
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import TopBar from '@/components/common/TopBar.vue'
import BottomBar from '@/components/common/BottomBar.vue'

export default {
  name: 'Home',
  components: {
    TopBar,
    BottomBar,
  },
  data: () => ({
    //
  }),
  methods: {

  },
  computed: {
    ...mapState([
      'login'
    ])
  },
  created() {
    if (this.login == false) {
      this.$router.push({name: 'Login'})
    }
  }
}
</script>

<style>
</style>