<template>
  <div id="container"> 
    <RestaurantItem
      v-for="(item, index) in items"
      :restaurantItem="item"
      :key="index" class="aaa"
    ></RestaurantItem>
  </div>
</template>

<script>
import RestaurantItem from "@/components/restaurants/RestaurantItem.vue";
// import axios from 'axios'
export default {
  name: "RestaurantList",
  components: {
    RestaurantItem,
  },
  props: {
    items: Array,
  },  
  data:() => ({

  }),
  methods: {

  }
}
</script>

<style scoped>
.aaa:last-child{
  margin-bottom: 60px;
}
</style>
