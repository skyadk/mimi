<template>
  <div class="text-center">
    <v-container>
      <v-row justify="end" class="pt-3 pr-3">
        <v-chip class="mt-3 mr-1" color="#6A1B9A" outlined small @click="bigDataRecommend">
          빅데이터 추천
        </v-chip>
        <v-chip class="mt-3 mr-1" color="#6A1B9A" outlined small @click="scoreRecommend">
          별점순
        </v-chip>
        <v-chip class="mt-3 mr-1" color="#6A1B9A" outlined small @click="distanceRecommend">
          거리순
        </v-chip>
      </v-row>
    </v-container>
    <div><br><p class="highlight"></p></div>

    <RestaurantList v-if="items" :items="items" />
  </div>
</template>

<script>
import RestaurantList from "@/components/restaurants/RestaurantList.vue";
import { mapState } from 'vuex'
import axios from 'axios'
export default {
  name: "Nearby",
  components: {
    RestaurantList,
  },
  props: {
    address: String,
    latitude: String,
    logitude: String,
  },
  data: () => ({
    serverUrl: process.env.VUE_APP_SERVER_URL,
    items: [],
  }),
  methods: {
    bigDataRecommend() {
      console.log('빅데이터 추천')
      const data = {
        u_address: this.address,
        u_lat: this.latitude,
        u_long: this.logitude,
        num: String(this.user),
      }
      console.log(data)
      this.items = []
      this.$store.commit('SET_LOADER_TRUE')
      axios.post(`${this.serverUrl}/recommendroad/bigdata-recommend`, data)
        .then(res => {
          console.log(res.data.message)
          this.items = res.data.message
          this.$store.commit('SET_LOADER_FALSE')
          if (this.items.length == 1 && this.items[0].sid == "NULL") {
            console.log('빅데이터 추천 결과 없음')
            alert('추천 결과가 없습니다. 리뷰를 많이 남길 수록 추천 정확도가 높아집니다.')
          }
        })
        .catch(err => {
          console.log(err)
          this.$store.commit('SET_LOADER_FALSE')
        })      
    },
    scoreRecommend() {
      console.log('평점순 추천')
      const data = {
        u_address: this.address,
        u_lat: this.latitude,
        u_long: this.logitude
      }
      this.items = []
      this.$store.commit('SET_LOADER_TRUE')
      console.log(data)
      axios.post(`${this.serverUrl}/recommendroad/star-recommend`, data)
        .then(res => {
          console.log(res.data.message)
          this.items = res.data.message
          this.$store.commit('SET_LOADER_FALSE')
        })
        .catch(err => {
          console.log(err)
          this.$store.commit('SET_LOADER_FALSE')
        })
    },
    distanceRecommend() {
      console.log('거리순 추천')
      const data = {
        u_address: this.address,
        u_lat: this.latitude,
        u_long: this.logitude,
      }
      this.items = []
      console.log(data)
      this.$store.commit('SET_LOADER_TRUE')
      axios.post(`${this.serverUrl}/recommendroad/distance-recommend`, data)
        .then(res => {
          console.log(res.data.message)
          this.items = res.data.message
          this.$store.commit('SET_LOADER_FALSE')
        })
        .catch(err => {
          console.log(err)
          this.$store.commit('SET_LOADER_FALSE')
        })
    }
  },
  computed: {
    ...mapState([
      'user',
    ])
  },
  watch: {
    latitude: function() {
      this.distanceRecommend()
    }
  },
  created() {
    this.distanceRecommend()
  }
}
</script>

<style scoped>
.font-weight {
  font-weight: bolder;
}
.highlight {
  border-bottom: 7px solid #dbdbdb;
  width: 80%;
  margin-top: 7px;
  margin-bottom: 12px;
  margin-left: 10%;
}
</style>
