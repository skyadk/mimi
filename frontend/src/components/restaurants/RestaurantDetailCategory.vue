<template>
  <div>
  <v-card>
      <v-tabs
        dark
        background-color= "#EEEEEE"
        centered
        grow
      >
        <v-tab @click="clickCategory('정보')"><span class="category-color">기본정보</span>
        </v-tab>
        <v-tab @click="clickCategory('리뷰')"><span class="category-color">리뷰</span>
        </v-tab>
        <v-tab @click="clickCategory('지도')"><span class="category-color">지도</span>
        </v-tab>

      </v-tabs>
    </v-card>

    <div v-if="isInfo">
      <RestaurantDetailInfo :storeinfos="category1" :storemenus="category2"></RestaurantDetailInfo>
    </div>
    <div v-else-if="isReview">
      <RestaurantDetailReview :sid="category3"></RestaurantDetailReview>
    </div>
    <div v-else-if="isMap">
    <RestaurantDetailMap :storeinfo="category1"></RestaurantDetailMap>
    </div>
  </div>
</template>

<script>
import RestaurantDetailInfo from '@/components/restaurants/RestaurantDetailInfo.vue';
import RestaurantDetailReview from '@/components/restaurants/RestaurantDetailReview.vue';
import RestaurantDetailMap from '@/components/restaurants/RestaurantDetailMap.vue';

export default {
  name: 'RestaurantDetailCategory',
  components: {
    RestaurantDetailInfo,
    RestaurantDetailReview,
    RestaurantDetailMap,
  },
  props: {
    category1: Object,
    category2: [Array, Object],
    category3: Number,
  },
  data() {
    return {
      isInfo: true,
      isReview: false,
      isMap: false,
    };
  },
  methods: {
    clickCategory(categorizeItem) {
      this.isInfo = false;
      this.isReview = false;
      this.isMap = false;

      switch(categorizeItem){
        case "정보" :
          this.isInfo = true;
          break;
        case "리뷰" :
          this.isReview = true;
          break;
        case "지도" :
          this.isMap = true;
          break;
      }
    }
  },
  // created() {
  //   console.log('zkxprh')
  //   console.log(this.category1)
  //   console.log(this.category2)
  // }

}
</script>

<style scoped>
.category-color {
  font-weight: 700;
  color: #6A1B9A;
  font-size: 125%;
}
.categoty-imfo {
  padding-left: 60px;
  padding-right: 60px;
}
</style>