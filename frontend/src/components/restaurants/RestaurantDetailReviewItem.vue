<template>
  <div>
    <v-rating
      v-model="score"
      aria-readonly="h"
      readonly
      background-color="#FFC107"
      color="#FFC107"
      dense
      class="pl-4 pb-2"
    ></v-rating>
    <p class="pl-5 pr-5 mb-0">{{ item.content }}</p>
    <p class="mt-0 pl-5 pr-5">({{ item.reg_time }})</p>
    <v-row style="width: 90%; margin-left: 5%" class="mt-0 mb-0">
      <v-divider></v-divider>
    </v-row>  
  </div>
</template>

<script>
export default {
  name: 'RestaurantDetailReviewItem',
  props: {
    item: Object,
  },
  data: () => ({

  }),
  methods: {

  },
  computed: {
    score: function() {
      return Number(this.item.total_score)
    }
  },
}
</script>

<style>

</style>