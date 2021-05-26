<template>
  <div>
    <v-app-bar 
      flat 
      fixed
      class="pa-0"
    >
      <v-toolbar-title>
        <label style="color:#283593"><router-link to='/' class="text-decoration-none">미미여지도</router-link></label>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="logout"><v-icon style="color:#3949AB">mdi-account-arrow-right</v-icon></v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'TopBar',
  components: {

  },
  data: () => ({
    //
  }),
  methods: {
    logout() {
      this.$store.dispatch('LOGOUT')
      this.$router.push({name: 'Login'})
    }
  },
  computed: {
    ...mapState([
      'login',
      'user',
    ])
  }
}
</script>

<style scoped>
/* .top {
  background-color: rgb(137, 137, 255);
} */

</style>