<template>
  <div>
  <wordcloud
    :data="defaultWords"
    nameKey="name"
    valueKey="value"
    class="description"
    :rotate="degrees"
    :color="myColors"
    :showTooltip="false"
    :wordClick="wordClickHandler">
  </wordcloud>  
  <div><br><p class="highlight"></p></div>
  <RestaurantList v-if="items" :items="items" />
  </div>
</template>

<script>
import RestaurantList from '@/components/restaurants/RestaurantList.vue'
import wordcloud  from 'vue-wordcloud'
import axios from 'axios'
export default {
  name: 'Keyword',
  components: {
    RestaurantList,
    wordcloud,
  },
  props: {
    latitude: String,
    logitude: String,
  },
  data: () => ({
    myColors: ['#6A1B9A', '#AB47BC', '#AD1457', '#EC407A'],
    degrees: {from: -10, to: 10, numOfOrientation: 5},
    selectKeyword: null,
    defaultWords: [],
    items: [],
  }),
  methods: {
    wordClickHandler(name, value, vm) {
      console.log('wordClickHandler', name, value, vm)
      this.selectKeyword = name
      alert(`'${name}' 키워드 적용`)
    },
    getKeyword() {
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        latitude: Number(this.latitude),
        logitude: Number(this.logitude)
      }
      console.log(data)
      this.defaultWords = []
      this.$store.commit('SET_LOADER_TRUE')
      axios.post(`${serverUrl}/recommendroad/hot-keyword-15`, data)
        .then(res => {
          console.log(res)
          const keywords = res.data.message
          keywords.forEach(k => {
            const name = k.keyword.keyword
            const value = k.keyword.value
            const word = {
              "name": name,
              "value": value,
            }
            this.defaultWords.push(word)
          })
          this.$store.commit('SET_LOADER_FALSE');
        })
        .catch(err => {
          console.log(err)
          alert('추천 키워드가 없습니다.')
          this.$store.commit('SET_LOADER_FALSE');
        })
    },
    getKeywordItems() {
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        keyword: this.selectKeyword,
        latitude: Number(this.latitude),
        logitude: Number(this.logitude),
      }
      console.log(data)
      this.items = []
      axios.post(`${serverUrl}/recommendroad/keyword-storelist`, data)
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
  watch: {
    selectKeyword: function () {
      console.log('키워드 변경 감지')
      if (this.selectKeyword != null) {
        this.getKeywordItems()
        this.$store.commit('SET_LOADER_TRUE')
      }
    },
    $router(to, from) {
      if (to.path != from.path) {
        this.$store.commit('SET_LOADER_FALSE');
      }
    },
    latitude: function() {
      this.getKeyword()
    },
  },
  created() {
    this.getKeyword()
  }
}
</script>

<style scoped>
  .description {
    font-family: "NanumBarunGothic", Helvetica, Arial;
    height: 500px;
  }
  .highlight {
  border-bottom: 7px solid #dbdbdb;
  width: 80%;
  margin-top: -60px;
  margin-bottom: 5px;
  margin-left: 10%;
}
</style>