<template>
  <div>
    <v-card :elevation= "0">
      <v-tabs
        dark
        background-color= "#EEEEEE"
        centered
        grow
      >
        <v-tab @click="clickCategory('근처')"><span class="category-color">주변맛집</span>
        </v-tab>
        <v-tab @click="clickCategory('키워드')"><span class="category-color">키워드맛집</span>
        </v-tab>

      </v-tabs>
    </v-card>
    <div v-if="isNearby">
    <Nearby :address="address" :latitude="latitude" :logitude="logitude"></Nearby>
    </div>
    <div v-else-if="!isNearby">
    <Keyword :latitude="latitude" :logitude="logitude"></Keyword>
    </div>
  </div>
  
</template>

<script>
import Nearby from '@/components/restaurants/Nearby.vue';
import Keyword from '@/components/restaurants/Keyword.vue';

export default {
  name: 'Category',
  components: {
    Keyword,
    Nearby,
  },
  props: {
    address: String,
    latitude: String,
    logitude: String,
  },
  data() {
    return {
      isKeyword: false,
      isNearby: true,
    };
  },
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
  }

}
</script>

<style scoped>
.category-color {
  font-weight: 700;
  color: black;
  font-size: 125%;
}

</style>