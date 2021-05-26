<template>
  <div>
    <v-card :elevation= "0">
      <v-tabs
        dark
        background-color= "#cabdda"
        centered
        grow
      >
        <v-tab @click="clickCategory('근처')"><span class="category-color">주변맛집</span>
        </v-tab>
        <v-tab @click="clickCategory('키워드')"><span class="category-color">키워드맛집</span>
        </v-tab>
      </v-tabs>
    </v-card>
    <div>
      <div v-if="isNearby">
      <Nearby :address="word" :latitude="lat" :logitude="log"></Nearby>
      </div>
      <div v-else-if="!isNearby">
      <Keyword :latitude="lat" :logitude="log"></Keyword>
      </div>
    </div>
  </div>
</template>

<script>
import Nearby from '@/components/restaurants/Nearby.vue';
import Keyword from '@/components/restaurants/Keyword.vue';
// import { postSearch } from '@/api/search'
// import { postSearchKeyword } from '@/api/search'

export default {
  name: 'RestaurantSearch',
  components: {
    Keyword,
    Nearby,
  },
  props: {
    word: String,
    lat: String,
    log: String,
  },
  data: () => ({
    isKeyword: false,
    isNearby: true,
  }),
  methods: {
    clickCategory(categorizeItem) {
      this.isKeyword = false;
      this.isNearby = false;

      switch(categorizeItem){
        case "근처" :
          this.isNearby = true;
          break;
        case "키워드" :
          this.isKeyword = true;
          break;
      }
    },
    // async getStoreList(data) {
    //   await postSearch(data)
    //     .then(res => {
    //       console.log(res)
    //       // console.log(JSON.stringify(res))
    //     })
    //     .catch(err => {
    //       console.log(err)
    //     })

    // },
    // async getKeywordList(data) {
    //   await postSearchKeyword(data)
    //     .then(res => {
    //       console.log(JSON.stringify(res))
    //     })
    //     .catch(err => {
    //       console.log(err)
    //     })
    // },
  },
  // async created() {
  //   const data = {
  //     keyword: this.word,
  //     latitude: this.lat,
  //     logitude: this.log,
  //   }
  //   this.getStoreList(data)
  //   this.getKeywordList(data)
  // },

}
</script>

<style scoped>
.bg {
  background-image: linear-gradient(to bottom right, #EDE7F6,#F8BBD0);
  /* min-height: 750px; */
  display: flex;
  flex-direction: column;
  align-items: center;
  top: 0; 
  left: 0; 
    
  /* Preserve aspet ratio */
  min-width: 100%;
  min-height: 100%;
}
.category-color {
  font-weight: 700;
  color: black;
  font-size: 125%;
}
.COLOR {
  color: #cabdda;
}
.highlight {
  border-bottom: 7px solid #EEEEEE;
  width: 30%;
  margin: auto;
}

</style>