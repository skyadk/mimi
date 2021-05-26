<template>
  <div>
    <v-container v-for="(item, idx) in reviewList" :key="idx" class="pb-0">
      <RestaurantDetailReviewItem :item="item" />
    </v-container>
  </div>
</template>

<script>
import { getStoreReview } from '@/api/storedetail'
import RestaurantDetailReviewItem from './RestaurantDetailReviewItem.vue'
export default {
  name: '',
  components: {
    RestaurantDetailReviewItem,
  },
  props: {
    sid: Number,
  },
  data() {
    return {
      reviewList: []
    };
  },
  async created() {
    const storeReview = await getStoreReview(this.sid);
    this.reviewList = storeReview.data.result_set
    console.log(this.reviewList)
  }
}
</script>

<style>

</style>